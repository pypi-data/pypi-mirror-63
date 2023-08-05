import random
from numpy import log,sqrt,power
from scipy.stats import poisson
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
from scipy.special import comb
from itertools import product,chain
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import warnings
import os
import cmocean
import matplotlib.ticker as mtick

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. '+directory)

def parent_directory(n):
    path = ''
    while n:
        path = os.path.join(path,os.pardir)
        n -= 1
    path = os.path.abspath(path)
    return path
    
warnings.filterwarnings('ignore')

seed = None

def set_seed(num):
    global seed
    seed = num

class Environment:
    def __init__(self,sale=None,wholesale=None,retail=None,r=None,gamma=None,N=None,M=None,lam=None,start_state=(1,0),fit=True):
        self.sale = sale
        self.wholesale = wholesale
        self.retail = retail
        self.r = r
        self.gamma = gamma
        self.N = N
        self.M = M
        self.lam = lam
        if self.lam is not None:
            self.poi = poisson(self.lam)
            self.poi.random_state = np.random.RandomState(seed)
        self.start_state = start_state
        self.time_range = range(self.start_state[0],self.N)
        self.memory = TabularMemory()
        if fit:
            self._fit()

    def states(self):
        return chain(
            product(*(range(self.start_state[0],self.start_state[0]+1),range(self.start_state[1],self.start_state[1]+1))),
            product(*(range(self.start_state[0]+1,self.N+1),range(self.M+1)))
            )
    
    def actions(self,state):
        if state[0] == self.N:
            return product(*(range(1),))
        return product(*(range(self.M-state[1]+1),))
    
    def terminal_reward(self,state):
        return self.sale*state[1]
    
    def interact(self,state,action):
        demand = self.poi.rvs()
        R = self.gamma*self.retail*min(demand,state[1]+action[0])-self.wholesale*action[0]-self.gamma*self.r*self.wholesale*(state[1]+action[0])
        next_state = (state[0]+1,max(0,state[1]+action[0]-demand))
        return R,next_state
    
    def normalize_state(self,state):
        return (state[0]/self.N,state[1]/self.M)
    
    def normalize_action(self,action):
        return (action[0]/self.M,)
    
    def _dim_state(self):
        return len(next(self.states()))
    
    def _dim_action(self):
        return len(next(self.actions(self.start_state)))

    def _fit(self):
        self._V(self.start_state)
    
    def _V(self,state):
        t = state[0]
        inventory = state[1]
        if state in self.memory.V:
            return self.memory.V[state]
        if t == self.N:
            action = (0,)
            self.memory.Q[state][action] = self.memory.Q.setdefault(state,{}).get(action,self.sale*inventory)
            self.memory.V[state] = self.memory.Q[state][action]
            self.memory.A[state] = action
            return self.memory.V[state]
        for action in self.actions(state):
            buy = action[0]
            expected_demand = 0
            expected_V = 0
            for demand in range(inventory+buy+1):
                if demand == inventory+buy:
                    prob = 1-self.poi.cdf(demand-1)
                else:
                    prob = self.poi.pmf(demand)
                expected_demand += demand*prob
                expected_V += self._V((t+1,inventory+buy-demand))*prob
            expected_revenue = self.gamma*self.retail*expected_demand
            cost = self.wholesale*buy+self.gamma*self.r*self.wholesale*(inventory+buy)
            expected_R = expected_revenue-cost
            self.memory.Q[state][action] = self.memory.Q.setdefault(state,{}).get(action,expected_R+self.gamma*expected_V)
        self.memory.V[state] = self.memory.V.get(state,max(self.memory.Q[state].values()))
        self.memory.A[state] = self.memory.A.get(state,max(self.memory.Q[state],key=self.memory.Q[state].get))
        return self.memory.V[state]

