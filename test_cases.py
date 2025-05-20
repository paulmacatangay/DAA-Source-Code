import random
import time
from typing import Optional
from graph import Graph
from johnson_pairing_heap import johnsons_algorithm

def generate_test_case(vertices: int, edge_density: float, negative_weight_ratio: float = 0.2) -> Graph:
    graph = Graph(vertices)
    max_edges = vertices * (vertices - 1)
    num_edges = int(max_edges * edge_density)
    for _ in range(num_edges):
        u = random.randint(0, vertices - 1)
        v = random.randint(0, vertices - 1)
        if u != v:
            weight = random.uniform(-100, 100) if random.random() < negative_weight_ratio else random.uniform(1, 100)
            graph.add_edge(u, v, weight)
    return graph

def generate_grid_graph(size: int) -> Graph:
    graph = Graph(size * size)
    for i in range(size):
        for j in range(size):
            current = i * size + j
            if j < size - 1:
                graph.add_edge(current, current + 1, random.uniform(1, 10))
            if i < size - 1:
                graph.add_edge(current, current + size, random.uniform(1, 10))
    return graph

def generate_scale_free_graph(vertices: int, edges: int) -> Graph:
    graph = Graph(vertices)
    for i in range(min(5, vertices)):
        for j in range(i + 1, min(5, vertices)):
            graph.add_edge(i, j, random.uniform(1, 10))
    for _ in range(edges - (min(5, vertices) * (min(5, vertices) - 1)) // 2):
        u = random.randint(0, vertices - 1)
        v = random.randint(0, vertices - 1)
        if u != v:
            graph.add_edge(u, v, random.uniform(1, 10))
    return graph

def run_test_suite():
    test_cases = [
        ("Small Sparse", generate_test_case(100, 0.2)),
        ("Small Dense", generate_test_case(100, 0.8)),
        ("Medium Sparse", generate_test_case(1000, 0.1)),
        ("Medium Dense", generate_test_case(1000, 0.5)),
        ("Large Sparse", generate_test_case(5000, 0.05)),
        ("Large Dense", generate_test_case(5000, 0.2)),
        ("Grid Graph", generate_grid_graph(30)),  # 30x30 grid
        ("Scale-Free Graph", generate_scale_free_graph(1000, 3000)),
    ]
    results = {}
    for name, graph in test_cases:
        print(f"Running {name}...")
        start_time = time.time()
        result = johnsons_algorithm(graph)
        end_time = time.time()
        print(f"  Vertices: {graph.V}")
        print(f"  Edges: {sum(len(edges) for edges in graph.graph.values())}")
        print(f"  Time: {end_time - start_time:.4f} seconds")
        print(f"  Success: {result is not None}")
        print()
        results[name] = {
            "time": end_time - start_time,
            "vertices": graph.V,
            "edges": sum(len(edges) for edges in graph.graph.values()),
            "success": result is not None
        }
    return results

if __name__ == "__main__":
    run_test_suite()
