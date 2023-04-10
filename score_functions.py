
import itertools
import scipy.special
from BN import *


#Function computing the different combinations of (Xi,Parents(Xi)) and counting each occurence
def compute_all_combinations(var,parents,data):
    #var is a dict of size 1 with var as key and list of values it can take as value
    #Parents is a dict with parent names as keys and list of values they can take as values
    
    #Finding the different instances (Xi,Parents(Xi))
    
    values = []
    variables = []
    for elem in var.keys():
        values.append(elem)
        variables.append(var[elem])
    for elem in parents.keys():
        values.append(elem)
        variables.append(parents[elem])
    variables = list(itertools.product(*variables))
    #Computing the M_ijk values and storing them
    #There is maybe a faster time to do this check : https://stackoverflow.com/questions/27654474/count-the-tuples-of-a-pandas-dataframe
    #getting the variable and parents names
    var_name = list(var.keys())[0]
    parent_names = list(parents.keys())
    new_data = data[[var_name] + parent_names]
    new_data.head()
    #transforming the dataframe into a list of tuples
    new_data = list(new_data.itertuples(index=False, name=None))
    count_dict={}
    for var in variables:
        count_dict[var] = 0
    for row in new_data:
        count_dict[row] += 1
    return count_dict
            

#Computing the occurences of a variable Xi and its fixed parent values
def compute_fixed_parents(var,parent_values,count_dict):
    #Var is a dict with all of the potential values as a value
    #parent_values is a tuple of fixed parent values
    var_name = list(var.keys())[0]
    new_dict = {}
    for elem in var[var_name]:
        new_dict[elem] = 0
    for key in count_dict.keys():
        #Split the tuple to get the x_value and the parent instantiation
        instantiation = key[1:]
        if instantiation == parent_values:
            new_dict[key[0]] += count_dict[key]
    return new_dict
        

#Computing the first internal sum of the Bayesian-Dirichlet score
def first_sum(var,parent_values,count_dict):
    x_counts = compute_fixed_parents(var,parent_values,count_dict)
    m_ij_0 = sum(x_counts.values())
    internal_sum = 0
    for key in x_counts:
        internal_sum += scipy.special.loggamma(1 + x_counts[key])
    #Finding the value of r_i
    var_name = list(var.keys())[0]
    r_i = len(var[var_name])
    internal_sum += (scipy.special.loggamma(r_i) - scipy.special.loggamma(r_i + m_ij_0))
    
    return internal_sum
    
#Computing the second internal sum of the Bayesian Dirichlet score
def sum_over_parents(var,parents,data):
    new_data_counts = compute_all_combinations(var,parents,data)
    parent_values = set()
    #Finding all the parents combinations
    for key in new_data_counts.keys():
        extracted_value = key[1:]
        parent_values.add(extracted_value)
    #Computing the outer-internal sum of the score
    ret_sum = 0
    for instantiation in parent_values:
        ret_sum += first_sum(var,instantiation,new_data_counts)
    return ret_sum

#Getting a dictionary of variables as keys and their different values as a list
def get_variable_values(df):
    return {c: list(df[c].unique()) for c in df.columns}

#Computing the Bayesian-Dirichlet score of a proposed network given a dataset
def compute_score(network,data,variable_values):
    score = 0
    for variable in variable_values.keys():
        #On a besoin d'un argument {variable_actuelle : valeurs}
        var_dict = {}
        var_dict[variable] = variable_values[variable]
        #Et d'un autre arguments {parents de la variable : leur valeurs}
        parents_dict = {}
        for parent in network.parents[variable]:
            parents_dict[parent] = variable_values[parent]
        score += sum_over_parents(var_dict,parents_dict,data)
    return score
        
