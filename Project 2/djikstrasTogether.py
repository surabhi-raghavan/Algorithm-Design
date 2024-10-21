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

class Matrix:
    def __init__(self, size):
        self.size = size
        self.data = [[INF for _ in range(size)] for _ in range(size)]

    def set(self, i, j, value):
        self.data[i][j] = value

    def get(self, i, j):
        return self.data[i][j]


def read_input(file_path):
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

def dijkstra_linked_list(nodes, edges, src, num_nodes):
    dist = [INF] * num_nodes
    prev = [-1] * num_nodes
    visited = [False] * num_nodes

    dist[src] = 0

    for _ in range(num_nodes):
        u = -1
        min_dist = INF
        for i in range(num_nodes):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        if u == -1:
            break

        visited[u] = True

        edge_idx = nodes[u].head
        while edge_idx != -1:
            edge = edges[edge_idx]
            v = edge.to
            weight = edge.weight
            if not visited[v] and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u
            edge_idx = edge.next

    return dist, prev

def dijkstra_matrix(graph, src, num_nodes):
    dist = [INF] * num_nodes
    prev = [-1] * num_nodes
    visited = [False] * num_nodes

    dist[src] = 0

    for _ in range(num_nodes):
        u = -1
        min_dist = INF
        for i in range(num_nodes):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        if u == -1:
            break

        visited[u] = True

        for v in range(num_nodes):
            weight = graph.get(u, v)
            if not visited[v] and weight != INF and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u

    return dist, prev

def calculate_memory_linked_list(nodes, edges):
    node_memory = sum(sys.getsizeof(node) for node in nodes)
    edge_memory = sum(sys.getsizeof(edge) for edge in edges)
    return node_memory + edge_memory

def calculate_memory_matrix(graph):
    matrix_memory = sys.getsizeof(graph.data) + sum(sys.getsizeof(row) for row in graph.data)
    return matrix_memory

def process_file(file_path, src_node, dest_node):
    print(f"Processing file: {file_path}")
    
    edges_data, num_nodes = read_input(file_path)
    
    nodes_linked_list = [Node() for _ in range(num_nodes)]
    edges_linked_list = []
    
    for u, v, w in edges_data:
        new_edge = Edge()
        new_edge.to = v
        new_edge.weight = w
        new_edge.next = nodes_linked_list[u].head
        nodes_linked_list[u].head = len(edges_linked_list)
        edges_linked_list.append(new_edge)

    start_time = time.time()
    dist_ll, _ = dijkstra_linked_list(nodes_linked_list, edges_linked_list, src_node, num_nodes)
    linked_list_time = time.time() - start_time
    linked_list_memory = calculate_memory_linked_list(nodes_linked_list, edges_linked_list)
    print(f"Linked List - Time: {linked_list_time:.4f} seconds, Memory: {linked_list_memory / 1024:.2f} KB")

    graph_matrix = Matrix(num_nodes)
    for u, v, w in edges_data:
        graph_matrix.set(u, v, w)

    start_time = time.time()
    dist_mx, _ = dijkstra_matrix(graph_matrix, src_node, num_nodes)
    matrix_time = time.time() - start_time
    matrix_memory = calculate_memory_matrix(graph_matrix)
    print(f"Matrix - Time: {matrix_time:.4f} seconds, Memory: {matrix_memory / 1024:.2f} KB")

    return linked_list_time, matrix_time, linked_list_memory, matrix_memory

def main():
    input_files = [
        f'Project2_Input_File/Project2_Input_File{i}.csv' for i in range(1, 16)
    ]

    linked_list_times = []
    matrix_times = []
    linked_list_memories = []
    matrix_memories = []
    file_indices = list(range(1, len(input_files) + 1))

    src_node = 192  
    dest_node = 163  

    for file_path in input_files:
        if os.path.exists(file_path):
            ll_time, mx_time, ll_memory, mx_memory = process_file(file_path, src_node, dest_node)
            linked_list_times.append(ll_time)
            matrix_times.append(mx_time)
            linked_list_memories.append(ll_memory / 1024)  # Convert to KB
            matrix_memories.append(mx_memory / 1024)  # Convert to KB
        else:
            print(f"File not found: {file_path}")
            linked_list_times.append(None)
            matrix_times.append(None)
            linked_list_memories.append(None)
            matrix_memories.append(None)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel("Input File Index")
    ax1.set_ylabel("Memory (KB)", color='tab:red')
    ax1.plot(file_indices, linked_list_memories, marker='o', label="Linked List Memory", color='tab:red')
    ax1.plot(file_indices, matrix_memories, marker='x', label="Matrix Memory", color='tab:orange')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    plt.title("Dijkstra's Algorithm - Memory Usage Comparison (Linked List vs Matrix)")
    fig.tight_layout()  
    ax1.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
