from graphviz import Digraph

class ArbreBinaire:
    def __init__(self,cle , gauche = None, droite = None):
        self.cle = cle
        self.gauche = gauche
        self.droite = droite
        
class ArbreDST :
    def __init__(self, dico , c = None):
        self.dico = dico  # Exemple : dico = {'a':'01','b':'11','c':'00','d':'10'}
        self.racine = None            

    def car(self, c , i):
        """DST * str * int -> int/None"""
        """Renvoie le i-ème caractère de l'encodage de c, lorsque c existe dans le dictionnaire, None sinon"""
        for k , v in self.dico.items():
            if k == c and len(v)-1 >= i:
                res= v[i]
                return int(res)
        return None

    def duplique(self , noeud): #A est un arbre binaire
        """DST * ArbreBinaire -> ArbreBinaire"""
        """Renvoie une copie de l'arbre binaire A"""
        #print("passage ?")
        if noeud is None:
            return None
        else:
            return ArbreBinaire(noeud.cle, self.duplique(noeud.gauche), self.duplique(noeud.droite))
        

    def ajout(self, c ): #c est un caractère
        """DST * str -> ArbreBinaire"""
        """Renvoie un arbre binaire contenant le caractère c"""
        return self._ajout(c , 0 , self.racine)

    def _ajout(self, c , i , noeud): #noeud est un arbre binaire
        """DST * str * int * ArbreBinaire -> ArbreBinaire"""
        """Renvoie un arbre binaire contenant le caractère c"""
        if noeud is None:
            return ArbreBinaire(c, None, None)

        if c == noeud.cle:
            return noeud
        if self.car(c,i) == 0 :
            nouveau_D = self.duplique(noeud.droite)
            return ArbreBinaire(noeud.cle, self._ajout(c , i+1 , noeud.gauche), nouveau_D)
        
        if self.car(c,i) == 1 :
            nouveau_G = self.duplique(noeud.gauche)
            return ArbreBinaire(noeud.cle, nouveau_G, self._ajout(c , i+1 , noeud.droite))

        return noeud # Dans le cas ou le caractère n'est pas trouvé



    def recherche(self, c): #c est un caractère
        """DST * str -> bool"""
        """Renvoie True si le caractère c est dans l'arbre, False sinon"""
        return self._recherche( self.racine, c , 0)
    
    def _recherche(self, noeud,  c , i):    #A est un arbre binaire
        """DST * ArbreBinaire * str * int -> bool"""
        """Renvoie True si le caractère c est dans l'arbre, False sinon"""
        if noeud is None: 
            return False
        if c == noeud.cle:    
            return True
        if self.car(c,i) == 0 :  
            return self._recherche(noeud.gauche , c , i+1)
        else :     
            return self._recherche(noeud.droite , c , i+1)
        
        

    def suppression(self, c): #c est un caractère
        """DST * str -> ArbreBinaire"""
        """Supprime le caractère c de l'arbre binaire"""
        return self._suppression(self.racine, c , 0)
    

    def _suppression(self, noeud , c , i): # CBinaire est un caractère binaire, exemple : '0101'
        """DST * ArbreBinaire * str * int -> ArbreBinaire"""
        """Supprime le caractère c de l'arbre binaire"""
        if noeud is None:   #Si l'arbre est vide
            return None
        
        if c == noeud.cle:      #Si le caractère est trouvé, on verifie tous les cas
            #cas si on est sur la racine
            if noeud.gauche is None and noeud.droite is None and self.racine.cle == noeud.cle and self.racine.gauche is None and self.racine.droite is None:
                return None
            if noeud.gauche is None and self.racine.cle == noeud.cle and self.racine.gauche == noeud.gauche:
                return self.duplique(noeud.droite)
            
            if noeud.droite is None and self.racine.cle == noeud.cle and self.racine.droite == noeud.droite:
                return self.duplique(noeud.gauche)
            
            #cas hors de la racine
            if noeud.gauche is None and noeud.droite is None:
                return None
            if noeud.gauche is None:  
                return self.duplique(noeud.droite) 
            if noeud.droite is None:    
                return self.duplique(noeud.gauche)
            else:   #Si le noeud a deux fils
                noeud_min = self.noeud_min(noeud.droite)
                nouveau_G = self.duplique(noeud.gauche)
                return ArbreBinaire(noeud_min.cle, nouveau_G, self._suppression(noeud.droite,noeud_min.cle , i+1) )
            
        if self.car(c,i) == 0 :  
            nouveau_D = self.duplique(noeud.droite)
            return ArbreBinaire(noeud.cle, self._suppression(noeud.gauche , c , i+1), nouveau_D)
        else :#self.car(c,i) == 1:     
            nouveau_G = self.duplique(noeud.gauche)
            return ArbreBinaire(noeud.cle, nouveau_G, self._suppression(noeud.droite , c , i+1))



    def noeud_min(self, noeud ):    #noeud est un arbre binaire
        """DST * ArbreBinaire -> ArbreBinaire"""
        """Renvoie le noeud le plus à gauche, qui est le plus petit noeud de l'arbre binaire A"""
        cour = noeud  
        while (cour.gauche is not None): 
            cour = cour.gauche
        return cour
        

    def construction(self):
        """DST -> DST"""
        """Construit l'arbre binaire à partir du dictionnaire"""
        for c in self.dico:
            self.racine = self.ajout(c)
        return self


    def visualiser_arbre(self):
        """DST -> Digraph"""
        """Renvoie un Digraph qui représente l'arbre binaire"""
        dot = Digraph()

        cpt = 0

        def generer_graphique(noeud):
            nonlocal cpt
            if noeud is not None:
                dot.node(str(noeud.cle))
                if noeud.gauche is not None:
                    dot.edge(str(noeud.cle), str(noeud.gauche.cle) , label = "0" , fontsize="10")
                    generer_graphique(noeud.gauche)
                else:
                    cpt += 1
                    dot.node(f"empty_{cpt}", shape="point", fillcolor="white" , width="0.5")
                    dot.edge(str(noeud.cle), f"empty_{cpt}" , label = "0" , fontsize="10")
                if noeud.droite is not None:
                    dot.edge(str(noeud.cle), str(noeud.droite.cle) , label = "1" , fontsize="10" )
                    generer_graphique(noeud.droite)
                else:
                    cpt += 1
                    dot.node(f"empty_{cpt}", shape="point", fillcolor="white" , width="0.5")
                    dot.edge(str(noeud.cle), f"empty_{cpt}" , label = "1" , fontsize="10")

        generer_graphique(self.racine)
        return dot


    def afficher_arbre(self , arbre, niveau=0):
        if arbre is not None:
            self.afficher_arbre(arbre.droite, niveau + 1)
            if niveau > 0:
                print('   ' * (niveau - 1) + '|--', end='')
            print(str(arbre.cle))
            self.afficher_arbre(arbre.gauche, niveau + 1)