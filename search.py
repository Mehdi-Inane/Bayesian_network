
from score_functions import *
from BN import *
import numpy as np

def acceptance_probability(old_score, new_score, temperature):
    if new_score > old_score:
        return 1.0
    else:
        return np.exp((new_score - old_score) / temperature)

#Implementing the simulated annealing algorithm
def bn_simulated_annealing(data,init_network,temperature = 1000,cooling_rate = 0.95,max_iterations = 1000):
    variable_values = get_variable_values(data)
    current_network = init_network.copy()
    current_score = compute_score(current_network,data,variable_values)
    print(current_score)
    visited_graphs = set()
    for i in range(max_iterations):
        if (i % 10 == 0):
            #print("iteration",i)
            pass
        new_network = get_new_network(current_network)
        new_score = compute_score(new_network,data,variable_values)
        
        prob = acceptance_probability(current_score, new_score, temperature)
        rand = np.random.rand()
        if  rand < prob:
            current_network = new_network
            current_score = new_score
            #print(current_score)
        temperature *= cooling_rate
    print(current_score)
    return current_network