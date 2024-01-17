from Uint128 import Uint128
from readKeys import readKeysFromCSV
import timeit
import matplotlib.pyplot as plt


class TreeNode:
    def __init__(self, key: Uint128):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

    def getMinChild(self) -> 'TreeNode':
        min_child = self
        if self.left and Uint128.inf(self.left.key, min_child.key):
            min_child = self.left
        if self.right and Uint128.inf(self.right.key, min_child.key):
            min_child = self.right
        return min_child


class MinHeapTree:
    def __init__(self):
        self.root = None
        self.len = 0

    # Helper functions
    
    # check if the heap is a min heap
    def _isHeap(self, node: 'TreeNode') -> bool: 
        if node is None:
            return True

        left = node.left
        right = node.right

        if left and Uint128.inf(left.key, node.key):
            return False

        if right and Uint128.inf(right.key, node.key):
            return False

        return self.isHeap(left) and self.isHeap(right)
    
    #moves down the key at index i until it satisfies the heap property
    def _minHeapify(self, node: 'TreeNode') -> None:  
        if node is None:
            return

        smallest = node
        left = node.left
        right = node.right

        if left and Uint128.inf(left.key, smallest.key):
            smallest = left

        if right and Uint128.inf(right.key, smallest.key):
            smallest = right

        if smallest != node:
            node.key, smallest.key = smallest.key, node.key
            self._minHeapify(smallest)

    def _lastParent(self, node: 'TreeNode', len: int) -> 'TreeNode': # return last parent node
        # Iterate all the bits except the leftmost 1 and the final bit
        # start from third to second last = ignore prefixe 0b and first/last bit
        for bit in bin(len)[3:-1]:
            # Choose side if 0=left, 1 = right           # if len = 9, bit(len) = 0b1001
            node = [node.left, node.right][int(bit)]
        return node

    def _lastNode(self) -> tuple[bool, 'TreeNode']: # return last node and side (0=left, 1=right)
        lastParent = self._lastParent(self.root, self.len)
        if lastParent.right:
            return 1, lastParent.right
        else:
            return 0, lastParent.left

    def _getKeyList(self, node, listKey, i=0): # return list of keys
        if not (node is None):
            if node.left:
                self._getKeyList(node.left, listKey, i+1)
            if node.right:
                self._getKeyList(node.right, listKey, i+1)
            listKey.append(node.key)
            if i == 0:
                return listKey

    # build heap from node
    def _buildHeap(self, node: 'TreeNode') -> None: 
        if node.left != None:
            self._buildHeap(node.left)
            if node.right != None:
                self._buildHeap(node.right)
            while ((node.left != None) | (node.right != None)):
                min = node.getMinChild()
                if min != node:
                    node.key, min.key = min.key, node.key
                    node = min
                else:
                    break

    # insert nodes in level order
    def _insertLevelOrder(self, parent: 'TreeNode', list: list, i: int, len: int) -> 'TreeNode': 
        if i >= len:
            return None
        root = TreeNode(list[i])
        root.parent = parent
        root.left = self._insertLevelOrder(root, list, 2*i+1, len)
        root.right = self._insertLevelOrder(root, list, 2*i+2, len)
        return root
    
    # Ajout
    def insertKey(self, key: Uint128) -> None: # add the new key at the end of the heap and move it up until it satisfies the heap property
        self.len += 1
        if self.len == 1:  # First node
            self.root = TreeNode(key)
            return
        lastParent = self._lastParent(self.root, self.len)
        # Use final bit to determine where child goes: (& = and bitwise) check if the last bit is 1
        if self.len & 1:
            lastParent.right = TreeNode(key)
            lastParent.right.parent = lastParent
            insertNode = lastParent.right
        else:
            lastParent.left = TreeNode(key)
            lastParent.left.parent = lastParent
            insertNode = lastParent.left

        while (insertNode != self.root) and Uint128.inf(insertNode.key, insertNode.parent.key):
            insertNode.key, insertNode.parent.key = insertNode.parent.key, insertNode.key
            insertNode = insertNode.parent

    # AjoutIteratifs
    def insertKeyList(self, key_list: list) -> None: # add keys one by one
        for key in key_list:
            self.insertKey(key)
    
    # SupprMin
    def extractMin(self) -> Uint128:    # swap root with last node, delete last node, minHeapify
        if self.root is None:
            return None
        min_key = self.root.key
        side, lastNode = self._lastNode()
        self.root.key = lastNode.key
        if side:
            lastNode.parent.right = None
        else:
            lastNode.parent.left = None
        lastNode = None
        self._minHeapify(self.root)
        self.len -= 1
        return min_key

    # Construction
    def createMinHeap(self, list: list) -> None:    # insert keys one by one to create a binary tree, then build heap
        n = len(list)
        self.root = self._insertLevelOrder(None, list, 0, n)
        self._buildHeap(self.root)
        self.len = n

    # Union
    def union(heap1: 'MinHeapTree', heap2: 'MinHeapTree') -> None: # create a new heap with keys from both heaps and create heap
        heap = MinHeapTree()
        array1 = heap1._getKeyList(heap1.root, [])
        array2 = heap2._getKeyList(heap2.root, [])
        heap.len = heap1.len + heap2.len
        data = array1 + array2
        heap.createMinHeap(data)
        return heap

