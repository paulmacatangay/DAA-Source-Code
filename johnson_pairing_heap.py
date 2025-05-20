import sys
from typing import List, Dict, Tuple, Optional
import heapq
from collections import defaultdict

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
        self.node_map: Dict[int, PairingHeapNode] = {}  # Maps vertex to node

    def insert(self, key: float, value: int) -> None:
        """Insert a new node into the heap."""
        new_node = PairingHeapNode(key, value)
        self.node_map[value] = new_node
        if self.root is None:
            self.root = new_node
        else:
            self.root = self._meld(self.root, new_node)
        self.size += 1

    def _meld(self, h1: PairingHeapNode, h2: PairingHeapNode) -> PairingHeapNode:
        """Meld two heaps together."""
        if h1 is None:
            return h2
        if h2 is None:
            return h1
        if h1.key > h2.key:
            h1, h2 = h2, h1
        h2.parent = h1
        h1.children.append(h2)
        return h1

    def delete_min(self) -> Tuple[float, int]:
        """Remove and return the minimum element."""
        if self.root is None:
            raise IndexError("Heap is empty")
        
        min_node = self.root
        del self.node_map[min_node.value]
        self.root = self._combine_pairs(min_node.children)
        self.size -= 1
        return min_node.key, min_node.value

    def _combine_pairs(self, nodes: List[PairingHeapNode]) -> Optional[PairingHeapNode]:
        """Combine pairs of nodes recursively."""
        if not nodes:
            return None
        if len(nodes) == 1:
            return nodes[0]
        
        pairs = []
        for i in range(0, len(nodes) - 1, 2):
            pairs.append(self._meld(nodes[i], nodes[i + 1]))
        if len(nodes) % 2 == 1:
            pairs.append(nodes[-1])
        return self._combine_pairs(pairs)

    def decrease_key(self, value: int, new_key: float) -> bool:
        """Decrease the key of a node."""
        if value not in self.node_map:
            return False
        
        node = self.node_map[value]
        if new_key > node.key:
            return False
        
        node.key = new_key
        if node is self.root:
            return True
        
        # Remove node from parent's children
        if node.parent:
            node.parent.children.remove(node)
            node.parent = None
        
        # Meld with root
        self.root = self._meld(self.root, node)
        return True

    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return self.root is None

class Graph:
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph = defaultdict(list)
        self.weights = {}

    def add_edge(self, u: int, v: int, w: float) -> None:
        """Add an edge to the graph."""
        self.graph[u].append(v)
        self.weights[(u, v)] = w

def bellman_ford(graph: Graph, source: int) -> Optional[List[float]]:
    """Bellman-Ford algorithm for reweighting."""
    V = graph.V
    dist = [float('inf')] * V
    dist[source] = 0

    # Relax edges repeatedly
    for _ in range(V - 1):
        for u in range(V):
            for v in graph.graph[u]:
                if dist[u] != float('inf') and dist[u] + graph.weights[(u, v)] < dist[v]:
                    dist[v] = dist[u] + graph.weights[(u, v)]

    # Check for negative cycles
    for u in range(V):
        for v in graph.graph[u]:
            if dist[u] != float('inf') and dist[u] + graph.weights[(u, v)] < dist[v]:
                return None  # Negative cycle detected

    return dist

def dijkstra_with_pairing_heap(graph: Graph, source: int, weight_func) -> List[float]:
    """Dijkstra's algorithm using pairing heap."""
    V = graph.V
    dist = [float('inf')] * V
    dist[source] = 0
    
    heap = PairingHeap()
    heap.insert(0, source)
    
    while not heap.is_empty():
        d, u = heap.delete_min()
        
        if d > dist[u]:
            continue
            
        for v in graph.graph[u]:
            new_dist = dist[u] + weight_func(u, v)
            if new_dist < dist[v]:
                dist[v] = new_dist
                if v in heap.node_map:
                    heap.decrease_key(v, new_dist)
                else:
                    heap.insert(new_dist, v)
    
    return dist

def johnsons_algorithm(graph: Graph) -> Optional[List[List[float]]]:
    """Johnson's algorithm for all-pairs shortest paths."""
    V = graph.V
    
    # Add new vertex and edges
    new_graph = Graph(V + 1)
    for u in range(V):
        for v in graph.graph[u]:
            new_graph.add_edge(u, v, graph.weights[(u, v)])
        new_graph.add_edge(V, u, 0)  # Add edge from new vertex to all vertices
    
    # Run Bellman-Ford
    h = bellman_ford(new_graph, V)
    if h is None:
        return None  # Negative cycle detected
    
    # Reweight edges
    reweighted_graph = Graph(V)
    for u in range(V):
        for v in graph.graph[u]:
            new_weight = graph.weights[(u, v)] + h[u] - h[v]
            reweighted_graph.add_edge(u, v, new_weight)
    
    # Run Dijkstra's algorithm for each vertex
    D = [[0] * V for _ in range(V)]
    for u in range(V):
        D[u] = dijkstra_with_pairing_heap(reweighted_graph, u, 
                                        lambda u, v: reweighted_graph.weights[(u, v)])
    
    # Adjust distances
    for u in range(V):
        for v in range(V):
            if D[u][v] != float('inf'):
                D[u][v] = D[u][v] - h[u] + h[v]
    
    return D

def main():
    # Example usage
    V = 5
    graph = Graph(V)
    
    # Add edges (example graph)
    edges = [
        (0, 1, -1),
        (0, 2, 4),
        (1, 2, 3),
        (1, 3, 2),
        (1, 4, 2),
        (3, 2, 5),
        (3, 1, 1),
        (4, 3, -3)
    ]
    
    for u, v, w in edges:
        graph.add_edge(u, v, w)
    
    # Run Johnson's algorithm
    result = johnsons_algorithm(graph)
    
    if result is None:
        print("Graph contains negative cycle")
    else:
        print("Shortest distances between all pairs of vertices:")
        for i in range(V):
            for j in range(V):
                if result[i][j] == float('inf'):
                    print(f"{i} -> {j}: INF", end="\t")
                else:
                    print(f"{i} -> {j}: {result[i][j]}", end="\t")
            print()

if __name__ == "__main__":
    main() 