

import networkx as nx
import numpy as np




class DAG(nx.Digraph):
    def __init__(self,data):
        super(DAG,self).__init__(data)
        #Checking for cycles 
        try:
            nx.find_cycle(self)
        except nx.NetworkXNoCycle:
            pass
        else:
            raise ValueError("This graph has a directed cycle")
    
    # Adding a single node
    def add_node(self,node,weight=None):
        super(DAG, self).add_node(node, weight=weight)
    

    #Adding a node from an iterator
    def add_nodes_from(self,nodes,weights = None):
        if weights:
            if len(weights) == len(nodes):
                for i in range(len(nodes)):
                    self.add_node(nodes[i],weights[i])
        else:
            for i in range(len(nodes)):
                self.add_node(nodes[i])
    

    # Adding edges

    def add_edge(self,edge):
        pass