class TabularMemory:
    def __init__(self):
        self.type = 'tabular'
        self.Q = {}
        self.N = {}
        self.V = {}
        self.A = {}
    
    def reset(self,env):
        self.init_Q(env)
        self.init_N(env)
    
    def init_Q(self,env):
        for state in env.states():
            for action in env.actions(state):
                self.Q[state][action] = self.Q.setdefault(state,{}).get(action,0)
                if state[0] == env.N:
                    self.Q[state][action] += env.terminal_reward(state)
    
    def init_N(self,env):
        for state in env.states():
            for action in env.actions(state):
                self.N[state][action] = self.N.setdefault(state,{}).get(action,0)

class ApproxMemory:
    def __init__(self,degree=2):
        self.type = 'approx'
        self.degree = degree
        self.poly = PolynomialFeatures(degree=self.degree)
        self.W = None
        self.approxQ = lambda normalized_state,normalized_action: np.dot(self.poly.fit_transform(self.features(normalized_state,normalized_action)).flat,self.W)
    
    def reset(self,env):
        self.W = np.zeros(comb(env._dim_state()+env._dim_action()+self.degree,self.degree,exact=True))
    
    def features(self,normalized_state,normalized_action):
        return np.append(normalized_state,normalized_action).reshape(1,-1)
    
    def get_Q(self,env):
        Q = {}
        for state in env.states():
            for action in env.actions(state):
                Q[state][action] = Q.setdefault(state,{}).get(action,0)
                if state[0] == env.N:
                    Q[state][action] += env.terminal_reward(state)
                else:
                    Q[state][action] += self.approxQ(env.normalize_state(state),env.normalize_action(action))
        return Q

class PerformanceMemory:
    def __init__(self):
        self.type = 'performance'
        self.seq_V = []
        self.seq_A = []
        self.total_V = 0
        self.seq_rmse_Q = []
        self.seq_rmse_V = []
        self.seq_rmse_A = []
        self.seq_G = []
    
    def reset(self):
        self.seq_V = []
        self.seq_A = []
        self.total_V = 0
        self.seq_rmse_Q = []
        self.seq_rmse_V = []
        self.seq_rmse_A = []
        self.seq_G = []

