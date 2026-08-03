# list is the collections of similar values inside a single variable of any datatypes#
list_format = []

#list are mutable that means you can change the values inside the list :)
fruits = ["apple", "banana", "cherry", "grape", "mango"]
print(fruits) # ["apple", "banana", "cherry", "grape", "mango"]
fruits[0] = "Pineapple"
print(fruits) # ['Pineapple', 'banana', 'cherry', 'grape', 'mango'], CASUE WE CHANGED VALUE OF INDEX 0 FROM apple to Pineapple.

#retrive the data of list using index number
print(fruits[0]) #Pineapple
print(fruits[1]) #banana
print(fruits[2]) #cherry
print(fruits[3]) #grape
print(fruits[4]) #mango
print(fruits[1:4]) # ["banana", "cherry", "grape"}

# ================================================================
# IMPORTANT POINTS TO REMEMBER
# ================================================================

# ✔ Lists are ordered.
# ✔ Lists are mutable (can be modified after creation).
# ✔ Lists allow duplicate values.
# ✔ Lists can store multiple data types.
# ✔ Lists are slower than tuples (slightly, due to mutability).
# ✔ Lists are created using square brackets [].
# ✔ Lists support indexing and slicing.
# ✔ Lists can contain other lists (nested lists).
# ✔ Lists are one of the most commonly used Python data structures.
