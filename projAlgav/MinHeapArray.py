from Uint128 import Uint128
from readKeys import readKeysFromCSV
import timeit
import matplotlib.pyplot as plt


class MinHeapArray:
    def __init__(self):
        self.heap = [] # list of Uint128

    # Helper functions
    def _isHeap(self) -> bool: # check if the heap is a min heap
        n = len(self.heap)
        for i in range(0, n//2):
            left = 2*i + 1
            right = 2*i + 2
            if left < n and self.heap[left].inf(self.heap[i]):
                return False
            if right < n and self.heap[right].inf(self.heap[i]):
                return False
        return True
    
    def _parent(self, i: int) -> int:  # return parent's index
        # the floor division // rounds the result down to the nearest whole number
        return (i-1)//2

    # moves down the key at index i until it satisfies the heap property
    def _minHeapify(self, i: int) -> None:  
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(self.heap) and Uint128.inf(self.heap[left], self.heap[smallest]):
            smallest = left
        if right < len(self.heap) and Uint128.inf(self.heap[right], self.heap[smallest]):
            smallest = right
        if smallest != i:
            self.heap[i], self.heap[smallest] = (self.heap[smallest], self.heap[i])
            self._minHeapify(smallest)

    # Ajout
    def insertKey(self, key: Uint128) -> None:
        self.heap.append(key)  # add the new key
        i = len(self.heap) - 1
        # moves it up (swap with parent) until it satisfies the heap property
        while (i != 0) and Uint128.inf(self.heap[i], self.heap[self._parent(i)]):
            self.heap[i], self.heap[self._parent(i)] = (
                self.heap[self._parent(i)], self.heap[i])
            i = self._parent(i)

    # AjoutIteratifs
    def insertKeyList(self, list: list) -> None:
        for key in list:
            self.insertKey(key)

    # SupprMin
    def extractMin(self) -> Uint128:
        if self.heap[0] is None:
            return None
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        root = self.heap.pop()
        self._minHeapify(0)
        return root.value

    # Construction
    def createMinHeap(self, list: list) -> None:
        self.heap = list
        n = len(self.heap)
        # opti = loop half : nodes, not leaves. second half contains leaves(=node without children)
        for i in range(n//2, -1, -1):
            self._minHeapify(i)

    # Union
    def union(heap1: 'MinHeapArray', heap2: 'MinHeapArray') -> 'MinHeapArray':
        newHeap = MinHeapArray()
        data = heap1.heap + heap2.heap
        newHeap.createMinHeap(data)
        return newHeap


# CALCUL TEMPS D'EXECUTION ---------------------------------------------------
def exec_time_construction_array():
    # CONSTRUCTION
    nbJeu = 5
    nbCle = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]

    heap = MinHeapArray()
    avg_times_construction = []
    for i in nbCle:
        # List to store execution times for each run
        execution_times = []
        for j in range(1, nbJeu+1):
            path = './cles_alea/jeu_'+str(j)+'_nb_cles_'+str(i)+'.txt'
            print(path)
            listKeys = readKeysFromCSV(path)
            execution_times.append(timeit.timeit(
                lambda: heap.createMinHeap(listKeys), number=5))
        # Calculate the average execution time for the current dataset size
        avg_execution_time = sum(execution_times) / len(execution_times)
        avg_times_construction.append(avg_execution_time)
    print(avg_times_construction)
    return avg_times_construction


def exec_time_ajout_iteratif_array():
    # AJOUT ITERATIF
    nbJeu = 5
    nbCle = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]

    avg_times_insertKeyList = []
    for i in nbCle:
        # List to store execution times for each run
        execution_times = []
        for j in range(1, nbJeu+1):
            heap = MinHeapArray()
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


def exec_time_union_array():
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
            heap1 = MinHeapArray()
            heap1.createMinHeap(listKeys1)
            heap2 = MinHeapArray()
            heap2.createMinHeap(listKeys2)
            execution_times.append(timeit.timeit(
                lambda: heap1.union(heap2), number=5))
        # Calculate the average execution time for the current dataset size
        avg_execution_time = sum(execution_times) / len(execution_times)
        avg_times_union.append(avg_execution_time)
    print(avg_times_union)
    return avg_times_union


def exec_time_insert_array():
    # Insert
    nbJeu = 5
    nbCle = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]

    heap = MinHeapArray()
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


def exec_time_extract_min_array():
    # Extract Min
    nbJeu = 5
    nbCle = [1000, 5000, 10000, 20000, 50000, 80000, 120000, 200000]

    heap = MinHeapArray()
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
    exec_time_construction_array()
    exec_time_ajout_iteratif_array()
    exec_time_union_array()
    exec_time_insert_array()
    exec_time_extract_min_array()