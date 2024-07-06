
def knapsack(budget, item_id, weight, value, n):

    # this is to create a table with budget number of columns, and n number of rows
    table = [[0 for x in range(budget + 1)] for x in range(n + 1)]

    # this is to iterate through all rows
    for row in range(n + 1):

        # this is to iterate through each column
        for column in range(budget + 1):

            # if it is row 0 or column 0, just put zeroes
            if row == 0 or column == 0:
                table[row][column] = 0

            # if the current candidate price is lower or equal than current column price, go inside
            elif weight[row - 1] <= column:
                # we will be getting the maximum value from the following:
                # - rating of current candidate and the other item that fits the budget 
                # - the previous best rating for the given price
                table[row][column] = max(value[row - 1] + table[row - 1][column - weight[row - 1]], table[row - 1][column])
            # if the current candidate price is greater than the budget, just copy the previous best value.
            else:
                table[row][column] = table[row - 1][column]

    # set counters for the end of the table for iteration
    row_counter = n
    col_counter = budget

    # this will store the ids of items that will be recommended
    results = []

    # while there are valid recommendations still, iterate through the table
    while row_counter > 0 and col_counter > 0:

        # if the current value and the value on the left is the same, go left
        if table[row_counter][col_counter] == table[row_counter - 1][col_counter]:
            row_counter -= 1
        # if the cur value and value on top is same, go top
        elif table[row_counter][col_counter] == table[row_counter][col_counter - 1]:
            col_counter -= 1
        # if value is unique from its left and top counterparts, append it
        else:
            results.append(item_id[row_counter - 1])

            # subtract the weight of the recommended item to the column counter
            col_counter -= weight[row_counter - 1]
            row_counter -= 1
    
    return results
