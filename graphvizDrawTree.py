#graphviz
from graphviz import Digraph

##  AVL Tree, Splay Tree, ..?
def draw_tree(root):
    dot = Digraph()
    
    def traverse(node):
        if node is None:
            return

        dot.node(str(node.key), str(node.key))
        
        if node.left is not None:
            dot.edge(str(node.key), str(node.left.key), label="L", style="dashed")
            traverse(node.left)
        
        if node.right is not None:
            dot.edge(str(node.key), str(node.right.key), label="R", style="solid")
            traverse(node.right)
    
    traverse(root)
    return dot

## other tree ?
#...