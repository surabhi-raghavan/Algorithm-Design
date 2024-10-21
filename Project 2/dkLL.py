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

def dijkstra(nodes, edges, src, num_nodes):
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
            if not visited[edge.to]:
                if dist[u] + edge.weight < dist[edge.to]:
                    dist[edge.to] = dist[u] + edge.weight
                    prev[edge.to] = u
            edge_idx = edge.next

    return dist, prev

def report_memory_usage(nodes, edges, dist, prev, visited, file_name, totals):
    print(f"\n[ Memory Usage Report for {file_name} ]")
    
    node_memory = sum(sys.getsizeof(node) for node in nodes)
    edge_memory = sum(sys.getsizeof(edge) for edge in edges)
    distance_memory = sys.getsizeof(dist)
    prev_memory = sys.getsizeof(prev)
    visited_memory = sys.getsizeof(visited)

    print(f"Memory used by Nodes: {node_memory / 1024:.2f} KB")
    print(f"Memory used by Edges: {edge_memory / 1024:.2f} KB")
    print(f"Memory used by Distance Array: {distance_memory / 1024:.2f} KB")
    print(f"Memory used by Previous Array: {prev_memory / 1024:.2f} KB")
    print(f"Memory used by Visited Array: {visited_memory / 1024:.2f} KB")

    # Accumulate totals for averaging
    totals["node_memory"] += node_memory
    totals["edge_memory"] += edge_memory
    totals["dist_memory"] += distance_memory
    totals["prev_memory"] += prev_memory
    totals["visited_memory"] += visited_memory
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
        lines = file.readlines()[1:]  # Skip the header line
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

    dist, prev = dijkstra(nodes, edges, 0, num_nodes)
    visited = [False] * num_nodes

    report_memory_usage(nodes, edges, dist, prev, visited, input_file, totals)
    track_peak_memory()
    track_process_memory()
    track_memory_snapshot()

    tracemalloc.stop()

def main(input_files):
    totals = {
        "node_memory": 0,
        "edge_memory": 0,
        "dist_memory": 0,
        "prev_memory": 0,
        "visited_memory": 0,
        "count": 0
    }

    for file_path in input_files:
        print(f"\nProcessing {file_path}...")
        process_file(file_path, totals)

    if totals["count"] > 0:
        avg_node_memory = totals["node_memory"] / totals["count"]
        avg_edge_memory = totals["edge_memory"] / totals["count"]
        avg_dist_memory = totals["dist_memory"] / totals["count"]
        avg_prev_memory = totals["prev_memory"] / totals["count"]
        avg_visited_memory = totals["visited_memory"] / totals["count"]

        print("\n[ Average Memory Usage Across All Files ]")
        print(f"Average Memory used by Nodes: {avg_node_memory / 1024:.2f} KB")
        print(f"Average Memory used by Edges: {avg_edge_memory / 1024:.2f} KB")
        print(f"Average Memory used by Distance Array: {avg_dist_memory / 1024:.2f} KB")
        print(f"Average Memory used by Previous Array: {avg_prev_memory / 1024:.2f} KB")
        print(f"Average Memory used by Visited Array: {avg_visited_memory / 1024:.2f} KB")

if __name__ == "__main__":
    input_files = [
       f'Project2_Input_File/Project2_Input_File{i}.csv' for i in range(1, 16)
    ]
    main(input_files)