class Metrics:
    def rmse(self,env,Q_pred):
        rmse_Q = 0
        n = 0
        for state in env.memory.Q.keys():
            for action in env.memory.Q[state].keys():
                if state[0] == env.N:
                    continue
                rmse_Q += (env.memory.Q[state][action]-Q_pred[state][action])**2
                n += 1
        rmse_Q = sqrt(rmse_Q/n)

        rmse_V = 0
        rmse_A = [0]*len(env.memory.A[env.start_state])
        n = 0
        for state in env.memory.V.keys():
            if state[0] == env.N:
                continue
            rmse_V += (env.memory.V[state]-max(Q_pred[state].values()))**2
            for i in range(len(rmse_A)):
                rmse_A[i] += (env.memory.A[state][i]-max(Q_pred[state],key=Q_pred[state].get)[i])**2
            n += 1
        rmse_V = sqrt(rmse_V/n)
        for i in range(len(rmse_A)):
            rmse_A[i] = sqrt(rmse_A[i]/n)
        return rmse_Q,rmse_V,rmse_A
    
    def create_figure(self,env):
        plt.rcParams.update({'font.size': 16})
        self.nrow = 1
        self.ncol = (env.N-env.start_state[0]+1)
        self.fig = plt.figure(figsize=plt.figaspect(1/self.ncol))
        self.inches = 5
        self.fig.set_size_inches(self.inches*self.ncol,self.inches)
        self.elev = 30
        self.azim = 45+180

    def plot_Q(self,env,Q_pred,name,episodes,silent_plot,save_figure):
        if silent_plot and not save_figure:
            pass
        self.create_figure(env)
        self.fig.suptitle(f'Q-values over State and Action for {name} at Episode {episodes}',fontsize=36)
        for index,t in enumerate(range(env.start_state[0],env.N+1)):
            x = np.arange(env.M+1)
            y = np.arange(env.M+1)
            z = []
            z_pred = []
            for buy in y:
                z.append([])
                z_pred.append([])
                for inventory in x:
                    if (t,inventory) not in env.memory.Q:
                        z[-1].append(np.nan)
                        z_pred[-1].append(np.nan)
                        continue
                    z[-1].append(env.memory.Q[(t,inventory)].get((buy,),np.nan))
                    z_pred[-1].append(Q_pred[(t,inventory)].get((buy,),np.nan))
            x,y = np.meshgrid(x,y)
            z = np.array(z)
            z_pred = np.array(z_pred)

            ax = self.fig.add_subplot(self.nrow,self.ncol,index+1,projection='3d')
            ax.view_init(elev=self.elev,azim=self.azim)
            ax.set_title(f'At Time {t}')
            ax.set_xlabel('State',labelpad=7)
            ax.set_ylabel('Action',labelpad=7)
            ax.set_zlabel('Q-value')
            ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))
            ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))
            ax.zaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))
            if t == env.start_state[0] or t == env.N:
                ax.plot_wireframe(x,y,z_pred,color='crimson',alpha=.75)
                ax.plot_wireframe(x,y,z,color='royalblue',alpha=.75)
            else:
                ax.plot_surface(x,y,z_pred,cmap=cmocean.cm.thermal,vmin=np.nanmin(z_pred),vmax=np.nanmax(z_pred),alpha=.75)
                ax.plot_surface(x,y,z,cmap=cmocean.cm.haline,vmin=np.nanmin(z),vmax=np.nanmax(z),alpha=.75)

        plt.tight_layout()
        plt.subplots_adjust(top=.85)
        if not silent_plot:
            plt.show()
        if save_figure:
            path = parent_directory(0)+rf'\plots\{name}\Q\episode_{episodes}'
            create_folder(path)
            plt.savefig(path+r'\fig.svg',bbox_inches='tight',transparent=True)
        plt.close('all')
    
    def plot_V(self,env,Q_pred,name,episodes,silent_plot,save_figure):
        if silent_plot and not save_figure:
            pass
        self.create_figure(env)
        self.fig.suptitle(f'V-values over State for {name} at Episode {episodes}',fontsize=36)
        x = np.arange(env.M+1)
        for index,t in enumerate(range(env.start_state[0],env.N+1)):
            y = []
            y_pred = []
            for inventory in x:
                if (t,inventory) in env.memory.V:
                    y.append(env.memory.V[(t,inventory)])
                else:
                    y.append(np.nan)
                if (t,inventory) in Q_pred:
                    y_pred.append(max(Q_pred[(t,inventory)].values()))
                else:
                    y_pred.append(np.nan)

            ax = self.fig.add_subplot(self.nrow,self.ncol,index+1)
            ax.set_title(f'At Time {t}')
            ax.set_xlabel('State')
            ax.set_ylabel('V-value')
            ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))
            ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))
            min_x = np.nanmin(x)
            max_x = np.nanmax(x)
            range_x = max_x-min_x
            ax.set_xlim([min_x-.1*range_x,max_x+.1*range_x])
            min_y = 0
            max_y = np.nanmax(y+y_pred)
            range_y = max_y-min_y
            ax.set_ylim([min_y-.1*range_y,max_y+.1*range_y])
            if t == env.start_state[0]:
                ax.scatter(x,y_pred,color='crimson',alpha=.75)
                ax.scatter(x,y,color='royalblue',alpha=.75)
            else:
                ax.plot(x,y_pred,color='crimson',alpha=.75)
                ax.plot(x,y,color='royalblue',alpha=.75)

        plt.tight_layout()
        plt.subplots_adjust(top=.80)
        if not silent_plot:
            plt.show()
        if save_figure:
            path = parent_directory(0)+rf'\plots\{name}\V\episode_{episodes}'
            create_folder(path)
            plt.savefig(path+r'\fig.svg',bbox_inches='tight',transparent=True)
        plt.close('all')
    
    def plot_A(self,env,Q_pred,name,episodes,silent_plot,save_figure):
        if silent_plot and not save_figure:
            pass
        self.create_figure(env)
        self.fig.suptitle(f'A-values over State for {name} at Episode {episodes}',fontsize=36)
        x = np.arange(env.M+1)
        for index,t in enumerate(range(env.start_state[0],env.N+1)):
            y = []
            y_pred = []
            for inventory in x:
                if (t,inventory) in env.memory.A:
                    y.append(env.memory.A[(t,inventory)][0])
                else:
                    y.append(np.nan)
                if (t,inventory) in Q_pred:
                    y_pred.append(max(Q_pred[(t,inventory)],key=Q_pred[(t,inventory)].get)[0])
                else:
                    y_pred.append(np.nan)

            ax = self.fig.add_subplot(self.nrow,self.ncol,index+1)
            ax.set_title(f'At Time {t}')
            ax.set_xlabel('State')
            ax.set_ylabel('A-value')
            ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))
            ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))
            min_x = np.nanmin(x)
            max_x = np.nanmax(x)
            range_x = max_x-min_x
            ax.set_xlim([min_x-.1*range_x,max_x+.1*range_x])
            min_y = 0
            max_y = np.nanmax(y+y_pred)
            range_y = max_y-min_y
            ax.set_ylim([min_y-.1*range_y,max_y+.1*range_y])
            if t == env.start_state[0]:
                ax.scatter(x,y_pred,color='crimson',alpha=.75)
                ax.scatter(x,y,color='royalblue',alpha=.75)
            else:
                ax.plot(x,y_pred,color='crimson',alpha=.75)
                ax.plot(x,y,color='royalblue',alpha=.75)

        plt.tight_layout()
        plt.subplots_adjust(top=.80)
        if not silent_plot:
            plt.show()
        if save_figure:
            path = parent_directory(0)+rf'\plots\{name}\A\episode_{episodes}'
            create_folder(path)
            plt.savefig(path+r'\fig.svg',bbox_inches='tight',transparent=True)
        plt.close('all')

