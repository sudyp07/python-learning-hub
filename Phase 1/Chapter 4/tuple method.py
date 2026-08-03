# ============================ TUPLES ============================
# A tuple is an ordered and immutable (unchangeable) collection.
# It can store multiple data types and allows duplicate values.

# Creating Tuples

empty_tuple = ()
print(empty_tuple)                 # Creates an empty tuple                           ()

tup1 = (1)
print(type(tup1))                  # <class 'int'> (This is NOT a tuple)

# IMPORTANT:
# A comma (,) creates a tuple, NOT the parentheses.

tup2 = (1,)
print(type(tup2))                  # <class 'tuple'> (Single-element tuple)

tuple1 = (5, 3, 56, 6, 78, 2, 5, 5, 2, 6, 8, 54, 35, 345, 43, 5, 435, 43, 534, 5, 4)
print(tuple1)

# Tuple Methods (Only 2 because tuples are immutable)

tuple1.count(5)         #5      # Counts how many times 5 appears
tuple1.index(78)        #4      # Returns the index of first occurrence of 78

# ================================================================
# Common Built-in Functions
# ================================================================

len(tuple1)                        # Returns total number of elements                 21
max(tuple1)                        # Returns the largest value                        534
min(tuple1)                        # Returns the smallest value                       2
sum(tuple1)                        # Returns the sum of all elements                  1678
sorted(tuple1)                     # Returns a NEW sorted list                        [2, 2, 3, 4, 5, 5, 5, 5, 5, 6, 6, 8, 35, 43, 43, 54, 56, 78, 345, 435, 534]
tuple(sorted(tuple1))              # Returns a NEW sorted tuple                       (2, 2, 3, 4, 5, 5, 5, 5, 5, 6, 6, 8, 35, 43, 43, 54, 56, 78, 345, 435, 534)
tuple(reversed(tuple1))            # Returns a NEW reversed tuple                     (4, 5, 534, 43, 435, 5, 43, 345, 35, 54, 8, 6, 2, 5, 5, 2, 78, 6, 56, 3, 5)
any(tuple1)                        # True (if at least one value is True)              True
all(tuple1)                        # True (if all values are True)                     True

# ================================================================
# Tuple Operations
# ================================================================

tuple1 = (5, 3, 56, 6, 78)
tuple2 = (1, 2, 3)

# -------------------- Concatenation --------------------

tuple1 + tuple2                    # Joins two tuples                   # (5, 3, 56, 6, 78, 1, 2, 3)

# -------------------- Repetition -----------------------

tuple2 * 3                         # Repeats the tuple 3 times          # (1, 2, 3, 1, 2, 3, 1, 2, 3)

# -------------------- Membership -----------------------

78 in tuple1                       # Checks whether 78 exists                         True
100 in tuple1                      # Checks whether 100 exists                        False

# -------------------- Indexing -------------------------

tuple1[0]                          # First element                                   5
tuple1[2]                          # Element at index 2                              56
tuple1[-1]                         # Last element                                    78
tuple1[-2]                         # Second-last element                             6

# -------------------- Slicing --------------------------

tuple1[1:4]                        # Elements from index 1 to 3                      (3, 56, 6)
tuple1[:3]                         # From beginning to index 2                       (5, 3, 56)
tuple1[2:]                         # From index 2 to end                             (56, 6, 78)
tuple1[:]                          # Copy of the entire tuple                        (5, 3, 56, 6, 78)
tuple1[::-1]                       # Reverse using slicing                           (78, 6, 56, 3, 5)

# ================================================================
# Tuple Packing & Unpacking
# ================================================================

student = ("Sudip", 20, "Nepal")   # Packing

name, age, country = student       # Unpacking

print(name)                        # Sudip
print(age)                         # 20
print(country)                     # Nepal


# ================================================================
# Nested Tuples
# ================================================================

student = ("Sudip", (90, 85, 88))

print(student[0])                  # Sudip
print(student[1])                  # (90, 85, 88)
print(student[1][0])               # 90


# ================================================================
# Type Conversion
# ================================================================

tuple([1, 2, 3])                   # Converts a list into a tuple
list((1, 2, 3))                    # Converts a tuple into a list

# ================================================================
# Deleting a Tuple
# ================================================================

temp = (1, 2, 3)

del temp                           # Deletes the entire tuple

# print(temp)
# NameError: name 'temp' is not defined


