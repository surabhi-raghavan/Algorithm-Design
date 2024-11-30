import csv
import os

def readMatrix(filepath):
    matrix = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            matrix.append([float(value) for value in row])
    return matrix


def findLeastEdge(matrix):
    n = len(matrix)
    min_weight = float('inf')
    min_edge = (0, 0)
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] < min_weight:
                min_weight = matrix[i][j]
                min_edge = (i, j)
    return min_edge, min_weight

def nearestInsertion(matrix):
    n = len(matrix)
    nodes = set(range(n))
    edge, total_weight = findLeastEdge(matrix)
    tour = [edge[0], edge[1], edge[0]]
    nodes.remove(edge[0])
    nodes.remove(edge[1])

    while nodes:
        min_increase = float('inf')
        insertion_node = None
        insertion_pos = None

        for node in nodes:
            for i in range(1, len(tour)):
                prev_node = tour[i-1]
                next_node = tour[i]
                increase = (matrix[prev_node][node] + matrix[node][next_node]
                            - matrix[prev_node][next_node])
                if increase < min_increase:
                    min_increase = increase
                    insertion_node = node
                    insertion_pos = i

        tour.insert(insertion_pos, insertion_node)
        total_weight += min_increase
        nodes.remove(insertion_node)

    calculated_weight = sum(matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
    return tour, calculated_weight

if __name__ == "__main__":
    folderpath = "Project 3/Project3-Input-Files"  
    results = []

    for i in range(4, 14):
        filename = f"{i}n.csv"
        filepath = os.path.join(folderpath, filename)
        try:
            matrix = readMatrix(filepath)
            tour, totalWeight = nearestInsertion(matrix)
            results.append((filename, tour, totalWeight))
            print(f"Nearest Insertion Heuristic for {filename}:")
            print("Tour:", tour)
            print("Total Weight:", totalWeight)
        except FileNotFoundError:
            print(f"File {filename} not found in {folderpath}. Skipping.")
