import csv
import os

def readMatrix(filepath):
    matrix = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            matrix.append([float(value) for value in row])
    return matrix

def nearestNeighbor(matrix, start):
    n = len(matrix)
    unvisited = set(range(n))
    unvisited.remove(start)
    tour = [start]
    total_weight = 0
    current = start

    while unvisited:
        nearest = min(unvisited, key=lambda x: matrix[current][x])
        total_weight += matrix[current][nearest]
        current = nearest
        tour.append(current)
        unvisited.remove(current)

    total_weight += matrix[current][start]
    tour.append(start)
    return tour, total_weight

if __name__ == "__main__":
    folderpath = "Project 3/Project3-Input-Files"
    for i in range(4, 14):
        filename = f"{i}n.csv"
        filepath = os.path.join(folderpath, filename)
        try:
            matrix = readMatrix(filepath)
            start_node = 0
            tour, totalWeight = nearestNeighbor(matrix, start_node)
            print(f"Nearest Neighbor Heuristic for {filename}:")
            print("Tour:", tour)
            print("Total Weight:", totalWeight)
        except FileNotFoundError:
            print(f"File {filename} not found in {folderpath}. Skipping.")
