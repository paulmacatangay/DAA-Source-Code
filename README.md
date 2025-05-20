# Johnson's Algorithm with Pairing Heap

This repository contains a Python implementation of Johnson's Algorithm for the All-Pairs Shortest Path (APSP) problem, utilizing a Pairing Heap as the priority queue in Dijkstra's phase. The project includes modular code, extended test cases, and performance analysis tools.

## Features
- Efficient Johnson's Algorithm for APSP
- Pairing Heap data structure for improved performance
- Handles graphs with negative edge weights (no negative cycles)
- Includes utilities for generating various types of graphs (random, grid, scale-free)
- Comprehensive test suite and benchmarking

## Repository Structure
- `johnson_pairing_heap.py` – Main implementation of Johnson’s Algorithm with Pairing Heap
- `pairing_heap.py` – Pairing Heap data structure
- `graph.py` – Graph representation and utilities
- `test_cases.py` – Extended test cases and test suite
- `README.md` – Documentation and usage instructions
- `requirements.txt` – List of required Python packages (if any)

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/paulmacatangay/DAA-Source-Code.git
cd DAA-Source-Code
```

### 2. Install Requirements
Make sure you have Python 3.8+ installed. Install any dependencies:
```bash
pip install -r requirements.txt
```

### 3. Running the Main Algorithm
You can run the main script or import the modules in your own code. Example:
```bash
python johnson_pairing_heap.py
```

### 4. Running Test Cases
To run the provided test suite and benchmark different graph types:
```bash
python test_cases.py
```

## Example Usage
```python
from graph import Graph
from johnson_pairing_heap import johnsons_algorithm

graph = Graph(5)
graph.add_edge(0, 1, -1)
graph.add_edge(0, 2, 4)
graph.add_edge(1, 2, 3)
graph.add_edge(1, 3, 2)
graph.add_edge(1, 4, 2)
graph.add_edge(3, 2, 5)
graph.add_edge(3, 1, 1)
graph.add_edge(4, 3, -3)

result = johnsons_algorithm(graph)
if result is not None:
    print("Shortest distances:", result)
else:
    print("Graph contains a negative cycle")
```

## Documentation
- See `appendices.md` for full source code, extended test cases, and complexity proofs.
- See `experimental_results.md` for performance evaluation and analysis.

## Repository
[https://github.com/paulmacatangay/DAA-Source-Code](https://github.com/paulmacatangay/DAA-Source-Code)
