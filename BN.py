import networkx as nx
import random

class BayesianNetwork:
    
    def __init__(self,variables = [],edges = []):
        self.variables = variables
        self.parents = {}
        self.edges = []
        #Creating a dictionary for storing dependency relationships between variables
        for node in variables:
            self.parents[node] = []
        self.add_edges(edges)
            
    #Adding a dependency
    def add_edge(self,edge):
        self.edges.append(edge)
        self.parents[edge[1]].append(edge[0])
    
    
    def add_edges(self,edges):
        for edge in edges:
            self.edges.append(edge)
            self.parents[edge[1]].append(edge[0])

    #Removing a dependency
    def remove_edge(self,edge):
        if edge[0] in self.parents[edge[1]]:
            self.parents[edge[1]].remove(edge[0])
            self.edges.remove(edge)
    

    #Creating a new Bayesian network

    def copy(self):
        return BayesianNetwork(self.variables,self.edges.copy())
    
    def show_network(self):
        nx_graph = nx.DiGraph()
        nx_graph.add_nodes_from(self.variables)
        nx_graph.add_edges_from(self.edges)
        nx.draw(nx_graph,with_labels = True)
        
    
    def __eq__(self,graph):
        set_1 = set(self.edges)
        set_2 = set(graph.edges)
        return set_1 == set_2
        
            
#Function doing a DFS to check if a digraph is acyclic
def has_cycle(network,added_edge,reverse = False):
    graph = {}
    for elem in network.parents.keys():
        graph[elem] = []
        for elem_2 in network.parents[elem]:
            graph[elem].append(elem_2)
    if reverse: #If reversing the graph, we need to remove the edge from the adjacency list before adding
                #its reverse
        graph[added_edge[0]].remove(added_edge[1])
        graph[added_edge[1]].append(added_edge[0])
    else:
        #If we add an edge
        graph[added_edge[1]].append(added_edge[0])
    visited = set()
    stack = set()
    # DFS function
    def dfs(node):
        visited.add(node)
        stack.add(node)
        if node in graph:
            for parent in graph[node]:
                if parent not in visited:
                    if dfs(parent):
                        return True
                elif parent in stack:
                    return True
        stack.remove(node)
        return False
    # Check for cycles
    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    return False

#Function generating a new DAG by either adding, deleting or reversing an edge
def get_new_network(network):
        #Choosing from either deleting an edge or adding one
        i = random.randint(0,2)
        new_network = network.copy()
        #Adding an edge
        u , w = random.randint(0,len(network.variables) - 1),random.randint(0,len(network.variables) - 1)
        if i == 0 or (len(network.edges) == 0):
            simple_digraph = False
            while(True):
                u , w = random.randint(0,len(network.variables) - 1),random.randint(0,len(network.variables) - 1)
                #Checking if it's a new edge
                if (network.variables[u] not in network.parents[network.variables[w]]):
                    #Checking if it's not a loop and that it does not create a cycle
                    if ((u != w) and not(has_cycle(network,(network.variables[u],network.variables[w])))):
                        new_network.add_edge((network.variables[u],network.variables[w]))
                        break
        #Deleting an edge
        elif i == 1:
            while(network.variables[u] not in network.parents[network.variables[w]]):
                u , w = random.randint(0,len(network.variables) - 1),random.randint(0,len(network.variables) - 1)
            new_network.remove_edge((network.variables[u],network.variables[w]))
        #Reversing an edge
        else:
            visited = set()
            #Choosing a random edge to reverse
            while(True):
                if len(visited) == len(network.edges):
                    return network
                i = random.randint(0,len(network.edges)-1)
                var_1,var_2 = network.edges[i]
                if (var_1,var_2) in visited:
                    continue
                visited.add((var_1,var_2))
                #Checking if reversing an edge does not create a cycle
                if not(has_cycle(network,(var_2,var_1),reverse = True)):
                    new_network.remove_edge(network.edges[i])
                    new_network.add_edge((var_2,var_1))
                    break
        return new_network
            
                
    

    



