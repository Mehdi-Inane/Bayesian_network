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
            self.prob_parent[i] = self.tpc.table[variable][tupple] #dico ave clé tuple et valeur proba

        #trouver les children a verfier que ca trouves les bons trucs
        self.children = []
        for key in self.network.parents.keys():
            if variable in self.network.parents[key]:
                self.children.append(key)

        for i in variable_values[variable]:
            for enfant in self.children :
                x= []
                for p in self.network.parents[enfant]:
                    if p not in self.donnee.keys():
                        x+= [i]
                    else :
                        x += [self.donnee[p]] # pour recup le tuple de valeur de parent de enfant
                tupple = tuple([self.donnee[enfant]]+x) #pour avoir la bonne forme (1,2,1) de enfant et ses parents
                self.prob_parent[i] *= self.tpc.table[enfant][tupple] #dico ave clé tuple et valeur proba
        total=0
        index = 0
        normaliser = 0
        for i in self.prob_parent.keys():
                normaliser += self.prob_parent[i]
                if self.prob_parent[i]>total:
                    total = self.prob_parent[i]
                    index = i
        self.max = index #la proba max
        self.value_max = total/normaliser #le survived qui donne la bonne proba et on normalise en meme temps
