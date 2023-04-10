from score_functions import *
class Proba:

    def __init__(self,variable, donnee, tpc, data, network):
        self.variable = variable
        self.donnee = donnee # {"age" : 3, "sex": 2 ...}
        self.network = network
        self.parent = self.network.parents[variable] #[sex, age, ..]
        self.data = data
        self.tpc= tpc
        #aller chercher la bonne tpc
        self.prob_parent={}
        variable_values = get_variable_values(data)
        for i in variable_values[variable]: #pour chaque valeur de survived
            x= []
            for p in self.parent:
                x += [self.donnee[p]] # pour recup le tuple de valeur de parent de var
            tupple = tuple([i]+x) #pour avoir la bonne forme (1,2,1) de variable et ses parents
            print(tupple)
            self.prob_parent[i] = self.tpc.table[variable][tupple] #dico ave clé tuple et valeur proba
        print(self.prob_parent)

        #trouver les children a verfier que ca trouves les bons trucs
        self.children = []
        for key in self.network.parents.keys():
            for j in network.parents[key]:
                if j == variable:
                    self.children.append(key)
        print(self.children)


        for i in variable_values[variable]:
            for enfant in self.children :
                x= []
                print(enfant)
                for p in self.network.parents[enfant]:
                    if p not in self.donnee.keys():
                        x+= [i]
                    else :
                        x += [self.donnee[p]] # pour recup le tuple de valeur de parent de enfant
                tupple = tuple([self.donnee[enfant]]+x) #pour avoir la bonne forme (1,2,1) de enfant et ses parents
                print(tupple)
                self.prob_parent[i] *= self.tpc.table[enfant][tupple] #dico ave clé tuple et valeur proba
        print(self.prob_parent)
        sum=0
        index = 0
        for i in self.prob_parent.keys():
                if self.prob_parent[i]>sum:
                    sum = self.prob_parent[i]
                    index = i
        self.max = i #la proba max
        self.value_max = sum #le survived qui donne la bonne proba
