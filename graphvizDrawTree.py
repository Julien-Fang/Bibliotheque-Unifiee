#graphviz
from graphviz import Digraph

##  AVL Tree, Splay Tree, ..?
def draw_tree(racine):
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
    
    traverse(racine)
    return dot

## other tree ?
#...