import pandas as pd
from BN import *
from score_functions import *
from search import *



data = pd.read_csv("small.csv")
variable_values = get_variable_values(data)
#Starting the search with an empty network
initial_network = BayesianNetwork(variables = list(variable_values.keys()))
initial_network.show_network()
optimal_network = bn_simulated_annealing(data, initial_network)
optimal_network.show_network()