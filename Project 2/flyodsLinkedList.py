import sys
import time
import os
import matplotlib.pyplot as plt

INF = float('inf')

# Custom Node and Edge classes to simulate a linked list
class Edge:
    def __init__(self):
        self.to = -1
        self.weight = INF
        self.next = -1  # Index of the next edge

class Node:
    def __init__(self):
        self.head = -1  # Index of the first edge

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
    return edges, max_node_id + 1  # Returning number of nodes as max_node_id + 1

def floyd_warshall(nodes, edges, num_nodes):
    dist = [[INF] * num_nodes for _ in range(num_nodes)]
    next_node = [[-1] * num_nodes for _ in range(num_nodes)]

    # Initialize distance and next_node matrices
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

    # Floyd-Warshall main algorithm
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node

def print_path(next_node, src, dest):
    if next_node[src][dest] == -1:
        print("No path", end='')
        return
    path = [src]
    while src != dest:
        src = next_node[src][dest]
        path.append(src)
    print(' -> '.join(map(str, path)), end='')

def calculate_memory(nodes, edges):
    memory_usage = sys.getsizeof(nodes) + sum(sys.getsizeof(node) for node in nodes)
    memory_usage += sys.getsizeof(edges) + sum(sys.getsizeof(edge) for edge in edges)
    return memory_usage

def process_file(file_path, source_node, destination_node):
    print(f"Processing file: {file_path}")
    edges_data, num_nodes = read_input(file_path)
    
    nodes = [Node() for _ in range(num_nodes)]
    edges = []
    
    # Build the adjacency list (linked list representation)
    for u, v, w in edges_data:
        new_edge = Edge()
        new_edge.to = v
        new_edge.weight = w
        new_edge.next = nodes[u].head
        nodes[u].head = len(edges)
        edges.append(new_edge)

    memory_used = calculate_memory(nodes, edges)
    print(f"Memory used: {memory_used / 1024:.2f} KB")

    start_time = time.time()
    dist, next_node = floyd_warshall(nodes, edges, num_nodes)
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.4f} seconds")

    print(f"Shortest path from node {source_node} to node {destination_node}: ", end='')
    print_path(next_node, source_node, destination_node)
    print(f"\nTotal distance: {dist[source_node][destination_node]}")
    print("\n")

    return total_time

def main():
    input_files = [
        f'Project2_Input_File/Project2_Input_File{i}.csv' for i in range(1, 16)
    ]
    
    floyd_warshall_times = []
    file_indices = list(range(1, len(input_files) + 1))

    source_node = 192  # Example source node
    destination_node = 163  # Example destination node

    for file_path in input_files:
        if os.path.exists(file_path):
            execution_time = process_file(file_path, source_node, destination_node)
            floyd_warshall_times.append(execution_time)
        else:
            print(f"File not found: {file_path}")
            floyd_warshall_times.append(None)

    # Plotting the time performance of Floyd-Warshall Algorithm
    plt.figure(figsize=(12, 6))
    plt.plot(file_indices, floyd_warshall_times, marker='o', label="Floyd-Warshall Algorithm")
    plt.xlabel("Input File Index")
    plt.ylabel("Time (seconds)")
    plt.title("Floyd-Warshall Algorithm Time Performance for Each Input File")
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
