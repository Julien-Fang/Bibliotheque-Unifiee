from graphviz import Digraph

class ArbreBinaire:
    def __init__(self,cle =None , gauche = None, droite = None):
        self.cle = cle
        self.gauche = gauche
        self.droite = droite
        
class TrieBinaire :
    def __init__(self, dico , c = None):
        self.dico = dico  # Exemple : dico = {'a':'01','b':'11','c':'00','d':'10'}
        if c is None :  #On suppose que c est un caractère de l'alphabet 
            self.racine = None
        else :  
            self.racine = ArbreBinaire(c)

    def car(self, c , i):
        """TrieBin * str * int -> int/None"""
        """Renvoie le i-ème caractère de l'encodage de c, lorsque c existe dans le dictionnaire, None sinon."""
        for k , v in self.dico.items():
            if k == c and len(v)-1 >= i:
                res= v[i]
                return int(res)
        return None

    def ajout(self, c):
        """TrieBin * str -> ArbreBinaire"""
        """Renvoie  l'arbre binaire résultant de l'insertion de c"""
        return self._ajout(c , 0, self.racine)
    

    def duplique(self, A):
        """TrieBin * ArbreBinaire -> ArbreBinaire/None"""
        """Renvoie une copie de l'arbre A, None si A est vide"""
        if A is None:
            return None
        return ArbreBinaire(A.cle, self.duplique(A.gauche), self.duplique(A.droite))
    

    def _ajout(self , c, i , A):
        """"TrieBin * str * int * ArbreBinaire -> ArbreBinaire"""
        """Renvoie le trie binaire en ajoutant le caractère c à l'arbre A, et i est l'indice du caractère c dans l'encodage binaire de c"""
        if A is None:
            return ArbreBinaire(c)
        if A.gauche is None and A.droite is None:
            if c == A.cle:
                return A
            else:
                return self.split( c, A.cle , i)
        if self.car(c, i) == 0:
           nouveau_D = self.duplique(A.droite)
           return ArbreBinaire(A.cle, self._ajout(c, i+1, A.gauche), nouveau_D)
        else:
            nouveau_G = self.duplique(A.gauche)
            return ArbreBinaire(A.cle, nouveau_G , self._ajout(c, i+1, A.droite))


    # Lorsqu'on ajoute un caractère qui à le meme prefixe qu'un autre caractère, on doit diviser le noeud en deux
    def split(self, c1 , c2, i): # c1 est un caractère deja dans l'arbre, c2 est un caractère à ajout
        """TrieBin * str * str * int -> ArbreBinaire"""
        """Retourne le trie binaire contenant c1 et c2"""
        if self.car(c1,i) == self.car(c2,i) == 0:
            return ArbreBinaire( '*' , self.split(c1, c2, i+1), None)
        if self.car(c1,i) == self.car(c2,i) == 1:
            return ArbreBinaire( '*' , None, self.split(c1, c2, i+1))
        if self.car(c1,i) == 0 and self.car(c2,i) == 1:
            return ArbreBinaire( '*' , ArbreBinaire(c1), ArbreBinaire(c2))
        if self.car(c1,i) == 1 and self.car(c2,i) == 0:
            return ArbreBinaire( '*' , ArbreBinaire(c2), ArbreBinaire(c1))
                

    def recherche(self, c):
        """TrieBin * str -> bool"""
        """Renvoie True si c est dans le trie binaire, False sinon"""
        return self._recherche(self.racine, c, 0)
    

    def _recherche(self, arbre, c, i):
        """TrieBin * ArbreBinaire * str * int -> bool"""
        """Renvoie True si c est dans le trie binaire, False sinon"""
        if arbre is None:
            return False
        if arbre.cle == c:
            return True
        if self.car(c, i) == 0:
            return self._recherche(arbre.gauche, c, i + 1)
        else:
            return self._recherche(arbre.droite, c, i + 1)


    def suppression(self, c):
        """TrieBin * str -> TrieBin"""
        """Renvoie le trie binaire après la suppression de c"""
        return self._suppression(self.racine, c, 0)
    

    def _suppression(self, noeud, c, i):
        """TrieBin * ArbreBinaire * str * int -> ArbreBinaire/None"""
        """Renvoie le trie binaire après la suppression de c"""
        res = noeud
        if noeud is None:
            return None
        if noeud.cle == c:
            if noeud.gauche is None and noeud.droite is None:
                return None
            if noeud.gauche is None:
                nouveau_DD = self.duplique(noeud.droite.droite)
                nouveau_DG = self.duplique(noeud.droite.gauche)
                res = ArbreBinaire(noeud.droite.cle, nouveau_DG, nouveau_DD)
                #res = ArbreBinaire(arbre.droite.cle, arbre.droite.gauche, arbre.droite.droite)
            if noeud.droite is None:
                nouveau_GG = self.duplique(noeud.gauche.gauche)
                nouveau_GD = self.duplique(noeud.gauche.droite)
                res = ArbreBinaire(noeud.gauche.cle, nouveau_GG, nouveau_GD)
                #res = ArbreBinaire(arbre.gauche.cle, arbre.gauche.gauche, arbre.gauche.droite)

        if self.car(c, i) == 0:
            nouveau_D = self.duplique(noeud.droite)
            res = ArbreBinaire(noeud.cle, self._suppression(noeud.gauche, c, i + 1), nouveau_D)
        elif self.car(c, i) == 1:
            nouveau_G = self.duplique(noeud.gauche)
            res = ArbreBinaire(noeud.cle, nouveau_G, self._suppression(noeud.droite, c, i + 1))

        # Remettre à jour l'arbre après la suppression
        if res.cle == '*' and res.gauche is None and res.droite is None and self.verifierEnfant(res) == 0:
            # Si l'arbre n'a pas d'enfant
            return None
        
        if res.cle == '*' and res.gauche is not None and res.droite is None and self.verifierEnfant(res) == 1:
            # Si l'arbre a un seul enfant, on peut le remonter 
            return res.gauche   #pas besoin de dupliquer car on a déjà dupliqué l'arbre avant
        
        if res.cle == '*' and res.gauche is None and res.droite is not None and self.verifierEnfant(res) == 1:
            # Si l'arbre a un seul enfant, on peut le remonter
            return res.droite   
        
        return res

    def verifierEnfant(self, noeud):
        """TrieBin * ArbreBinaire -> int"""
        """retourne le nombre d'enfants de l'arbre"""
        if noeud is None:
            return 0
        if noeud.gauche is None and noeud.droite is None:
            return 1
        return self.verifierEnfant(noeud.gauche) + self.verifierEnfant(noeud.droite)



    def construction(self):
        """TrieBin -> TrieBin"""
        """Renvoie le trie binaire construit à partir du dictionnaire"""
        for i in self.dico.keys():
            self.racine = self.ajout(i)
        return self



    def visualiser_arbre(self):
        dot = Digraph()
        compteur = 1

        def generer_graphique(noeud):
            nonlocal dot, compteur
            if noeud is not None:
                tmp = noeud.cle
                cle = str(noeud.cle)
                if '*' in cle:
                    cle = '*'+str(compteur)
                    compteur += 1
                dot.node(cle , label= cle if tmp != '*' else ' ' , width="0.5" if tmp == '*' else '')

            
                if noeud.gauche is not None:
                    if '*' in noeud.gauche.cle:
                        compteur += 1
                        node_g = '*'+str(compteur)
                        dot.edge(cle , node_g , label = "0" , fontsize="10")
                    else:
                        dot.edge(cle , str(noeud.gauche.cle) , label = "0" , fontsize="10")
                    generer_graphique(noeud.gauche)
                elif noeud.gauche is None and noeud.droite is not None:
                    compteur += 1
                    node_g = '*'+str(compteur)
                    dot.node(node_g , label= ' ' , width="0.5")
                    dot.edge(cle , node_g , label = "0" , fontsize="10")


                if noeud.droite is not None:
                    if '*' in noeud.droite.cle:
                        compteur += 1
                        node_d = '*'+str(compteur)
                        dot.edge(cle , node_d , label = "1" , fontsize="10")
                    else:
                        dot.edge(cle , str(noeud.droite.cle) , label = "1" , fontsize="10")
                    generer_graphique(noeud.droite)
                elif noeud.droite is None and noeud.gauche is not None:
                    compteur += 1
                    node_d = '*'+str(compteur)
                    dot.node(node_d , label= ' ' , width="0.5")
                    dot.edge(cle , node_d , label = "1" , fontsize="10")

        generer_graphique(self.racine)
        return dot


    def afficher_arbre(self , arbre, niveau=0):
        if arbre is not None:
            self.afficher_arbre(arbre.droite, niveau + 1)
            if niveau > 0:
                print('   ' * (niveau - 1) + '|--', end='')
            print(str(arbre.cle))
            self.afficher_arbre(arbre.gauche, niveau + 1)