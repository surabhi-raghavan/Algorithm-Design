import sys
import time
import tracemalloc
import psutil
import resource
import os

INF = float('inf')

class Edge:
    def __init__(self):
        self.to = -1
        self.weight = INF
        self.next = -1

class Node:
    def __init__(self):
        self.head = -1

def floyd_warshall(nodes, edges, num_nodes):
    dist = [[INF]*num_nodes for _ in range(num_nodes)]
    next_node = [[-1]*num_nodes for _ in range(num_nodes)]

    for i in range(num_nodes):
        dist[i][i] = 0
        next_node[i][i] = i
        edge_idx = nodes[i].head
        while edge_idx != -1:
            edge = edges[edge_idx]
            dist[i][edge.to] = edge.weight
            next_node[i][edge.to] = edge.to
            edge_idx = edge.next

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node

def report_memory_usage(nodes, edges, dist, next_node, file_name, totals):
    print(f"\n[ Memory Usage Report for {file_name} ]")
    node_memory = sum(sys.getsizeof(node) for node in nodes)
    edge_memory = sum(sys.getsizeof(edge) for edge in edges)
    dist_memory = sys.getsizeof(dist) + sum(sys.getsizeof(row) for row in dist)
    next_node_memory = sys.getsizeof(next_node) + sum(sys.getsizeof(row) for row in next_node)

    print(f"Memory used by Nodes: {node_memory / 1024:.2f} KB")
    print(f"Memory used by Edges: {edge_memory / 1024:.2f} KB")
    print(f"Memory used by Distance Matrix: {dist_memory / 1024:.2f} KB")
    print(f"Memory used by Next Node Matrix: {next_node_memory / 1024:.2f} KB")

    # Accumulate totals for averaging
    totals["node_memory"] += node_memory
    totals["edge_memory"] += edge_memory
    totals["dist_memory"] += dist_memory
    totals["next_node_memory"] += next_node_memory
    totals["count"] += 1

def track_peak_memory():
    peak_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(f"Peak Memory Usage: {peak_memory / 1024:.2f} MB")

def track_process_memory():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()

    print(f"Overall Process Memory Usage: {memory_info.rss / 1024 ** 2:.2f} MB (Resident Set Size)")

def track_memory_snapshot():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    print("\n[ Top 5 Memory Consumers ]")
    for stat in top_stats[:5]:
        print(stat)

def process_file(input_file, totals):
    tracemalloc.start()

    with open(input_file, 'r') as file:
        lines = file.readlines()[1:]
    max_node_id = -1
    edges_data = []
    for line in lines:
        parts = line.strip().split(',')
        node_id, connected_node_id, distance = map(int, parts[:3])
        edges_data.append((node_id, connected_node_id, distance))
        max_node_id = max(max_node_id, node_id, connected_node_id)

    num_nodes = max_node_id + 1
    nodes = [Node() for _ in range(num_nodes)]
    edges = []

    for u, v, w in edges_data:
        new_edge = Edge()
        new_edge.to = v
        new_edge.weight = w
        new_edge.next = nodes[u].head
        nodes[u].head = len(edges)
        edges.append(new_edge)

    dist, next_node = floyd_warshall(nodes, edges, num_nodes)

    report_memory_usage(nodes, edges, dist, next_node, input_file, totals)
    track_peak_memory()
    track_process_memory()
    track_memory_snapshot()

    tracemalloc.stop()

def main(input_files):
    totals = {
        "node_memory": 0,
        "edge_memory": 0,
        "dist_memory": 0,
        "next_node_memory": 0,
        "count": 0
    }

    for file_path in input_files:
        print(f"\nProcessing {file_path}...")
        process_file(file_path, totals)

    if totals["count"] > 0:
        avg_node_memory = totals["node_memory"] / totals["count"]
        avg_edge_memory = totals["edge_memory"] / totals["count"]
        avg_dist_memory = totals["dist_memory"] / totals["count"]
        avg_next_node_memory = totals["next_node_memory"] / totals["count"]

        print("\n[ Average Memory Usage Across All Files ]")
        print(f"Average Memory used by Nodes: {avg_node_memory / 1024:.2f} KB")
        print(f"Average Memory used by Edges: {avg_edge_memory / 1024:.2f} KB")
        print(f"Average Memory used by Distance Matrix: {avg_dist_memory / 1024:.2f} KB")
        print(f"Average Memory used by Next Node Matrix: {avg_next_node_memory / 1024:.2f} KB")

if __name__ == "__main__":
    input_files = [
        'Project2_Input_File/Project2_Input_File13.csv' 
    ]
    main(input_files)
