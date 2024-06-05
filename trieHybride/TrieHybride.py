from graphviz import Digraph

class TrieH:
    def __init__(self , c , inf, eq , sup, v=None ):
        self.c = c
        self.inf = inf
        self.eq = eq
        self.sup = sup
        self.v = v
        
        
class TrieHybride:
    def __init__(self):
        self.racine = None
    
    def lg(self , mot):
        """TH * str -> int"""
        """Retourne la longueur d'un mot"""
        return len(mot)

    def prem(self , mot):
        """TH * str -> str"""
        """Retourne le premier caractère d'un mot"""
        if len(mot) == 0:
            return None
        return mot[0]
    
    def reste(self , mot):
        """TH * str -> str"""
        """Retourne le reste d'un mot sans le premier caractère"""
        return mot[1:]
    
    def duplique(self, A):
        """TH * TrieH -> TrieH"""
        """Duplique un arbre hybride"""
        if A is None:
            return None
        else:
            return TrieH(A.c, self.duplique(A.inf), self.duplique(A.eq), self.duplique(A.sup), A.v)


    def ajout(self, mot, A , v):
        """TH * str * TrieH * int -> TrieH"""
        """Ajoute un mot dans un arbre hybride"""

        if A is None:
            if self.lg(mot) == 1:
                return TrieH(self.prem(mot) , None , None , None , v)
            else:
                return TrieH(self.prem(mot) , None , self.ajout(self.reste(mot), None , v) , None , None)
        
        if self.lg(mot) == 1 :
            n_Inf = self.duplique(A.inf)
            n_Eq = self.duplique(A.eq)
            n_Sup = self.duplique(A.sup)
            return TrieH(A.c , n_Inf , n_Eq , n_Sup , v) 

        else:
            p = self.prem(mot)

            if p == None:
                return A
            if p < A.c:
                # A.inf = self.ajout( mot , A.inf , v)
                n_Eq = self.duplique(A.eq)
                n_Sup = self.duplique(A.sup)
                return TrieH(A.c , self.ajout( mot , A.inf , v) , n_Eq , n_Sup , A.v)
            if p > A.c:
                #print("sup")
                # A.sup = self.ajout( mot , A.sup , v)
                n_Inf = self.duplique(A.inf)
                n_Eq = self.duplique(A.eq)
                return TrieH(A.c , n_Inf , n_Eq , self.ajout( mot , A.sup , v) , A.v)
                #return TrieH(A.c , A.inf , A.eq , self.ajout( mot , A.sup , v) , A.v)
            n_Inf = self.duplique(A.inf)
            n_Sup = self.duplique(A.sup)
            return TrieH(A.c , n_Inf , self.ajout( self.reste(mot) , A.eq , v) , n_Sup , A.v)



    # recherche un mot dans le trie hybride
    def recherche(self, mot, A):
        """TH * str * TrieH -> bool"""
        """Recherche un mot dans un arbre hybride et retourne True si le mot est trouvé, False sinon"""
        if A is None:
            return False
        if self.lg(mot) == 1 and A.c == mot and A.v is not None:
            return True
        p = self.prem(mot)
        if p < A.c:
            return self.recherche(mot, A.inf)
        elif p > A.c:
            return self.recherche(mot, A.sup)
        else:
            return self.recherche(self.reste(mot), A.eq)
        
        
    def suppression(self, mot, noeud):
        """TH * str * TrieH -> TrieH"""
        """Supprime un mot dans un arbre hybride"""
        res = noeud
        if noeud is None:
            return None
        p = self.prem(mot)
        if p < noeud.c:
            n_Eq = self.duplique(noeud.eq)
            n_Sup = self.duplique(noeud.sup)
            res = TrieH(noeud.c, self.suppression(mot, noeud.inf), n_Eq, n_Sup, noeud.v)
            
        elif p > noeud.c:
            n_Inf = self.duplique(noeud.inf)
            n_Eq = self.duplique(noeud.eq)
            res = TrieH(noeud.c, n_Inf, n_Eq, self.suppression(mot, noeud.sup), noeud.v)
            
        elif p == noeud.c:
            if self.lg(mot) == 1:
                if noeud.v is not None:
                    noeud.v = None
                    
            else:
                n_Inf = self.duplique(noeud.inf)
                n_Sup = self.duplique(noeud.sup)
                res = TrieH(noeud.c, n_Inf, self.suppression(self.reste(mot), noeud.eq), n_Sup, noeud.v)

        # Cas de suppression de la racine
        if noeud.c == self.racine.c and noeud.eq is None and noeud.inf is None and noeud.sup is None and noeud.v is None and self.racine.eq == noeud.eq and self.racine.inf == noeud.inf and self.racine.sup == noeud.sup and self.racine.v == noeud.v:
            return None

        # Cas de suppression hors de la racine
        if self.prem(mot) == res.c and res.eq is None and res.inf is None and res.sup is None and res.v is None:
            return None
            
        if res.inf is None and res.eq is None and res.sup is None and res.v is None:
            return None
        
        if res.inf is not None and res.eq is None and res.sup is not None:
            return self.Fusion(res.inf, res.sup)
  
        if res.inf is not None and res.eq is None and res.sup is None:
            return res.inf 
        if res.inf is None and res.eq is None and res.sup is not None:
            return res.sup  
        return res 





    # Fusionner deux arbres
    def Fusion(self, A, B): 
        """TH * TrieH * TrieH -> TrieH"""
        """Fusionne deux arbres hybrides"""
        if A is None:
            return B
        if B is None:
            return A
        if A is not None and B is not None:
            if A.c < B.c:
                n_Inf = self.duplique(A.inf)
                n_Eq = self.duplique(A.eq)
                return TrieH(A.c, n_Inf, n_Eq, self.Fusion(A.sup, B), A.v)
                                
            if A.c > B.c:
                n_Sup = self.duplique(B.sup)
                n_Eq = self.duplique(B.eq)
                return TrieH(B.c, self.Fusion(A, B.inf), n_Eq, n_Sup, B.v)
               
            if A.c == B.c:
                n_SupA = self.duplique(A.sup)
                n_InfA = self.duplique(A.inf)
                return TrieH(A.c, n_InfA, self.Fusion(A.eq, B.eq), n_SupA, A.v)
                
    

       
    def visualiser_arbre(self):
        dot = Digraph()
        fontsize = "10"

        def generer_graphique(A, dot=dot):
            if A is not None:
                dot.node(str(id(A)), label=f"{A.c} {({str(A.v)}) if A.v is not None else ''}")

                if A.inf is not None:
                    dot.node(str(id(A.inf)), label=f"{A.inf.c} (Inf)")
                    dot.edge(str(id(A)), str(id(A.inf)) , label="Inf", fontsize=fontsize )
                    generer_graphique(A.inf)

                if A.eq is not None:
                    dot.node(str(id(A.eq)), label=f"{A.eq.c} (Eq)")
                    dot.edge(str(id(A)), str(id(A.eq)) , label="Eq", fontsize=fontsize )
                    generer_graphique(A.eq)

                if A.sup is not None:
                    dot.node(str(id(A.sup)), label=f"{A.sup.c} (Sup)")
                    dot.edge(str(id(A)), str(id(A.sup)) , label="Sup", fontsize=fontsize )
                    generer_graphique(A.sup)

        generer_graphique(self.racine)
        return dot

