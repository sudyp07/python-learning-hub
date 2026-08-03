frutits = ['apple', "banana", 'coconut', 'grapes']
vegetables = ['celery','carrot', 'potato']
meats = ['buff', 'mutton', 'fish', 'turkey']

groceries = [frutits,vegetables,meats]

print(groceries[2][3]) # turkey
print(groceries[0][2]) # coconut
print(groceries[1][1]) # carrot
print(groceries[2][0]) # buff

for collection in groceries:
    for food in collection:
        print(food, end = " ")
    print()
'''
apple banana coconut grapes 
celery carrot potato 
buff mutton fish turkey 
'''
# ========== COMPLETE REFERENCE ==========
# Creating:      [[1,2], [3,4]]
# Access:        matrix[row][col]
# Modify:        matrix[row][col] = value
# Rows:          len(matrix)
# Columns:       len(matrix[0])
# Add row:       matrix.append([1,2,3])
# Delete row:    del matrix[0]
# Iterate:       for row in matrix: for item in row:
# Transpose:     [[row[i] for row in matrix] for i in range(cols)]
# Flatten:       [item for row in matrix for item in row]