import pandas as pd
from BN import *
from score_functions import *
from search import *
from TPC import *
from proba import*


data = pd.read_csv("data/small.csv")
variable_values = get_variable_values(data) 

#Starting the search with an empty network
initial_network = BayesianNetwork(variables = list(variable_values.keys())) # variables = [ age, sex , ...]
initial_network.show_network()
optimal_network = bn_simulated_annealing(data, initial_network)
optimal_network.show_network()
print(optimal_network.parents)

tpc = TPC(optimal_network,data)

donnee = {"age" :2,"portembarked" : 2,"fare" : 1,"numparentschildren" : 1,"passengerclass" : 2,"sex" : 2,"numsiblings" : 1}
prob = Proba("survived", donnee, tpc, data, optimal_network)
print(prob.value_max)
