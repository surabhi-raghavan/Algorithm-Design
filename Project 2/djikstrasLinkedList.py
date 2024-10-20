import sys
import time
import os
import matplotlib.pyplot as plt

INF = float('inf')

class Edge:
    def __init__(self):
        self.to = -1
        self.weight = INF
        self.next = -1  

class Node:
    def __init__(self):
        self.head = -1 

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

def djikstra(nodes, edges, source, num_nodes):
    distance = [INF] * num_nodes
    previous = [-1] * num_nodes
    visited = [False] * num_nodes

    distance[source] = 0

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

        edge_idx = nodes[u].head
        while edge_idx != -1:
            edge = edges[edge_idx]
            v = edge.to
            weight = edge.weight
            if not visited[v] and distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                previous[v] = u
            edge_idx = edge.next

    return distance, previous

def print_path(previous, destination):
    if previous[destination] == -1:
        print(destination, end='')
    else:
        print_path(previous, previous[destination])
        print(f' -> {destination}', end='')

def calculate_memory_linked_list(nodes, edges, num_nodes):
    node_memory = sum(sys.getsizeof(node) for node in nodes)
    edge_memory = sum(sys.getsizeof(edge) for edge in edges)
    return node_memory + edge_memory

def process_file(file_path, source_node, destination_node):
    
    print(f"Processing file: {file_path}")
    edges_data, num_nodes = readInput(file_path)
    
    nodes = [Node() for _ in range(num_nodes)]
    edges = []
    
    for u, v, w in edges_data:
        new_edge = Edge()
        new_edge.to = v
        new_edge.weight = w
        new_edge.next = nodes[u].head
        nodes[u].head = len(edges)
        edges.append(new_edge)

    
    linked_list_memory = calculate_memory_linked_list(nodes, edges, num_nodes)
    print(f"Memory used by linked list: {linked_list_memory / 1024:.2f} KB")

    start_time = time.time()
    distance, previous = dijkstra(nodes, edges, source_node, num_nodes)
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.4f} seconds")

    if distance[destination_node] != INF:
        print(f"Shortest distance from node {source_node} to node {destination_node}: {distance[destination_node]} feet")
        print("Path: ", end='')
        print_path(previous, destination_node)
        print(f"\nTotal distance: {distance[destination_node]}\n")
    else:
        print(f"No path from node {source_node} to node {destination_node}")

    return total_time

def main():
    input_files = [
        f'Project2_Input_File/Project2_Input_File{i}.csv' for i in range(1, 16)
    ]
    
    djikstra_times = []
    file_indices = list(range(1, len(input_files) + 1))

    src_node = 192  
    dest_node = 163  

    for file_path in input_files:
        if os.path.exists(file_path):
            execution_time = process_file(file_path, src_node, dest_node)
            djikstra_times.append(execution_time)
        else:
            print(f"File not found: {file_path}")
            djikstra_times.append(None)

    plt.figure(figsize=(10, 6))
    plt.plot(file_indices, djikstra_times, marker='o', label="Dijkstra's Algorithm (Linked List)")
    plt.xlabel("Input File Index")
    plt.ylabel("Time (seconds)")
    plt.title("Dijkstra's Algorithm Time Performance for Each Input File (Linked List)")
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
