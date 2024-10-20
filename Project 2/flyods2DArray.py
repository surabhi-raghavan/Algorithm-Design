import sys
import time
import os
import matplotlib.pyplot as plt

INF = float('inf')

class Matrix:
    def __init__(self, size):
        self.size = size
        self.data = [[INF for _ in range(size)] for _ in range(size)]
        for i in range(size):
            self.data[i][i] = 0  

    def set(self, i, j, value):
        self.data[i][j] = value

    def get(self, i, j):
        return self.data[i][j]

def readInput(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  
    max_node_id = -1
    edges = []
    for line in lines:
        parts = line.strip().split(',')
        node_id, connected_node_id, distance = int(parts[0]), int(parts[1]), int(parts[2])
        edges.append((node_id, connected_node_id, distance))
        max_node_id = max(max_node_id, node_id, connected_node_id)
    return edges, max_node_id + 1  

def floydWarshall(graph, num_nodes):
    distance = [[graph.get(i, j) for j in range(num_nodes)] for i in range(num_nodes)]
    previous = [[-1 if i != j and graph.get(i, j) == INF else i for j in range(num_nodes)] for i in range(num_nodes)]

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if distance[i][j] > distance[i][k] + distance[k][j]:
                    distance[i][j] = distance[i][k] + distance[k][j]
                    previous[i][j] = previous[k][j]

    return distance, previous

def print_path(previous, source_node, destination_node):
    path = []
    if previous[source_node][destination_node] == -1:
        print(f"No path from {source_node} to {destination_node}")
        return
    
    current = destination_node
    while current != source_node:
        path.append(current)
        current = previous[source_node][current]
    path.append(source_node)
    path.reverse()

    print(" -> ".join(map(str, path)))

def print_path_floyd_warshall(source_node, destination_node, distance_matrix, predecessor_matrix):
    if distance_matrix[source_node][destination_node] == INF:
        print(f"No path from {source_node} to {destination_node}")
    else:
        print(f"Shortest distance from node {source_node} to node {destination_node}: {distance_matrix[source_node][destination_node]} feet")
        print("Path: ", end='')
        print_path(predecessor_matrix, source_node, destination_node)

def calculate_memory_matrix(graph, num_nodes):
    matrix_memory = sys.getsizeof(graph.data) + sum(sys.getsizeof(row) for row in graph.data)
    return matrix_memory

def process_file(file_path, source_node, destination_node):
    print(f"Processing file: {file_path}")
    edges, num_nodes = readInput(file_path)
   
    graph = Matrix(num_nodes)
    for u, v, w in edges:
        graph.set(u, v, w)

    matrix_memory = calculate_memory_matrix(graph, num_nodes)
    print(f"Memory used by two-dimensional array (Matrix): {matrix_memory / 1024:.2f} KB")

    start_time = time.time()
    distance_matrix, previous_matrix = floydWarshall(graph, num_nodes)
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.4f} seconds")

    print_path_floyd_warshall(source_node, destination_node, distance_matrix, previous_matrix)
    print("\n")
    
    return total_time

def main():
    input_files = [
        f'Project2_Input_File/Project2_Input_File{i}.csv' for i in range(1, 16)
    ]
    
    floyd_warshall_times = []
    file_indices = list(range(1, len(input_files) + 1))

    source_node = 192  
    destination_node = 163 

    for file_path in input_files:
        if os.path.exists(file_path):
            execution_time = process_file(file_path, source_node, destination_node)
            floyd_warshall_times.append(execution_time)
        else:
            print(f"File not found: {file_path}")
            floyd_warshall_times.append(None)


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
