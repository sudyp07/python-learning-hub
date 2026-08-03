# ========== TUPLE METHODS (ONLY 2 METHODS!) ==========

# Tuples are IMMUTABLE - cannot be changed after creation!
# That's why they have only 2 methods compared to lists

# ========== SINGLE ELEMENT TUPLE (IMPORTANT!) ==========
# Correct way (with comma)
single_tuple = (5,)             # (5,) - This is a tuple
print(type(single_tuple))       # <class 'tuple'>

# Wrong way (without comma)
not_a_tuple = (5)               # 5 - This is an integer!
print(type(not_a_tuple))        # <class 'int'>

# Empty tuple
empty_tuple = ()                # () - Empty tuple

# Our main tuple for examples
my_tuple = (10, 20, 30, 20, 40, 20, 50)

# 1. count(x) - Count occurrences of x
cnt = my_tuple.count(20)        # cnt=3 (20 appears 3 times)
cnt = my_tuple.count(100)       # cnt=0 (no error, just returns 0)

# 2. index(x, start, end) - Find first index of x
idx = my_tuple.index(30)        # idx=2 (30 is at index 2)
idx = my_tuple.index(20)        # idx=1 (first 20 at index 1)
idx = my_tuple.index(20, 2)     # idx=3 (search from index 2 onward)
idx = my_tuple.index(20, 2, 5)  # idx=3 (search between index 2 to 5)

# ========== BUILT-IN FUNCTIONS ==========
numbers = (3, 1, 4, 1, 5, 9)
length = len(numbers)           # length=6
max_num = max(numbers)          # max_num=9
min_num = min(numbers)          # min_num=1
total = sum(numbers)            # total=23
sorted_list = sorted(numbers)   # sorted_list=[1, 1, 3, 4, 5, 9] (returns list)
reversed_tuple = tuple(reversed(numbers))  # reversed_tuple=(9, 5, 1, 4, 1, 3)
any_true = any(numbers)         # any_true=True (checks if any element is True)
all_true = all(numbers)         # all_true=True (checks if all elements are True)

# ========== TUPLE OPERATIONS ==========
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)

# Concatenation (+)
combined = tuple1 + tuple2      # (1, 2, 3, 4, 5, 6)

# Repetition (*)
repeated = tuple1 * 3           # (1, 2, 3, 1, 2, 3, 1, 2, 3)

# Membership (in / not in)
is_present = 2 in tuple1        # True
is_present = 5 in tuple1        # False

# Slicing
my_tuple = (10, 20, 30, 40, 50)
slice1 = my_tuple[1:4]          # (20, 30, 40)
slice2 = my_tuple[:3]           # (10, 20, 30)
slice3 = my_tuple[2:]           # (30, 40, 50)
slice4 = my_tuple[::-1]         # (50, 40, 30, 20, 10) (reverse)

# Unpacking
a, b, c = (1, 2, 3)             # a=1, b=2, c=3
a, *rest = (1, 2, 3, 4)         # a=1, rest=[2, 3, 4]
a, b, *rest = (1, 2, 3, 4, 5)   # a=1, b=2, rest=[3, 4, 5]

# ========== CONVERTING TO/FROM TUPLE ==========
# List to Tuple
my_list = [1, 2, 3, 4]
tuple_from_list = tuple(my_list)  # (1, 2, 3, 4)

# Tuple to List
my_tuple = (1, 2, 3, 4)
list_from_tuple = list(my_tuple)  # [1, 2, 3, 4]

# String to Tuple
string_tuple = tuple("hello")     # ('h', 'e', 'l', 'l', 'o')

# Tuple to String
char_tuple = ('h', 'e', 'l', 'l', 'o')
string_from_tuple = ''.join(char_tuple)  # "hello"

# ========== COMPLETE REFERENCE ==========
# count(x)           → Count occurrences of x
# index(x, start, end) → Find first index of x (ERROR if missing)

# ========== KEY DIFFERENCES FROM LISTS ==========
# ✓ Tuples are IMMUTABLE - Cannot add, remove, or change elements
# ✓ Tuples are FASTER than lists (less memory)
# ✓ Tuples can be used as dictionary KEYS (lists cannot)
# ✓ Tuples are SAFER for data that shouldn't change
# ✓ Tuples use parentheses () instead of square brackets []

# ========== WHEN TO USE TUPLES VS LISTS ==========
# Use Tuple when:
#   - Data should NEVER change (e.g., days of week, coordinates)
#   - You need a dictionary key
#   - You want better performance
#   - You're returning multiple values from a function

# Use List when:
#   - Data needs to change (add, remove, modify)
#   - You need dynamic size
#   - You need methods like append(), extend(), etc.

