import sys
import time
import os
import matplotlib.pyplot as plt

INF = float('inf')

# Custom Node and Edge classes to simulate a linked list representation
class Edge:
    def __init__(self):
        self.to = -1
        self.weight = INF
        self.next = -1  # Index of the next edge

class Node:
    def __init__(self):
        self.head = -1  # Index of the first edge

# Matrix (Array-based) representation of the graph
class Matrix:
    def __init__(self, size):
        self.size = size
        self.data = [[INF for _ in range(size)] for _ in range(size)]
        for i in range(size):
            self.data[i][i] = 0  # Distance to self is 0

    def set(self, i, j, value):
        self.data[i][j] = value

    def get(self, i, j):
        return self.data[i][j]

# Reading input from CSV files
def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Skip the header
    max_node_id = -1
    edges = []
    for line in lines:
        parts = line.strip().split(',')
        node_id, connected_node_id, distance = int(parts[0]), int(parts[1]), int(parts[2])
        edges.append((node_id, connected_node_id, distance))
        max_node_id = max(max_node_id, node_id, connected_node_id)
    return edges, max_node_id + 1

# Floyd-Warshall using linked list
def floyd_warshall_linked_list(nodes, edges, num_nodes):
    dist = [[INF] * num_nodes for _ in range(num_nodes)]
    next_node = [[-1] * num_nodes for _ in range(num_nodes)]

    for i in range(num_nodes):
        dist[i][i] = 0
        next_node[i][i] = i
        edge_idx = nodes[i].head
        while edge_idx != -1:
            edge = edges[edge_idx]
            v = edge.to
            weight = edge.weight
            dist[i][v] = weight
            next_node[i][v] = v
            edge_idx = edge.next

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node

# Floyd-Warshall using array-based graph representation
def floyd_warshall_array(graph, num_nodes):
    dist = [[graph.get(i, j) for j in range(num_nodes)] for i in range(num_nodes)]
    next_node = [[-1 if i != j and graph.get(i, j) == INF else i for j in range(num_nodes)] for i in range(num_nodes)]

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node

# Calculate memory usage for linked list representation
def calculate_memory_linked_list(nodes, edges):
    memory_usage = sys.getsizeof(nodes) + sum(sys.getsizeof(node) for node in nodes)
    memory_usage += sys.getsizeof(edges) + sum(sys.getsizeof(edge) for edge in edges)
    return memory_usage

# Calculate memory usage for array-based representation
def calculate_memory_array(graph):
    return sys.getsizeof(graph.data) + sum(sys.getsizeof(row) for row in graph.data)

# Processing file for linked list-based representation
def process_file_linked_list(file_path, source_node, destination_node):
    print(f"Processing file for Linked List representation: {file_path}")
    edges_data, num_nodes = read_input(file_path)

    nodes = [Node() for _ in range(num_nodes)]
    edges = []

    for u, v, w in edges_data:
        new_edge = Edge()
        new_edge.to = v
        new_edge.weight = w
        new_edge.next = nodes[u].head
        nodes[u].head = len(edges)
        edges.append(new_edge)

    memory_usage = calculate_memory_linked_list(nodes, edges)
    print(f"Memory used (Linked List): {memory_usage / 1024:.2f} KB")
    return memory_usage

# Processing file for array-based representation
def process_file_array(file_path, source_node, destination_node):
    print(f"Processing file for Array representation: {file_path}")
    edges_data, num_nodes = read_input(file_path)

    graph = Matrix(num_nodes)
    for u, v, w in edges_data:
        graph.set(u, v, w)

    memory_usage = calculate_memory_array(graph)
    print(f"Memory used (Array): {memory_usage / 1024:.2f} KB")
    return memory_usage

def main():
    input_files = [
        f'Project2_Input_File/Project2_Input_File{i}.csv' for i in range(1, 16)
    ]

    source_node = 192  # Example source node
    destination_node = 163  # Example destination node

    linked_list_memories = []
    array_memories = []
    file_indices = list(range(1, len(input_files) + 1))

    # Process each file for both linked list and array representations
    for file_path in input_files:
        if os.path.exists(file_path):
            print(f"Processing {file_path} ...")
            linked_list_memory = process_file_linked_list(file_path, source_node, destination_node)
            array_memory = process_file_array(file_path, source_node, destination_node)

            linked_list_memories.append(linked_list_memory / 1024)  # Convert to KB
            array_memories.append(array_memory / 1024)  # Convert to KB
        else:
            print(f"File not found: {file_path}")
            linked_list_memories.append(None)
            array_memories.append(None)

    # Plotting the memory usage comparison
    if any(linked_list_memories) or any(array_memories):
        plt.figure(figsize=(12, 6))
        plt.plot(file_indices, linked_list_memories, marker='o', label="Linked List Representation")
        plt.plot(file_indices, array_memories, marker='x', label="Array-Based Representation")
        plt.xlabel("Input File Index")
        plt.ylabel("Memory (KB)")
        plt.title("Floyd-Warshall Algorithm Memory Usage (Linked List vs Array)")
        plt.xticks(rotation=45, ha='right')
        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.show()
    else:
        print("No data to plot. Please check the input files.")

if __name__ == "__main__":
    main()