# CALCUL TEMPS D'EXECUTION ---------------------------------------------------
def exec_time_construction_tree():
    # CONSTRUCTION
    nbJeu = 5
    nbCle = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]

    heap = MinHeapTree()
    avg_times_construction = []
    for i in nbCle:
        # List to store execution times for each run
        execution_times = []
        for j in range(1, nbJeu+1):
            path = './cles_alea/jeu_'+str(j)+'_nb_cles_'+str(i)+'.txt'
            print(path)
            listKeys = readKeysFromCSV(path)
            # heap2 = MinHeapTree()
            # heap2.root = heap2._insertLevelOrder(listKeys)
            execution_times.append(timeit.timeit(
                lambda: heap.createMinHeap(listKeys), number=5))
        # Calculate the average execution time for the current dataset size
        avg_execution_time = sum(execution_times) / len(execution_times)
        avg_times_construction.append(avg_execution_time)
    print(avg_times_construction)
    return avg_times_construction


def exec_time_ajout_iteratif_tree():
    # AJOUT ITERATIF
    nbJeu = 5
    nbCle = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]

    avg_times_insertKeyList = []
    for i in nbCle:
        # List to store execution times for each run
        execution_times = []
        for j in range(1, nbJeu+1):
            heap = MinHeapTree()
            path = './cles_alea/jeu_'+str(j)+'_nb_cles_'+str(i)+'.txt'
            print(path)
            listKeys = readKeysFromCSV(path)
            execution_times.append(timeit.timeit(
                lambda: heap.insertKeyList(listKeys), number=5))
        # Calculate the average execution time for the current dataset size
        avg_execution_time = sum(execution_times) / len(execution_times)
        avg_times_insertKeyList.append(avg_execution_time)
    print(avg_times_insertKeyList)
    return avg_times_insertKeyList


def exec_time_union_tree():
    # UNION
    nbJeu = 5
    nbCle = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]

    avg_times_union = []
    for i in nbCle:
        # List to store execution times for each run
        execution_times = []
        for j in range(1, nbJeu):
            path1 = './cles_alea/jeu_'+str(j)+'_nb_cles_'+str(i)+'.txt'
            path2 = './cles_alea/jeu_'+str(j+1)+'_nb_cles_'+str(i)+'.txt'
            print(path1, ' UNION ', path2)
            listKeys1 = readKeysFromCSV(path1)
            listKeys2 = readKeysFromCSV(path2)
            heap1 = MinHeapTree()
            heap1.createMinHeap(listKeys1)
            heap2 = MinHeapTree()
            heap2.createMinHeap(listKeys2)
            execution_times.append(timeit.timeit(
                lambda: MinHeapTree.union(heap1, heap2), number=5))
        # Calculate the average execution time for the current dataset size
        avg_execution_time = sum(execution_times) / len(execution_times)
        avg_times_union.append(avg_execution_time)
    print(avg_times_union)
    return avg_times_union


def exec_time_insert_tree():
    # Insert
    nbJeu = 5
    nbCle = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]

    heap = MinHeapTree()
    avg_times_insert = []
    for i in nbCle:
        # List to store execution times for each run
        execution_times = []
        for j in range(1, nbJeu+1):
            path = './cles_alea/jeu_'+str(j)+'_nb_cles_'+str(i)+'.txt'
            print(path)
            listKeys = readKeysFromCSV(path)
            heap.createMinHeap(listKeys[1:])
            execution_times.append(timeit.timeit(
                lambda: heap.insertKey(listKeys[0]), number=1000))
        # Calculate the average execution time for the current dataset size
        avg_execution_time = sum(execution_times) / len(execution_times)
        avg_times_insert.append(avg_execution_time)
    print(avg_times_insert)
    return avg_times_insert


def exec_time_extract_min_tree():
    # Extract Min
    nbJeu = 5
    nbCle = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]

    heap = MinHeapTree()
    avg_times_extract_min = []
    for i in nbCle:
        # List to store execution times for each run
        execution_times = []
        for j in range(1, nbJeu+1):
            path = './cles_alea/jeu_'+str(j)+'_nb_cles_'+str(i)+'.txt'
            print(path)
            listKeys = readKeysFromCSV(path)
            heap.createMinHeap(listKeys)
            execution_times.append(timeit.timeit(
                lambda: heap.extractMin(), number=100))
        # Calculate the average execution time for the current dataset size
        avg_execution_time = sum(execution_times) / len(execution_times)
        avg_times_extract_min.append(avg_execution_time)
    print(avg_times_extract_min)
    return avg_times_extract_min

if __name__ == '__main__' :
    exec_time_construction_tree()
    exec_time_ajout_iteratif_tree()
    exec_time_union_tree()
    exec_time_insert_tree()
    exec_time_extract_min_tree()