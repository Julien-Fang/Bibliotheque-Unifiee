from Uint128 import Uint128
from readKeys import readKeysFromCSV
import timeit
from collections import deque


class BinomialTree:
    def __init__(self, key: Uint128 = None):
        self.key = key
        self.parent = None
        self.children = deque()
        self.degree = 0

    def isEmpty(self) -> bool:
        return self.key is None

    # Merge two trees of the same degree
    def mergeBT(self, tree: 'BinomialTree') -> 'BinomialTree':
        if (self.degree != tree.degree):
            raise ValueError("Trees must have the same degree to be merged")
        if self.key.inf(tree.key):
            self.children.appendleft(tree)
            tree.parent = self
            self.degree += 1
            return self
        else:
            tree.children.appendleft(self)
            self.parent = tree
            tree.degree += 1
            return tree

    # Remove the root of the tree and return the heap of the remaining trees
    def decapitate(self) -> 'BinomialHeap':
        heap = BinomialHeap()
        for child in self.children:
            child.parent = None
            heap.trees.append(child)
        return heap

    # Convert a tree to a heap
    def toHeap(self) -> 'BinomialHeap':
        heap = BinomialHeap()
        heap.trees = [self]
        return heap


class BinomialHeap:
    def __init__(self):
        self.trees = deque()  # list of BinomialTrees

    def isEmpty(self) -> bool:
        return self is None or len(self.trees) == 0

    # Return the tree with the minimum degree
    def minDeg(self) -> 'BinomialTree':
        minDeg = self.trees[0]
        for tree in self.trees:
            if tree.degree < minDeg.degree:
                minDeg = tree
        return minDeg

    # Remove the tree with the minimum degree from the heap
    def _remains(self) -> None:
        minDeg = self.minDeg()
        self.trees.remove(minDeg)
        return self
    # Add a tree to the heap

    def _addMin(self, tree: 'BinomialTree') -> 'BinomialHeap':
        # tree is assumed to have the minimum degree
        self.trees.append(tree)
        return self

    # Merge heap with another heap follwing pseudo codes in class
    def mergeHeap(self, heap: 'BinomialHeap') -> 'BinomialHeap':
        return BinomialHeap._merge(self, heap, BinomialTree())

    def _merge(heap1: 'BinomialHeap', heap2: 'BinomialHeap', tree: 'BinomialTree') -> 'BinomialHeap':
        if tree.isEmpty():
            if heap1.isEmpty():
                return heap2
            if heap2.isEmpty():
                return heap1

            tree1 = heap1.minDeg()
            tree2 = heap2.minDeg()

            if (tree1.degree < tree2.degree):
                return BinomialHeap._addMin(BinomialHeap.mergeHeap(heap1._remains(), heap2), tree1)
            if (tree2.degree < tree1.degree):
                return BinomialHeap._addMin(BinomialHeap.mergeHeap(heap1, heap2._remains()), tree2)
            if (tree1.degree == tree2.degree):
                return BinomialHeap._merge(heap1._remains(), heap2._remains(), BinomialTree.mergeBT(tree1, tree2))
        else:
            if (heap1.isEmpty()):
                return BinomialHeap.mergeHeap(heap2, tree.toHeap())
            if (heap2.isEmpty()):
                return BinomialHeap.mergeHeap(heap1, tree.toHeap())

            tree1 = heap1.minDeg()
            tree2 = heap2.minDeg()

            if (tree.degree < tree1.degree and tree.degree < tree2.degree):
                return BinomialHeap._addMin(BinomialHeap.mergeHeap(heap1, heap2), tree)
            if (tree.degree == tree1.degree and tree.degree == tree2.degree):
                return BinomialHeap._addMin(BinomialHeap._merge(heap1._remains(), heap2._remains(), BinomialTree.mergeBT(tree1, tree2)), tree)
            if (tree.degree == tree1.degree and tree.degree < tree2.degree):
                return BinomialHeap._merge(heap1._remains(), heap2, BinomialTree.mergeBT(tree1, tree))
            if (tree.degree == tree2.degree and tree.degree < tree1.degree):
                return BinomialHeap._merge(heap1, heap2._remains(), BinomialTree.mergeBT(tree2, tree))

    # Insert by merging current heap with a heap containing only the key
    def insertKey(self, key: Uint128) -> None:
        result = BinomialHeap.mergeHeap(self, BinomialTree(key).toHeap())
        self.trees = result.trees

    # Construction of a heap from a list of keys
    def createBinomialHeap(self, list: list):
        for key in list:
            self.insertKey(key)

    def extractMin(self) -> Uint128:
        if self.isEmpty():
            return None
        minTree = self.trees[0]
        for tree in self.trees:
            if tree.key.inf(minTree.key):
                minTree = tree
        self.trees.remove(minTree)
        if (len(self.trees) == 0):
            self.trees = minTree.decapitate().trees
        else:
            self.trees = BinomialHeap.mergeHeap(
                self, minTree.decapitate()).trees
        return minTree.key

