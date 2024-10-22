import numpy as np

adj_matrix = [
    [0, 1, 0, 1, 0, 0],
    [1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 0]
]

colors = ['Red', 'Green', 'White']
n = 6  # Number of vertices
state_id = 0  # Counter for solution number

state_matrices = {}  # Dictionary to store solutions


def is_safe(v, color_assignment, color, adj_matrix):
    # Check if adjacent vertices have the same color
    for i in range(len(adj_matrix)):
        if adj_matrix[v][i] == 1 and color_assignment[i] == color:
            return False
    return True


def generate_matrix(color_assignment):
    # Generate a matrix showing the current color assignment
    return np.array([[f'{colors[color]}' if color != -1 else 'None' for color in color_assignment]])


def backtrack(v, color_assignment):
    global state_id
    
    if v == n:
        # All vertices are colored, store the solution
        state_id += 1
        solution_label = f'Solution {state_id}'
        state_matrices[solution_label] = generate_matrix(color_assignment)
        return True
    
    found_solution = False
    
    for color_index in range(len(colors)):
        if is_safe(v, color_assignment, color_index, adj_matrix):
            color_assignment[v] = color_index  # Assign the color
            
            if backtrack(v + 1, color_assignment):  # Move to the next vertex
                found_solution = True  # Mark that we found a solution

            color_assignment[v] = -1  # Reset the color if it doesn't work

    return found_solution


# Initial color assignment: -1 means uncolored
color_assignment = [-1] * n

# Start the backtracking algorithm
backtrack(0, color_assignment)

# Output only matrices for each solution
for state, matrix in state_matrices.items():
    print(f"State: {state}")
    print(matrix)
    print("\n")
