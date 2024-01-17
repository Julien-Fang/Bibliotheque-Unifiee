from Uint128 import Uint128


class Node:
    def __init__(self, key: Uint128) -> None:
        self.key = key
        self.left = None
        self.right = None


class BSTree:
    def __init__(self) -> None:
        self.root = None

    def isEmpty(self) -> bool:
        return self.root is None

    def search(self, key: Uint128) -> bool:
        current = self.root

        while current:
            if Uint128.inf(key, current.key):
                current = current.left
            elif Uint128.egal(key, current.key):
                return True
            else:
                current = current.right
        return False

    def insert(self, key: Uint128) -> bool:
        if self.isEmpty():
            self.root = Node(key)
            return True
        else:
            current = self.root
            while True:
                if Uint128.inf(key, current.key):
                    if current.left is None:
                        current.left = Node(key)
                        return True
                    else:
                        current = current.left
                elif Uint128.egal(key, current.key):
                    return False
                else:
                    if current.right is None:
                        current.right = Node(key)
                        return True
                    else:
                        current = current.right

    def inorderTraversal(self) -> list[Uint128]:
        result = []

        def inorder(node: Node) -> None:
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)

        inorder(self.root)
        return result

    def balance(self) -> None:
        keys = self.inorderTraversal()
        self.root = None
        self._build_balanced(keys, 0, len(keys) - 1)

    def _build_balanced(self, keys: list[Uint128], start: int, end: int) -> None:
        if start > end:
            return None

        mid = (start + end) // 2
        self.insert(keys[mid])
        self._build_balanced(keys, start, mid - 1)
        self._build_balanced(keys, mid + 1, end)
