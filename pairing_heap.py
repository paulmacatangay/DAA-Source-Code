from typing import List, Optional, Tuple

class PairingHeapNode:
    def __init__(self, key: float, value: int):
        self.key = key
        self.value = value
        self.children: List['PairingHeapNode'] = []
        self.parent: Optional['PairingHeapNode'] = None

class PairingHeap:
    def __init__(self):
        self.root: Optional[PairingHeapNode] = None
        self.size = 0

    def insert(self, key: float, value: int) -> PairingHeapNode:
        """Insert a new node with the given key and value."""
        node = PairingHeapNode(key, value)
        self.root = self._meld(self.root, node)
        self.size += 1
        return node

    def delete_min(self) -> Optional[Tuple[float, int]]:
        """Remove and return the minimum key and its value."""
        if not self.root:
            return None
        result = (self.root.key, self.root.value)
        self.root = self._combine_pairs(self.root.children)
        self.size -= 1
        return result

    def decrease_key(self, node: PairingHeapNode, new_key: float):
        """Decrease the key of a given node."""
        if new_key > node.key:
            raise ValueError("New key must be smaller than current key")
        node.key = new_key
        if node == self.root:
            return
        # Remove node from its parent's children
        if node.parent:
            node.parent.children.remove(node)
            node.parent = None
        # Meld the subtree with the root
        self.root = self._meld(self.root, node)

    def _meld(self, h1: Optional[PairingHeapNode], h2: Optional[PairingHeapNode]) -> Optional[PairingHeapNode]:
        if not h1:
            return h2
        if not h2:
            return h1
        if h1.key < h2.key:
            h1.children.append(h2)
            h2.parent = h1
            return h1
        else:
            h2.children.append(h1)
            h1.parent = h2
            return h2

    def _combine_pairs(self, children: List[PairingHeapNode]) -> Optional[PairingHeapNode]:
        if not children:
            return None
        pairs = []
        for i in range(0, len(children), 2):
            if i + 1 < len(children):
                pairs.append(self._meld(children[i], children[i + 1]))
            else:
                pairs.append(children[i])
        result = pairs[-1]
        for i in range(len(pairs) - 2, -1, -1):
            result = self._meld(result, pairs[i])
        return result