# CALCUL TEMPS D'EXECUTION ---------------------------------------------------


def exec_time_construction_binomial():
    # CONSTRUCTION
    nbJeu = 5
    nbCle = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]

    heap = BinomialHeap()
    avg_times_construction = []
    for i in nbCle:
        # List to store execution times for each run
        execution_times = []
        for j in range(1, nbJeu+1):
            path = './cles_alea/jeu_'+str(j)+'_nb_cles_'+str(i)+'.txt'
            print(path)
            listKeys = readKeysFromCSV(path)
            execution_times.append(timeit.timeit(
                lambda: heap.createBinomialHeap(listKeys), number=5))
        # Calculate the average execution time for the current dataset size
        avg_execution_time = sum(execution_times) / len(execution_times)
        avg_times_construction.append(avg_execution_time)
    print(avg_times_construction)
    return avg_times_construction


def exec_time_union_binomial():
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
            heap1 = BinomialHeap()
            heap1.createBinomialHeap(listKeys1)
            heap2 = BinomialHeap()
            heap2.createBinomialHeap(listKeys2)
            execution_times.append(timeit.timeit(
                lambda: heap1.mergeHeap(heap2), number=5))
        # Calculate the average execution time for the current dataset size
        avg_execution_time = sum(execution_times) / len(execution_times)
        avg_times_union.append(avg_execution_time)
    print(avg_times_union)
    return avg_times_union


def exec_time_insert_binomial():
    # Insert
    nbJeu = 5
    nbCle = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]

    heap = BinomialHeap()
    avg_times_insert = []
    for i in nbCle:
        # List to store execution times for each run
        execution_times = []
        for j in range(1, nbJeu+1):
            path = './cles_alea/jeu_'+str(j)+'_nb_cles_'+str(i)+'.txt'
            print(path)
            listKeys = readKeysFromCSV(path)
            heap.createBinomialHeap(listKeys[1:])
            execution_times.append(timeit.timeit(
                lambda: heap.insertKey(listKeys[0]), number=1000))
        # Calculate the average execution time for the current dataset size
        avg_execution_time = sum(execution_times) / len(execution_times)
        avg_times_insert.append(avg_execution_time)
    print(avg_times_insert)
    return avg_times_insert


def exec_time_extract_min_binomial():
    # Extract Min
    nbJeu = 5
    nbCle = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]

    heap = BinomialHeap()
    avg_times_extract_min = []
    for i in nbCle:
        # List to store execution times for each run
        execution_times = []
        for j in range(1, nbJeu+1):
            path = './cles_alea/jeu_'+str(j)+'_nb_cles_'+str(i)+'.txt'
            print(path)
            listKeys = readKeysFromCSV(path)
            heap.createBinomialHeap(listKeys)
            execution_times.append(timeit.timeit(
                lambda: heap.extractMin(), number=100))
        # Calculate the average execution time for the current dataset size
        avg_execution_time = sum(execution_times) / len(execution_times)
        avg_times_extract_min.append(avg_execution_time)
    print(avg_times_extract_min)
    return avg_times_extract_min
