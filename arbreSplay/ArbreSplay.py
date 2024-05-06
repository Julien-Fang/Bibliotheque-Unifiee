from graphviz import Digraph

class ArbreBinaire:
    def __init__(self, cle, gauche=None, droite=None):
        self.cle = cle
        self.gauche = gauche
        self.droite = droite

class ArbreSplay:
    def __init__(self):
        self.racine = None
    def _duplique(self,noeud) -> 'ArbreSplay':
        '''ArbreSplay * ArbreBinaire-> ArbreSplay'''
        '''Crée une copie de l'arbre Splay.'''
        if noeud is None:
            return None
        else:
            return ArbreBinaire(noeud.cle, self._duplique(noeud.gauche), self._duplique(noeud.droite))
    #AJOUT
    def ajout_liste(self, cles : list) -> 'ArbreSplay':
        '''ArbreSplay * int list -> ArbreSplay'''
        '''Ajoute une liste de clés dans l'arbre splay.'''
        splay = self
        for cle in cles:
            splay = splay.ajout(cle)
        return splay

    def ajout(self, cle : int) -> 'ArbreSplay':
        '''ArbreSplay * int -> ArbreSplay'''
        '''Ajoute une clé dans l'arbre splay.'''
        splay = ArbreSplay()
        splay.racine = self._duplique(self.racine)
        splay.racine = splay._ajout(splay.racine, cle)
        return splay
        
    def _ajout(self, noeud : ArbreBinaire, cle : int) -> 'ArbreBinaire':
        '''ArbreSplay * ArbreBinaire * int -> ArbreBinaire'''
        '''Ajoute une clé dans l'arbre binaire de recherche et renvoie l'arbre résultant.'''
        if noeud is None:
            return ArbreBinaire(cle)
        elif cle == noeud.cle:
            return noeud
        elif cle < noeud.cle:
            nouveauGauche = self._ajout(noeud.gauche, cle)
            nouveauNoeud = ArbreBinaire(noeud.cle, nouveauGauche, noeud.droite)
        else:
            nouveauDroite = self._ajout(noeud.droite, cle)
            nouveauNoeud = ArbreBinaire(noeud.cle, noeud.gauche, nouveauDroite)
        return self._splay(nouveauNoeud, cle)
    #SUPPRESSION
    def supprime(self, cle : int) -> 'ArbreSplay':
        '''ArbreSplay * int -> ArbreSplay'''
        '''Supprime une clé de l'arbre splay.'''
        splay = ArbreSplay()
        splay.racine = self._duplique(self.racine)
        splay.racine = splay._supprime(splay.racine, cle)
        return splay
        
    def _supprime(self, noeud : ArbreBinaire, cle : int) -> 'ArbreBinaire':
        '''ArbreSplay * ArbreBinaire * int -> ArbreBinaire'''
        '''Supprime une clé de l'arbre binaire de recherche et renvoie l'arbre résultant.'''
        if noeud is None:
            return noeud
        elif cle < noeud.cle:
            nouveauGauche = self._supprime(noeud.gauche, cle)
            nouveauNoeud = ArbreBinaire(noeud.cle, nouveauGauche, noeud.droite)
        elif cle > noeud.cle:
            nouveauDroite = self._supprime(noeud.droite, cle)
            nouveauNoeud = ArbreBinaire(noeud.cle, noeud.gauche, nouveauDroite)
        else:
            if noeud.gauche is None:
                return noeud.droite
            elif noeud.droite is None:
                return noeud.gauche
            
            min_noeud = self._min_noeud(noeud.droite)
            nouveauNoeud = ArbreBinaire(min_noeud.cle, noeud.gauche, self._supprime(noeud.droite, min_noeud.cle))
        return nouveauNoeud
    
    #RECHERCHE
    def recherche(self, cle : int) -> (bool, 'ArbreSplay'):
        '''ArbreSplay * int -> bool * ArbreSplay'''
        '''Recherche une clé dans l'arbre splay et renvoie un booléen indiquant si la clé est présente et l'arbre résultant.'''
        splay = ArbreSplay()
        splay.racine = self._duplique(self.racine)
        splay.racine = splay._splay(splay.racine, cle)
        exist = splay.racine is not None and splay.racine.cle == cle
        return exist, splay


    #     return noeud  # Si aucune rotation n'est effectuée
    def _recherche(self, noeud : ArbreBinaire, cle : int) -> 'ArbreBinaire':
        '''ArbreSplay * ArbreBinaire * int -> ArbreBinaire'''
        '''Recherche une clé dans l'arbre binaire de recherche et renvoie le noeud contenant la clé ou le noeud parent si la clé n'est pas présente.'''
        return self._splay(noeud, cle)
      
    #FONCTIONS UTILES / PRIMITIVES    
    
    def _splay(self, noeud : ArbreBinaire, cle : int) -> 'ArbreBinaire':
        '''ArbreSplay * ArbreBinaire * int -> ArbreBinaire'''
        '''Recherche une clé dans l'arbre binaire de recherche et renvoie le noeud contenant la clé ou le noeud parent si la clé n'est pas présente.'''
        
        if noeud is None or cle == noeud.cle:
            return noeud
        
        if cle < noeud.cle:
            if noeud.gauche is not None:
                if cle < noeud.gauche.cle:
                    noeud.gauche.gauche = self._recherche(noeud.gauche.gauche, cle)
                    noeud = self._rotation_droite(noeud)
                elif cle > noeud.gauche.cle:
                    noeud.gauche.droite = self._recherche(noeud.gauche.droite, cle)
                    if noeud.gauche.droite is not None:
                        noeud.gauche = self._rotation_gauche(noeud.gauche)
                if noeud.gauche is not None:
                    return self._rotation_droite(noeud)
            else:
                return noeud
        else:
            if noeud.droite is not None:
                if cle < noeud.droite.cle:
                    noeud.droite.gauche = self._recherche(noeud.droite.gauche, cle)
                    if noeud.droite.gauche is not None:
                        noeud.droite = self._rotation_droite(noeud.droite)
                elif cle > noeud.droite.cle:
                    noeud.droite.droite = self._recherche(noeud.droite.droite, cle)
                    noeud = self._rotation_gauche(noeud)
                if noeud.droite is not None:
                    return self._rotation_gauche(noeud)
            else:
                return noeud  

    def _rotation_gauche(self, noeud : ArbreBinaire) -> 'ArbreBinaire':
        '''ArbreBinaire -> ArbreBinaire'''
        '''Effectue une rotation gauche sur l'arbre binaire de recherche et renvoie l'arbre résultant.'''
        y = noeud.droite
        noeud.droite = y.gauche
        y.gauche = noeud
        return y

    def _rotation_droite(self, noeud : ArbreBinaire) -> 'ArbreBinaire':
        '''ArbreBinaire -> ArbreBinaire'''
        '''Effectue une rotation droite sur l'arbre binaire de recherche et renvoie l'arbre résultant.'''
        x = noeud.gauche
        noeud.gauche = x.droite
        x.droite = noeud
        return x

    def _min_noeud(self, noeud : ArbreBinaire) -> 'ArbreBinaire':
        '''ArbreBinaire -> ArbreBinaire'''
        '''Renvoie le noeud contenant la clé minimale de l'arbre binaire de recherche.'''
        if noeud is None or noeud.gauche is None:
            return noeud
        return self._min_noeud(noeud.gauche)
    
    def visualiser_arbre(self):
        '''ArbreSplay -> dot'''
        '''Affiche l'arbre binaire'''
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