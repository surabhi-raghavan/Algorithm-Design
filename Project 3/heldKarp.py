import csv
import itertools
import os

def readMatrix(filepath):
    matrix = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            matrix.append([float(value) for value in row])
    return matrix

def heldKarp(matrix):
    n = len(matrix)
    C = {}

    for k in range(1, n):
        C[(1 << k, k)] = (matrix[0][k], 0)

    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = sum(1 << bit for bit in subset)
            for k in subset:
                prev_bits = bits & ~(1 << k)
                res = []
                for m in subset:
                    if m == k:
                        continue
                    res.append((C[(prev_bits, m)][0] + matrix[m][k], m))
                C[(bits, k)] = min(res)

    bits = (2 ** n - 1) - 1
    res = [(C[(bits, k)][0] + matrix[k][0], k) for k in range(1, n)]
    opt, parent = min(res)

    path = []
    bits = (2 ** n - 1) - 1
    last = parent

    while last != 0:
        path.append(last)
        new_bits = bits & ~(1 << last)
        _, last = C[(bits, last)]
        bits = new_bits

    path = [0] + list(reversed(path)) + [0]
    return path, opt


if __name__ == "__main__":
    folderpath = "Project 3/Project3-Input-Files"
    results = []

    for i in range(4, 14):
        filename = f"{i}n.csv"
        filepath = os.path.join(folderpath, filename)
        try:
            matrix = readMatrix(filepath)
            tour, total_weight = heldKarp(matrix)
            results.append((filename, tour, total_weight))
            print(f"Dynamic Programming (Held-Karp) Algorithm for {filename}:")
            print("Tour:", tour)
            print("Total Weight:", total_weight)
        except FileNotFoundError:
            print(f"File {filename} not found in {folderpath}. Skipping.")
