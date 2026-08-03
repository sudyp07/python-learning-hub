# breaking the loops (exit loops)
for i in range (10):
    if(i == 6):
        break  # it exits the loops right now it means it will print from 0 to 5 and exits :)
    print(i)

# continue the loops  (break the iteration at particular point)
for i in range (10):
    if(i == 4):
        continue  #it just skips the iteration when i = 4,it means it will print from 1 to 9 but not 4 (skips 4)
    print(i)

# pass the loops
for i in range (10):
        pass   # with the pass statement it helps to run loops and program without error 
else:
    print("Goodbye")