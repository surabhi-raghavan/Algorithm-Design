import sys
import time

INF = float('inf')
MAX_NODES = 2000

class Matrix:
    def set(self, i, j, value):
        row = list(self.data[i])
        row[j] = value
        self.data = self.data [:i] + (tuple (row), ) +self.data [i+1 :]
        
    def get(self, i, j):
        return self.data[i][j]
    
    def djikstra(graph, src, num_nodes):
        
        
