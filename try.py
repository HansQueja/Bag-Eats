def knapsack(budget, item_id, weight, value, food_type, n):
    # Create the table
    table = [[0 for x in range(budget + 1)] for x in range(n + 1)]

    # Fill the table
    for row in range(1, n + 1):
        for column in range(1, budget + 1):
            if weight[row - 1] <= column:
                table[row][column] = max(value[row - 1] + table[row - 1][column - weight[row - 1]], table[row - 1][column])
            else:
                table[row][column] = table[row - 1][column]

    # Backtrack to find the solution
    row_counter = n
    col_counter = budget
    results = []
    food_types = set()

    while row_counter > 0 and col_counter > 0:
        if table[row_counter][col_counter] != table[row_counter - 1][col_counter]:
            current_food_type = food_type[row_counter - 1]
            
            if current_food_type not in food_types:
                results.append(item_id[row_counter - 1])
                food_types.add(current_food_type)
                col_counter -= weight[row_counter - 1]
            
            row_counter -= 1
        else:
            row_counter -= 1

    return results

# Example usage
budget = 100
item_id = [1, 2, 3, 4, 5]
weight = [20, 30, 40, 25, 35]
value = [40, 50, 60, 45, 55]
food_type = ['A', 'B', 'A', 'C', 'B']
n = len(item_id)

recommended_items = knapsack(budget, item_id, weight, value, food_type, n)
print("Recommended items:", recommended_items)