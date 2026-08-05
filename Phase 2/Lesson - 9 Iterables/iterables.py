## Iterables --> An collection that can return its element on at a time, allowing it to be iterated over in a loop
## strings,list, tuple and list all are iterables like below :)

numbers = [1,2,3,4,5] # --> lists
for number in reversed(numbers):  # it can be reversed
    print(number)

tup_numbers = (1,2,3,4,5)# --> tuple
for number in reversed(tup_numbers): # it can be reversed
    print(number)

set_number  = {1,2,3,4,5}# --> sets
for number in set_number: # it cannot be reversed
    print(number)

name = "Sudeep Hero"# --> Strings
for character in name:
    print(character, end=" ")   # S u d e e p   H e r o
print()

## Dictionary method to retrive data 

my_dict = {"A": "META" , "B" :"GOODLE", "C": "APPLE"}

for value in my_dict.values():
    print(value) ## it will just print values like META, GOOGLE AND APPLE

for key in my_dict.keys():
    print(key) ## it will just print keys like A , B, C

for key, value in my_dict.items():
    print(f'{key} : {value}')

"""
A : META
B : GOODLE
C : APPLE
"""