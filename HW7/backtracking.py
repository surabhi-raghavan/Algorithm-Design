# Function to solve the knapsack problem using backtracking and print each step
def knapsack_backtracking_with_all_steps(weights, profits, capacity, n):
    def backtrack(i, curr_weight, curr_profit, items_included):
        nonlocal max_profit, best_combination
        
        # If we have processed all items or reached capacity
        if i == n or curr_weight > capacity:
            # Print the current state when we reach a leaf of the decision tree
            print(f"Leaf reached - Step {i}, Current weight: {curr_weight}, Current profit: {curr_profit}, Items included: {items_included}")
            return

        # Print current state before including the next item
        print(f"Step {i}, Include item {i + 1}: Current weight: {curr_weight + weights[i]}, Current profit: {curr_profit + profits[i]}, Items included: {items_included + [i + 1]}")
        
        # Include the current item and recurse
        if curr_weight + weights[i] <= capacity:
            items_included.append(i + 1)  # Track the item index (1-based)
            backtrack(i + 1, curr_weight + weights[i], curr_profit + profits[i], items_included)
            items_included.pop()  # Backtrack
        
        # Print current state before excluding the next item
        print(f"Step {i}, Exclude item {i + 1}: Current weight: {curr_weight}, Current profit: {curr_profit}, Items included: {items_included}")
        
        # Exclude the current item and recurse
        backtrack(i + 1, curr_weight, curr_profit, items_included)

    max_profit = 0
    best_combination = []
    backtrack(0, 0, 0, [])
    
    print(f"\nBest profit: {max_profit}, Items included: {best_combination}")

# Items data
weights = [2, 5, 7, 3, 1]  # Weights of the items
profits = [20, 30, 35, 12, 3]  # Profits of the items
capacity = 9  # Maximum weight capacity of the knapsack
n = len(weights)

# Call the function with step printing
knapsack_backtracking_with_all_steps(weights, profits, capacity, n)
