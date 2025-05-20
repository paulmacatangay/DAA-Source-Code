from collections import defaultdict
from typing import Dict, List, Tuple

class Graph:
    """
    Directed graph representation for Johnson's Algorithm.
    Vertices are indexed from 0 to V-1.
    """
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph: Dict[int, List[int]] = defaultdict(list)
        self.weights: Dict[Tuple[int, int], float] = {}

    def add_edge(self, u: int, v: int, weight: float):
        """
        Add a directed edge from u to v with the given weight.
        """
        self.graph[u].append(v)
        self.weights[(u, v)] = weight