class EpsilonGreedy:
    def __init__(self,eps=.05,decay=None):
        self.eps = lambda episode: 1/(1+episode/decay) if decay is not None else eps
        self.random = random
        self.random.seed(seed)

    def get_action(self,state,env,episode,memory,memory2=None):
        if self.random.random() < self.eps(episode):
            return self.random.choice([action for action in env.actions(state)])
        if memory.type == 'tabular':
            Q = memory.Q[state]
            if memory2 is not None:
                Q2 = memory2.Q[state]
                Q = {action: (Q[action]+Q2[action])/2 for action in Q.keys()}
        if memory.type == 'approx':
            Q = {action: memory.approxQ(env.normalize_state(state),env.normalize_action(action)) for action in env.actions(state)}
        max_Q = max(Q.values())
        return self.random.choice([action for action in Q.keys() if Q[action] == max_Q])

class Agent:
    def __init__(self,policy,lr,method):
        self.method = method
        if self.method == 'tabular':
            self.memory = TabularMemory()
        if self.method == 'approx':
            self.memory = ApproxMemory()
        self.policy = policy
        self.lr = lr
        self.episode = 0
        self.greedy = EpsilonGreedy(eps=0)
        self.performance_memory = PerformanceMemory()
        self.metrics = Metrics()
        self.name = None
        self.init = None
    
    def verbose_line(self,env,episodes,verbose,verbose_freq,silent_plot,save_figure,plot_freq):
        if verbose and self.episode % round(verbose_freq*episodes) == 0:
            if self.method == 'tabular':
                Q = self.memory.Q
            if self.method == 'approx':
                Q = self.memory.get_Q(env)
            rmse_Q,rmse_V,rmse_A = self.metrics.rmse(env,Q)
            self.performance_memory.seq_rmse_Q.append(rmse_Q)
            self.performance_memory.seq_rmse_V.append(rmse_V)
            self.performance_memory.seq_rmse_A.append(rmse_A)
            print(f'episode = {self.episode} {self.name} rmse_Q = {rmse_Q} rmse_V = {rmse_V} rmse_A = {rmse_A}')
            if self.episode % round(plot_freq*episodes) == 0:
                self.metrics.plot_Q(env,Q,self.name,self.episode,silent_plot,save_figure)
                self.metrics.plot_V(env,Q,self.name,self.episode,silent_plot,save_figure)
                self.metrics.plot_A(env,Q,self.name,self.episode,silent_plot,save_figure)

