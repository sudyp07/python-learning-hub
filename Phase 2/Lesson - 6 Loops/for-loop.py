"""
execute  a block of code  a fixed number of times.
You can iterate over a range, string and any sequence
"""
## Regular loop (Normal loop that prints from 1 to 10)
for x in range(1,11):
    print(x)                              ## It goes from 1 to all the way to 10


## FOR REVERESE LOOP (use this reverse() function)
for i in reversed(range(1,11)):
    print(i)                            ## It goes from 10 to all the way to 1


## JUMPING LOOP ( start : end : Jump)

for x in range(1,21,3):
    print(x)      ## it will take number from 1- 20 @ first and jumps 3 steps each time till it reaches the last number possible.

