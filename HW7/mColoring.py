import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# Graph adjacency matrix (6 vertices)
adj_matrix = [
    [0, 1, 0, 1, 0, 0],
    [1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 1, 0],
    [1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 1, 0]
]

colors = ['Red', 'Green', 'White']
n = 6  # Number of vertices
state_id = 0

# To store the decision tree
G = nx.DiGraph()

# To store matrices of color assignments for each state
state_matrices = {}

def is_safe(v, color_assignment, color, adj_matrix):
    """Check if it's safe to assign color to vertex v"""
    for i in range(len(adj_matrix)):
        if adj_matrix[v][i] == 1 and color_assignment[i] == color:
            return False
    return True

def generate_matrix(color_assignment):
    """Generate a matrix representation of the current state"""
    return np.array([[f'{colors[color]}' if color != -1 else 'None' for color in color_assignment]])

def backtrack(v, color_assignment):
    global state_id
    
    if v == n:
        # All vertices are colored, store solution
        state_id += 1
        solution_label = f'Solution {state_id}'
        G.add_node(solution_label)
        state_matrices[solution_label] = generate_matrix(color_assignment)
        return True
    
    for color_index, color in enumerate(colors):
        if is_safe(v, color_assignment, color_index, adj_matrix):
            color_assignment[v] = color_index  # Assign color

            # Add current state to the tree
            current_state = f'v{v+1}={color}'
            previous_state = f'v{v}={colors[color_assignment[v-1]]}' if v > 0 else 'Start'
            G.add_edge(previous_state, current_state)
            state_matrices[current_state] = generate_matrix(color_assignment)
            
            # Recur to assign colors to the rest
            if backtrack(v + 1, color_assignment):
                state_id += 1

            # Backtrack (reset the color)
            color_assignment[v] = -1

    return False

# Initialize the color assignment list (-1 means no color assigned)
color_assignment = [-1] * n

# Generate the state space tree and matrices
backtrack(0, color_assignment)

# Add hierarchical levels to nodes for the multipartite layout
for node in G.nodes():
    if node == "Start":
        G.nodes[node]['subset'] = 0
    elif "v1" in node:
        G.nodes[node]['subset'] = 1
    elif "v2" in node:
        G.nodes[node]['subset'] = 2
    elif "v3" in node:
        G.nodes[node]['subset'] = 3
    elif "v4" in node:
        G.nodes[node]['subset'] = 4
    elif "v5" in node:
        G.nodes[node]['subset'] = 5
    elif "v6" in node:
        G.nodes[node]['subset'] = 6
    elif "Solution" in node:
        G.nodes[node]['subset'] = 7
    else:
        G.nodes[node]['subset'] = 8  # Conflicts or backtracking steps

# Now apply multipartite layout
pos = nx.multipartite_layout(G, subset_key="subset")

# Plot the tree


# Output matrices for each state
for state, matrix in state_matrices.items():
    print(f"State: {state}")
    print(matrix)
    print("\n")