class MonteCarlo(Agent):
    def __init__(self,policy,lr,method='tabular'):
        super().__init__(policy,lr,method)
        self.name = 'Monte Carlo'
    
    def fit(self,env,episodes,init=None,verbose=True,verbose_freq=.1,silent_plot=False,save_figure=False,plot_freq=1):
        if self.init is None or init:
            self.init = False
            self.memory.reset(env)
            self.performance_memory.reset()
            self.episode = 0
        for _ in range(episodes):
            self.episode += 1
            states = {}
            actions = {}
            rewards = {}
            G = 0
            state = env.start_state
            action = self.policy.get_action(state,env,self.episode,self.memory)
            for t in env.time_range:
                states[t] = state
                actions[t] = action
                R,next_state = env.interact(state,action)
                rewards[t] = R
                if next_state[0] == env.N:
                    next_action = next(env.actions(next_state))
                else:
                    next_action = self.policy.get_action(next_state,env,self.episode,self.memory)
                state = next_state
                action = next_action
            G += env.terminal_reward(state)
            for t in reversed(env.time_range):
                state = states[t]
                action = actions[t]
                R = rewards[t]
                G *= env.gamma
                G += R
                self.memory.N[state][action] += 1
                self.memory.Q[state][action] += 1/self.memory.N[state][action]*(G-self.memory.Q[state][action])
            Q = self.memory.Q[env.start_state]
            self.performance_memory.seq_V.append(max(Q.values()))
            self.performance_memory.seq_A.append(max(Q,key=Q.get))
            self.performance_memory.total_V += self.performance_memory.seq_V[-1]
            self.performance_memory.seq_G.append(G)
            self.verbose_line(env,episodes,verbose,verbose_freq,silent_plot,save_figure,plot_freq)

class Sarsa(Agent):
    def __init__(self,policy,lr,method='tabular'):
        super().__init__(policy,lr,method)
        self.name = 'Sarsa'
        if self.method == 'approx':
            self.name = 'Episodic Semi-gradient '+self.name
    
    def fit(self,env,episodes,init=None,verbose=True,verbose_freq=.1,silent_plot=False,save_figure=False,plot_freq=1):
        if self.init is None or init:
            self.init = False
            self.memory.reset(env)
            self.performance_memory.reset()
            self.episode = 0
        for _ in range(episodes):
            self.episode += 1
            G = 0
            state = env.start_state
            action = self.policy.get_action(state,env,self.episode,self.memory)
            for t in env.time_range:
                R,next_state = env.interact(state,action)
                G += power(env.gamma,t-env.start_state[0])*R
                if next_state[0] == env.N:
                    next_action = next(env.actions(next_state))
                else:
                    next_action = self.policy.get_action(next_state,env,self.episode,self.memory)
                if self.method == 'tabular':
                    U = R+env.gamma*self.memory.Q[next_state][next_action]
                    self.memory.Q[state][action] += self.lr*(U-self.memory.Q[state][action])
                    self.memory.N[state][action] += 1
                if self.method == 'approx':
                    if next_state[0] == env.N:
                        U = R+env.gamma*env.terminal_reward(next_state)
                    else:
                        U = R+env.gamma*self.memory.approxQ(env.normalize_state(next_state),env.normalize_action(next_action))
                    self.memory.W += self.lr*(U-self.memory.approxQ(env.normalize_state(state),env.normalize_action(action)))*self.memory.poly.fit_transform(self.memory.features(env.normalize_state(state),env.normalize_action(action))).flat
                state = next_state
                action = next_action
            G += power(env.gamma,env.N-env.start_state[0])*env.terminal_reward(state)
            if self.method == 'tabular':
                Q = self.memory.Q[env.start_state]
            if self.method == 'approx':
                Q = {action: self.memory.approxQ(env.normalize_state(env.start_state),env.normalize_action(action)) for action in env.actions(env.start_state)}
            self.performance_memory.seq_V.append(max(Q.values()))
            self.performance_memory.seq_A.append(max(Q,key=Q.get))
            self.performance_memory.total_V += self.performance_memory.seq_V[-1]
            self.performance_memory.seq_G.append(G)
            self.verbose_line(env,episodes,verbose,verbose_freq,silent_plot,save_figure,plot_freq)

