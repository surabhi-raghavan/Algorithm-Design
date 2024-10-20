import sys
import time

INF = float('inf')
MAX_NODES = 2000

class Matrix:
    def __init__(self, size):
        self.size = size
        self.data = tuple (tuple (INF for _ in range(size)) for _ in range(size))
        
    def set(self, i, j, value):
        row = list(self.data[i])
        row[j] = value
        self.data = self.data [:i] + (tuple (row), ) +self.data [i+1 :]
        
    def get(self, i, j):
        return self.data[i][j]
    
def djikstra(graph, src, num_nodes):
    distance = [INF] * num_nodes
    previous = [-1] * num_nodes
    visited = [False] * num_nodes
    
    distance[src] = 0
    
    for _ in range (num_nodes):
        u = -1
        minimum_distance = INF
        
        for i in range (num_nodes):
            if not visited[i] and distance[i] < minimum_distance:
                minimum_distance = distance[i]
                u = i 
                
        if u == -1:
            break
        
        visited[u] = True
        
        for v in range(num_nodes):
            if not visited[v]:
                weight = graph.get(u, v)
                if weight != INF and distance[u] + weight <distance[v]:
                    distance[v] = distance[u] + weight
                    previous[v] = u
    return distance, previous

def path(previous, destination):
    if previous[destination] == -1:
        print(destination, end = '')
    else: 
        path(previous, previous[destination])
        print(f' -> {destination}', end='')

def main(input_file):
    
     
        