from graphviz import Digraph

class TasMin:
    def __init__(self):
        self.tas = [] 

    # Ajout
    
    def ajout_liste(self, cles: list) -> 'TasMin':
        '''Tas * list -> Tas'''
        '''Ajoute une liste de clés dans le tas et retourne un nouveau tas'''
        nouveauTas = self
        for cle in cles:
            nouveauTas = nouveauTas.ajout(cle)
        return nouveauTas
            
    def ajout(self, cle : int) -> 'TasMin':
        '''Tas * int -> Tas'''
        '''Ajoute une clé dans le tas et retourne un nouveau tas'''
        nouveauTas = TasMin()
        nouveauTas.tas = self.tas.copy()
        nouveauTas.tas = nouveauTas._ajout(cle)
        return nouveauTas
    
    def _ajout(self, cle : int) -> list:
        '''Tas * int -> list'''
        '''Ajoute une clé dans le tas et retourne le tas modifié'''
        self.tas.append(cle)  # add the new key
        i = len(self.tas) - 1
        # moves it up (swap with parent) until it satisfies the tas property
        while (i != 0) and self.tas[i] < self.tas[self._parent(i)]:
            self.tas[i], self.tas[self._parent(i)] = (
                self.tas[self._parent(i)], self.tas[i])
            i = self._parent(i)
        return self.tas

    # SupprMin
    def extractMin(self) -> (int, 'TasMin'):
        '''Tas -> (int * Tas)'''
        '''Retourne la clé minimum et le tas sans le minimum '''
        if self.tas[0] is None:
            return None
        nouveauTas = TasMin()
        nouveauTas.tas = self.tas.copy()
        nouveauTas.tas[0], nouveauTas.tas[-1] = nouveauTas.tas[-1], nouveauTas.tas[0]
        racine = nouveauTas.tas.pop()
        nouveauTas._heapify(0)
        return racine, nouveauTas

    # Construction
    def construction(self, cles: list) -> 'TasMin':
        '''Tas * list -> Tas'''
        '''Construit un tas à partir d'une liste de clés et retourne un nouveau tas'''
        self.tas = cles
        n = len(self.tas)
        # opti = loop half : nodes, not leaves. second half contains leaves(=node without children)
        for i in range(n//2, -1, -1):
            self._heapify(i)
        return self

    # Union
    def union(tas1: 'TasMin', tas2: 'TasMin') -> 'TasMin':
        '''Tas * Tas -> Tas'''
        '''Retourne un nouveau tas qui est l'union de deux tas'''
        nouveauTas = TasMin()
        valeurs = tas1.tas + tas2.tas
        nouveauTas.construction(valeurs)
        return nouveauTas
    
    
    
    # Helper functions
    def _est_tas(self) -> bool: 
        '''Tas -> bool'''
        '''Retourne True si le tas est un tas, False sinon'''
        n = len(self.tas)
        for i in range(0, n//2):
            gauche = 2*i + 1
            droite = 2*i + 2
            if gauche < n and self.tas[gauche] < self.tas[i]:
                return False
            if droite < n and self.tas[droite] < self.tas[i]:
                return False
        return True
    
    def _parent(self, i: int) -> int:  
        '''Tas * int -> int'''
        '''Retourne l'index du parent de l'élément à l'index i'''
        # the floor division // rounds the result down to the nearest whole number
        return (i-1)//2

    # moves down the key at index i until it satisfies the tas property
    def _heapify(self, i: int) -> None:  
        '''Tas * int -> None'''
        '''Modifie le tas pour satisfaire la propriété de tas'''
        min = i
        gauche = 2 * i + 1
        droite = 2 * i + 2
        if gauche < len(self.tas) and self.tas[gauche] < self.tas[min]:
            min = gauche
        if droite < len(self.tas) and self.tas[droite] < self.tas[min]:
            min = droite
        if min != i:
            self.tas[i], self.tas[min] = (self.tas[min], self.tas[i])
            self._heapify(min)
            
            
    def visualiser_arbre(self):
        '''Tas -> dot'''
        '''Affiche le tas'''
        dot = Digraph()
    
        def traverse(index):
            if index < len(self.tas):
                dot.node(str(self.tas[index]), str(self.tas[index]))
                
                gauche = 2 * index + 1
                droite = 2 * index + 2
                
                if gauche < len(self.tas):
                    dot.edge(str(self.tas[index]), str(self.tas[gauche]), label="L", style="dashed")
                    traverse(gauche)
                
                if droite < len(self.tas):
                    dot.edge(str(self.tas[index]), str(self.tas[droite]), label="R", style="solid")
                    traverse(droite)
        
        traverse(0)
        return dot
