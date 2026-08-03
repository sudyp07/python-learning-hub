#extraordinary for loops with else:
from unittest import result

list1 = [55,77,99,33,55,88,44,2,4,5]

for item in list1:
    print(item)  #it runs first properly
else:
    print("Done loop") # it runs once aftet above loops ends


# result:
# 55
# 77
# 99
# 33
# 55
# 88
# 44
# 2
# 4
# 5
# Done loop