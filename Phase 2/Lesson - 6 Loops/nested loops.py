# Nested loops = a loop within another loop (outer and inner basically)

# normal loops in single line output
for x in range(1,10):
    print(x, end=" ")  # print from 1 to 9 in same line like this  1 2 3 4 5 6 7 8 9

# loops inside loops
for x in range(4):
    for i in range(7):
            print(i, end=" ") ## print from 0 to 6 ( three times like below)
    print()
## OUTPUT
"""
0 1 2 3 4 5 6 
0 1 2 3 4 5 6 
0 1 2 3 4 5 6 
"""