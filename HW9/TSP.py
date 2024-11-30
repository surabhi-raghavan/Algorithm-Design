import itertools
import heapq

# Define the updated graph as an adjacency matrix with the new weights
graph = {
    (1, 2): 5, (1, 3): 8, (2, 3): 4, (2, 5): 4, (3, 4): 2, (3, 7): 5,
    (4, 8): 7, (8, 7): 4, (8, 6): 5, (7, 4): 3, (7, 6): 8, (6, 2): 6,
    (6, 5): 2, (5, 1): 1
}

# Since the graph is undirected, add the reverse edges
for (i, j), weight in list(graph.items()):
    graph[(j, i)] = weight

# List of vertices
vertices = [1, 2, 3, 4, 5, 6, 7, 8]

# Helper function to calculate tour length
def calculate_tour_length(tour):
    length = 0
    for i in range(len(tour) - 1):
        edge = (tour[i], tour[i + 1])
        length += graph.get(edge, float('inf'))  # Large penalty for missing edges
    # Return to starting node
    length += graph.get((tour[-1], tour[0]), float('inf'))
    return length

# Branch-and-Bound approach with detailed logging
def branch_and_bound_tsp():
    min_length = float('inf')
    optimal_tour = None
    steps = 0

    # Priority queue to keep nodes with bounds (path, bound, level)
    pq = []
    
    # Calculate initial bound (sum of the smallest outgoing edges from each vertex)
    initial_bound = sum(min(graph.get((i, j), float('inf')) for j in vertices if j != i) for i in vertices)
    
    # Push initial node to the queue
    heapq.heappush(pq, (initial_bound, [1]))  # Start from node 1
    print(f"Initial Step:\n- Step {steps}: Exploring node at level 0 with path [v1] and bound {initial_bound}")
    
    while pq:
        bound, path = heapq.heappop(pq)
        level = len(path) - 1
        print(f"\nProcessing Step {steps}: Exploring node at level {level} with path {[f'v{i}' for i in path]} and bound {bound}")
        steps += 1

        # If path is a complete tour, check length
        if level == len(vertices) - 1:
            tour_length = calculate_tour_length(path + [1])
            if tour_length < min_length:
                min_length = tour_length
                optimal_tour = path + [1]
                print(f"- Complete tour found: {[f'v{i}' for i in optimal_tour]} with length {tour_length}")
                print(f"- New optimal tour: {[f'v{i}' for i in optimal_tour]} with length {min_length}")
            continue

        # Explore next vertices
        for vertex in vertices:
            if vertex not in path:
                new_path = path + [vertex]
                new_bound = calculate_tour_length(new_path)
                if new_bound < min_length:
                    heapq.heappush(pq, (new_bound, new_path))
                    print(f"- Pushed node with path {[f'v{i}' for i in new_path]} and bound {new_bound} to the queue")
                else:
                    print(f"- Pruned path {[f'v{i}' for i in new_path]} with bound {new_bound} (exceeds min length {min_length})")

    print("\nFinal Solution:")
    print(f"- Optimal Tour: {[f'v{i}' for i in optimal_tour]}")
    print(f"- Minimum Length of the Tour: {min_length}")

# Run the branch-and-bound TSP with detailed steps
branch_and_bound_tsp()
