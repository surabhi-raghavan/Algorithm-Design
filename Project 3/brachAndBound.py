import csv
import os
import heapq

def readMatrix(filepath):
    matrix = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            matrix.append([float(value) for value in row])
    return matrix


def lowerBound(matrix, path):
    n = len(matrix)
    unvisited = set(range(n)) - set(path)
    cost = 0
    last_node = path[-1]
    
    if unvisited:
        min_outgoing = min(matrix[last_node][k] for k in unvisited)
        cost += min_outgoing

    for node in unvisited:
        min_edges = sorted(matrix[node][j] for j in range(n) if j != node)
        if len(min_edges) >= 2:
            cost += min_edges[0] + min_edges[1]

    return cost / 2

def branchAndBound(matrix, start_node):
    n = len(matrix)
    best_cost = float('inf')
    best_tour = None
    heap = []

    initial_path = [start_node]
    initial_bound = lowerBound(matrix, initial_path)
    heapq.heappush(heap, (initial_bound, 0, initial_path))

    while heap:
        bound, cost, path = heapq.heappop(heap)

        if bound >= best_cost:
            continue

        if len(path) == n:
            total_cost = cost + matrix[path[-1]][start_node]
            if total_cost < best_cost:
                best_cost = total_cost
                best_tour = path + [start_node]
            continue

        for node in range(n):
            if node not in path:
                new_cost = cost + matrix[path[-1]][node]
                new_path = path + [node]
                new_bound = new_cost + lowerBound(matrix, new_path)
                if new_bound < best_cost:
                    heapq.heappush(heap, (new_bound, new_cost, new_path))

    calculated_weight = sum(matrix[best_tour[i]][best_tour[i + 1]] for i in range(len(best_tour) - 1))
    return best_tour, calculated_weight

if __name__ == "__main__":
    folderpath = "Project 3/Project3-Input-Files"  
    results = []

    for i in range(4, 14):
        filename = f"{i}n.csv"
        filepath = os.path.join(folderpath, filename)
        try:
            matrix = readMatrix(filepath)
            start_node = 0
            tour, total_weight = branchAndBound(matrix, start_node)
            results.append((filename, tour, total_weight))
            print(f"Branch-and-Bound Algorithm for {filename}:")
            print("Tour:", tour)
            print("Total Weight:", total_weight)
        except FileNotFoundError:
            print(f"File {filename} not found in {folderpath}. Skipping.")
