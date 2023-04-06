from score_functions import *
class TPC:
    
    def __init__(self,network,data):
        self.network = network
        self.data = data
        self.table = {}
        variable_values = get_variable_values(data)
        for node in variable_values.keys(): #age
            print("node :")
            print(node)
            node_dict = {}
            node_dict[node] = variable_values[node]
            print("node dict :")
            print(node_dict) #age : [1,2,3]
            parents_dict = {}
            for parent in network.parents[node]:
                parents_dict[parent] = variable_values[parent]
            print("parents dict : ")
            print(parents_dict) #dico du noms des parents avec valeur qu'ils peuvent prendre
            dict = compute_all_combinations(node_dict,parents_dict,data) 
            print("dict " )
            print(dict)
            parent_values = set()
            #Finding all the parents combinations
            for key in dict.keys():
                extracted_value = key[1:]
                parent_values.add(extracted_value)
            parent_dict={}
            print("parent value :")
            print(parent_values) # toutes les combinaisons de parents possible
            for parent in parent_values :
                count_dict = compute_fixed_parents(node_dict,parent,dict)
                sum = 0
                for key in count_dict.keys():
                    sum += count_dict[key]
                parent_dict[parent]=sum #dico avec clé le tuple de valeur de parent et valeur le nombre de fois ou ca apparait
            print("parent_dict:")
            print(parent_dict)
            dico_proba={}
            for last_key in dict.keys():
                sum = parent_dict[last_key[1:]]
                if sum == 0 :
                    proba = 0
                else:
                    proba = dict[last_key]/sum
                dico_proba[last_key]=proba
            self.table[node]= dico_proba
           
          


