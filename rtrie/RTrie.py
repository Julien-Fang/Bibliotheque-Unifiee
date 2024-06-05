from graphviz import Digraph

class rtrie:
    def __init__(self, c , v = None , enfant = [None]*26 ): # c : caractere , v : valeur , enfant : liste des enfants
        self.c = c
        self.v = v
        self.enfants = enfant
        
        
class RTrie:
    def __init__(self):
        self.racine = [None]*26
    
    def prem(self , mot): #retourne le caractere en int
        """RTrie * str -> int"""
        """Retourne la position du premier caractere du mot dans l'alphabet."""
        res = ord(mot[0])
        return res-97

    def reste(self , mot):
        """RTrie * str -> str"""
        """Retourne le reste du mot sans le premier caractere."""
        return mot[1:]


    def EnfantSauf(self, A, i):
        """RTrie * rtrie * int -> rtrie[]"""
        """Retourne la liste des enfants de A sauf celui d'indice i."""
        if A is None:
            return []
        res = []

        for cpt in range(len(A.enfants)):
            if cpt == i:
                res.append(None)
            else:
                res.append(self.duplique(A.enfants[cpt]))
        return res



    def SousArbre(self, A, i):
        """RTrie * rtrie * int -> rtrie"""
        """Renvoie une copie du i-eme sous arbre de A"""
        if A.enfants[i] is None :
            return None
        return self.duplique(A.enfants[i])


    def R_Trie(self, c, v, i , L , A): # i : entier , L : liste , A : R-Trie
        """RTrie * str * int * int * rtrie[] * rt -> rtrie"""
        """ Renvoie le trie construit a partir de L en inserant A a la i-eme position,
            en ajoutant la lettre c comme cle et la valeur v
        """
        #Pas besoin de dupliquer L car elle est deja dupliquee dans la methode EnfantSauf
        res = rtrie(c, v)
        res.enfants = L
        res.enfants[i] = A
        return res
    

        
    def duplique(self,A):
        """RTrie * rtrie -> rtrie"""
        """Renvoie une copie de A."""
        if A is None :
            return None
        else:
            res = rtrie(A.c, A.v)
            res.enfants = [None]*26
            for i in range(len(A.enfants)):
                res.enfants[i] = self.duplique(A.enfants[i])
            return res




    def ajout(self, c, v ) : # c : cle, v : valeur
        """RTrie * str * RTrie * -> rtrie"""
        """Ajoute un mot dans l'arbre R-Trie."""
        p = self.prem(c)
        self.racine[p] = self._ajout(c, self.racine[p], v)
        return self.racine



    def _ajout(self, c , A , v ) : # c : cle , A : R-Trie , v : valeur
        """RTrie * str * rtrie * -> rtrie"""
        """Ajoute un mot dans l'arbre R-Trie."""
        if A is None :
            A = rtrie(c)
            
        if len(c) == 1 :
            A.v = v
            return A
        suivant = self.reste(c)[0]
        psuiv = self.prem(suivant)
        return self.R_Trie(c[0], A.v, psuiv, self.EnfantSauf(A, psuiv), self._ajout(self.reste(c),self.SousArbre(A,psuiv),v))


    def recherche(self, mot):
        """RTrie * str -> bool"""
        """Recherche un mot dans l'arbre R-Trie."""
        if len(mot) == 0:
            return False
        p = self.prem(mot)
        return self._recherche(mot, self.racine[p])
    

    def _recherche(self, mot, noeud):
        """RTrie * str * rtrie -> bool"""
        """Recherche un mot dans l'arbre R-Trie."""
        if noeud is None:
            return False

        if len(mot) == 1 and noeud.c == mot : # Si nous sommes à la fin du mot et il contient une valeur 
            return noeud.v is not None
        
        if len(mot) == 1 and noeud.c != mot : # Si nous sommes à la fin du mot et il ne contient pas de valeur
            return False

        suivant = self.reste(mot)[0]
        psuiv = self.prem(suivant)
        if noeud.c == mot[0]:
            return self._recherche(self.reste(mot), self.SousArbre(noeud, psuiv))
        else:
            return False



    def suppression(self, mot):
        """RTrie * str -> rtrie"""
        """Supprime un mot de l'arbre R-Trie."""
        p = self.prem(mot)
        self.racine[p] = self._suppression(mot, self.racine[p])
        return self.racine
    

    def _suppression(self, mot, noeud):
        """RTrie * str * rtrie -> rtrie"""
        """Supprime un mot de l'arbre R-Trie."""
        res = noeud
        if res is None:
            return None 
        
        if len(mot) < 1:
            return res

        p = self.prem(mot)

        if len(mot) == 1:
            if res.v is not None and mot[0] == res.c:
                res.v = None
            else : 
               res.enfants[p] = self._suppression(self.reste(mot), res.enfants[p])    
                
        elif len(mot) > 1 :
            suivant = self.reste(mot)[0]
            psuiv = self.prem(suivant)
            res = self.R_Trie(mot[0], res.v,  psuiv, self.EnfantSauf(noeud, psuiv), self._suppression(self.reste(mot), self.SousArbre(noeud, psuiv)))
            
        # Cas où le noeud contient une valeur et n'a pas d'enfants
        if mot[0]==res.c and self.contientNone(res.enfants) and res.v is not None:
            return res
        
        # Cas de suppression de noeud inutile
        if mot[0]==res.c and self.contientNone(res.enfants):
            return None

        return res
    

    def contientNone(self, noeud):
        """RTrie * rtrie -> bool"""
        """Vérifie si un noeud contient que des None"""
        for enfant in noeud:
            if enfant is not None:
                return False
        return True



    def afficher_mots(self, noeud=None, mot=''):
        """Affiche tous les mots présents dans l'arbre R-Trie."""
        if noeud is None:
            noeud = self.racine

        for i, enfant in enumerate(noeud):
            if enfant is not None:
                # Si nous sommes à la fin d'un mot, affichons le mot
                if enfant.v is not None:
                    print(mot + chr(i + 97))
                # Sinon, continuons à parcourir l'arbre
                self.afficher_mots(enfant.enfants, mot + chr(i + 97))





    def visualiser_arbre(self):
        dot = Digraph()

        def generer_graphique(arbre, parent_label=''):
            if arbre is not None:
                for enfant in arbre:
                    if enfant is not None:
                        enfant_label = f"{enfant.c}_{id(enfant)}"
                        dot.node(enfant_label, label=f"{enfant.v if enfant.v is not None else ''}")
                        if parent_label is not None:
                            dot.edge(parent_label, enfant_label, label=f" {enfant.c}") 

                        generer_graphique(enfant.enfants, enfant_label)

        # Noeud racine
        dot.node("racine", label="")

        for enfant in self.racine:
            if enfant is not None:
               generer_graphique([enfant], "racine")

        return dot

