import sys
import time
import os
import matplotlib.pyplot as plt

INF = float('inf')

class Matrix:
    def __init__(self, size):
        self.size = size
        self.data = [[INF for _ in range(size)] for _ in range(size)]

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

def djikstra(graph, source_node, num_nodes):
    distance = [INF] * num_nodes
    previous_node = [-1] * num_nodes
    visited = [False] * num_nodes

    distance[source_node] = 0

    for _ in range(num_nodes):
        u = -1
        minimum_distance = INF
        for i in range(num_nodes):
            if not visited[i] and distance[i] < minimum_distance:
                minimum_distance = distance[i]
                u = i

        if u == -1:
            break

        visited[u] = True

        for v in range(num_nodes):
            if not visited[v]:
                weight = graph.get(u, v)
                if weight != INF and distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
                    previous_node[v] = u

    return distance, previous_node

def print_path(previous, destination):
    if previous[destination] == -1:
        print(destination, end='')
        
    else:
        print_path(previous, previous[destination])
        print(f' -> {destination}', end='')

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
    distance, previous = djikstra(graph, source_node, num_nodes)
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.4f} seconds")

    print(f"Shortest distance from node {source_node} to node {destination_node}: {distance[destination_node]} feet")
    print("Path: ", end='')
    print_path(previous, destination_node)
    print("\n")
    
    return total_time

def main():
    input_files = [
        f'Project2_Input_File/Project2_Input_File{i}.csv' for i in range(1, 16)
    ]
    
    dijkstra_times = []
    file_indices = list(range(1, len(input_files) + 1))

    source_node = 465  
    destination_node = 22 

    for file_path in input_files:
        if os.path.exists(file_path):
            execution_time = process_file(file_path, source_node, destination_node)
            dijkstra_times.append(execution_time)
        else:
            print(f"File not found: {file_path}")
            dijkstra_times.append(None)


    plt.figure(figsize=(12, 6))
    plt.plot(file_indices, dijkstra_times, marker='o', label="Dijkstra's Algorithm")
    plt.xlabel("Input File Index")
    plt.ylabel("Time (seconds)")
    plt.title("Dijkstra's Algorithm Time Performance for Each Input File")
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
