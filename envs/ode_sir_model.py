#init and simulate_day are the interface of EpiModel, we will have a BiomialEpiModel as well, 
# that implements this same interface

from scipy.integrate import odeint
import numpy as np


class OdeEpiModel:
    #having a actor that allows initation from a particular state,
    #and a function to forward simulate a day, should allow us
    #to do everything we want,
    #standard trajectories via an MDP
    #running parts of a trajectory (for value iteration methods)
    #?
    
    def __init__(self, N, K, init_model_state, beta, gamma):
        #age groups
        self.K = K        
        #initial model state
        self.init_model_state = init_model_state
        #current model state
        self.current_model_state = init_model_state
        #parameters
        self.beta = beta
        self.gamma = gamma
        self.N = N
        self.n_comp = 3

    #number of compartments in each age groups

    #functions to compute the index, for the input and output vectors
    #return the idx for compartment S for age group k
    def S(self, k):
        return (self.n_comp*k) + 0

    def I(self, k):
        return (self.n_comp*k) + 1

    def R(self, k):
        return (self.n_comp*k) + 2

    #C is the contact matrix to be used,
    #would be used in beta
    def simulate_day(self, C=0):
        #TODO: check the size of C
        def deriv(y, t, N, beta, gamma):
            d_ = np.empty([(self.n_comp * self.K)])
            for k in range(self.K):
                d_[self.S(k)] = -beta * y[self.S(k)] * y[self.I(k)] / N
                d_[self.I(k)] = beta * y[self.S(k)] * y[self.I(k)] / N - gamma * y[self.I(k)]
                d_[self.R(k)] = gamma * y[self.I(k)]

            return d_


        #run the ode, something like this:
        # Initial conditions vector
        y0 = self.current_model_state        
        # Integrate the SIR equations over the time grid, t.
        #TODO: decide on t,
        #important, we will simulate one day here,
        #that should be OK for an ODE approximation, I think...
        # time for each hour of a day - needs to be defined        
        t = np.linspace(0,23,24)
        ret = odeint(deriv, y0, t, args=(self.N, self.beta, self.gamma))
        # state will be the last time period
        self.current_model_state = ret[-1].T

        return self.current_model_state
        
            
"""    
def main():
    # Parameters for SIR
    # K = number of age groups
    k = 2
    # init_model_state
    init_state = [49, 1, 0, 48, 1, 1]
    # beta
    beta = 0.05
    # gamma
    gamma = 1/3

    timesteps = 1
    ode_epi_model = OdeEpiModel(k, init_state, beta, gamma)

    for i in range(timesteps):        
        print("state:", ode_epi_model.simulate_day())

if __name__ == "__main__":
    main()

"""