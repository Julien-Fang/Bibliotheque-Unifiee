from graphviz import Digraph

class ArbreBinaire:
    def __init__(self, cle, gauche=None, droite=None, hauteur=1):
        self.cle = cle
        self.gauche = gauche
        self.droite = droite
        self.hauteur = hauteur

class ArbreAVL:
    def __init__(self):
        self.racine = None
    
    def _duplique(self, noeud) -> 'ArbreBinaire':
        if noeud is None:
            return None
        else:
            duplique = ArbreBinaire(noeud.cle, self._duplique(noeud.gauche), self._duplique(noeud.droite))
            duplique.hauteur = noeud.hauteur
            return duplique
    
    def ajout_liste(self, cles: list) -> 'ArbreAVL':
        avl = self
        for cle in cles:
            avl = avl.ajout(cle)
        return avl
    
    def ajout(self, cle: int) -> 'ArbreAVL':
        avl = ArbreAVL()
        avl.racine = self._duplique(self.racine)
        avl.racine = avl._ajout(avl.racine, cle)
        return avl
    
    def _ajout(self, noeud: ArbreBinaire, cle: int) -> ArbreBinaire:
        if not noeud:
            return ArbreBinaire(cle)
        elif cle < noeud.cle:
            noeud.gauche = self._ajout(noeud.gauche, cle)
        else:
            noeud.droite = self._ajout(noeud.droite, cle)
        
        noeud.hauteur = 1 + max(self._hauteur(noeud.gauche), self._hauteur(noeud.droite))
        return self._equilibrage(noeud, cle)
    
    def supprime(self, cle: int) -> 'ArbreAVL':
        avl = ArbreAVL()
        avl.racine = self._duplique(self.racine)
        avl.racine = avl._supprime(avl.racine, cle)
        return avl
    
    def _supprime(self, noeud: ArbreBinaire, cle: int) -> ArbreBinaire:
        if not noeud:
            return noeud
        elif cle < noeud.cle:
            noeud.gauche = self._supprime(noeud.gauche, cle)
        elif cle > noeud.cle:
            noeud.droite = self._supprime(noeud.droite, cle)
        else:
            if noeud.gauche is None:
                temp = noeud.droite
                noeud = None
                return temp
            elif noeud.droite is None:
                temp = noeud.gauche
                noeud = None
                return temp
            
            min_noeud = self._min_noeud(noeud.droite)
            noeud.cle = min_noeud.cle
            noeud.droite = self._supprime(noeud.droite, noeud.cle)
        
        if noeud is None:
            return noeud
        
        noeud.hauteur = 1 + max(self._hauteur(noeud.gauche), self._hauteur(noeud.droite))
        return self._equilibrage(noeud, cle)
    
    def recherche(self, cle: int) -> (bool, 'ArbreBinaire'):
        return self._recherche(self.racine, cle)
    
    def _recherche(self, noeud: ArbreBinaire, cle: int) -> (bool, 'ArbreBinaire'):
        if noeud is None:
            return False, None
        elif cle < noeud.cle:
            return self._recherche(noeud.gauche, cle)
        elif cle > noeud.cle:
            return self._recherche(noeud.droite, cle)
        else:
            return True, noeud
    
    def hauteur(self) -> int:
        return self._hauteur(self.racine)
    
    def _hauteur(self, noeud: ArbreBinaire) -> int:
        if not noeud:
            return 0
        
        return noeud.hauteur
    
    def _min_noeud(self, noeud: ArbreBinaire) -> ArbreBinaire:
        if noeud is None or noeud.gauche is None:
            return noeud
        return self._min_noeud(noeud.gauche)
    
    def _equilibre(self, noeud: ArbreBinaire) -> int:
        if not noeud:
            return 0
        return self._hauteur(noeud.gauche) - self._hauteur(noeud.droite)
    
    def _equilibrage(self, noeud: ArbreBinaire, cle: int) -> ArbreBinaire:
        equilibrage = self._equilibre(noeud)
        if equilibrage > 1:
            if self._equilibre(noeud.gauche)>=0:
                return self._rotation_droite(noeud)
            else:
                noeud.gauche = self._rotation_gauche(noeud.gauche)
                return self._rotation_droite(noeud)
        elif equilibrage < -1:
            if  self._equilibre(noeud.droite)<=0:
                return self._rotation_gauche(noeud)
            else:
                noeud.droite = self._rotation_droite(noeud.droite)
                return self._rotation_gauche(noeud)
        return noeud
    
    def _rotation_gauche(self, noeud: ArbreBinaire) -> ArbreBinaire:
        y = noeud.droite
        T2 = y.gauche
        y.gauche = noeud
        noeud.droite = T2
        noeud.hauteur = 1 + max(self._hauteur(noeud.gauche), self._hauteur(noeud.droite))
        y.hauteur = 1 + max(self._hauteur(y.gauche), self._hauteur(y.droite))
        return y
    
    def _rotation_droite(self, noeud: ArbreBinaire) -> ArbreBinaire:
        y = noeud.gauche
        T3 = y.droite
        y.droite = noeud
        noeud.gauche = T3
        noeud.hauteur = 1 + max(self._hauteur(noeud.gauche), self._hauteur(noeud.droite))
        y.hauteur = 1 + max(self._hauteur(y.gauche), self._hauteur(y.droite))
        return y
    
    def visualiser_arbre(self):
        dot = Digraph()
    
        def traverse(noeud):
            if noeud is None:
                return
            dot.node(str(noeud.cle), str(noeud.cle))
            if noeud.gauche is not None:
                dot.edge(str(noeud.cle), str(noeud.gauche.cle), label="L", style="dashed")
                traverse(noeud.gauche)
            if noeud.droite is not None:
                dot.edge(str(noeud.cle), str(noeud.droite.cle), label="R", style="solid")
                traverse(noeud.droite)
        
        traverse(self.racine)
        return dot