class QLearning(Agent):
    def __init__(self,policy,lr,method='tabular'):
        super().__init__(policy,lr,method)
        self.name = 'Q-learning'

    def fit(self,env,episodes,init=None,verbose=True,verbose_freq=.1,silent_plot=False,save_figure=False,plot_freq=1):
        if self.init is None or init:
            self.init = False
            self.memory.reset(env)
            self.performance_memory.reset()
            self.episode = 0
        for _ in range(episodes):
            self.episode += 1
            G = 0
            state = env.start_state
            for t in env.time_range:
                action = self.policy.get_action(state,env,self.episode,self.memory)
                R,next_state = env.interact(state,action)
                G += power(env.gamma,t-env.start_state[0])*R
                if next_state[0] == env.N:
                    next_action = next(env.actions(next_state))
                else:
                    next_action = self.greedy.get_action(next_state,env,self.episode,self.memory)
                U = R+env.gamma*self.memory.Q[next_state][next_action]
                self.memory.Q[state][action] += self.lr*(U-self.memory.Q[state][action])
                self.memory.N[state][action] += 1
                state = next_state
            G += power(env.gamma,env.N-env.start_state[0])*env.terminal_reward(state)
            Q = self.memory.Q[env.start_state]
            self.performance_memory.seq_V.append(max(Q.values()))
            self.performance_memory.seq_A.append(max(Q,key=Q.get))
            self.performance_memory.total_V += self.performance_memory.seq_V[-1]
            self.performance_memory.seq_G.append(G)
            self.verbose_line(env,episodes,verbose,verbose_freq,silent_plot,save_figure,plot_freq)

class DoubleQLearning(Agent):
    def __init__(self,policy,lr,method='tabular'):
        super().__init__(policy,lr,method)
        if self.method == 'tabular':
            self.memory2 = TabularMemory()
        self.name = 'Double Q-learning'
        self.random = random
        self.random.seed(seed)

    def fit(self,env,episodes,init=None,verbose=True,verbose_freq=.1,silent_plot=False,save_figure=False,plot_freq=1):
        if self.init is None or init:
            self.init = False
            self.memory.reset(env)
            self.memory2.reset(env)
            self.performance_memory.reset()
            self.episode = 0
        for _ in range(episodes):
            self.episode += 1
            G = 0
            state = env.start_state
            for t in env.time_range:
                action = self.policy.get_action(state,env,self.episode,self.memory,self.memory2)
                R,next_state = env.interact(state,action)
                G += power(env.gamma,t-env.start_state[0])*R
                rand = self.random.random() < .5
                if next_state[0] == env.N:
                    next_action = next(env.actions(next_state))
                else:
                    if rand:
                        next_action = self.greedy.get_action(next_state,env,self.episode,self.memory)
                    else:
                        next_action = self.greedy.get_action(next_state,env,self.episode,self.memory2)
                if rand:
                    U = R+env.gamma*self.memory2.Q[next_state][next_action]
                    self.memory.Q[state][action] += self.lr*(U-self.memory.Q[state][action])
                    self.memory.N[state][action] += 1
                else:
                    U = R+env.gamma*self.memory.Q[next_state][next_action]
                    self.memory2.Q[state][action] += self.lr*(U-self.memory2.Q[state][action])
                    self.memory2.N[state][action] += 1
                state = next_state
            G += power(env.gamma,env.N-env.start_state[0])*env.terminal_reward(state)
            Q = self.memory.Q[env.start_state]
            Q2 = self.memory2.Q[env.start_state]
            Q = {action: (Q[action]+Q2[action])/2 for action in Q.keys()}
            self.performance_memory.seq_V.append(max(Q.values()))
            self.performance_memory.seq_A.append(max(Q,key=Q.get))
            self.performance_memory.total_V += self.performance_memory.seq_V[-1]
            self.performance_memory.seq_G.append(G)
            self.verbose_line(env,episodes,verbose,verbose_freq,silent_plot,save_figure,plot_freq)