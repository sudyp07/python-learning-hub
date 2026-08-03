# ========== SET METHODS WITH SINGLE SET EXAMPLE ==========

# Our main set for all examples
my_set = {10, 20, 30, 40, 50}

# 1. add(x) - Add single element
my_set.add(60)                  # {10, 20, 30, 40, 50, 60}

# 2. update(iterable) - Add multiple elements (like extend for sets)
my_set.update([70, 80, 90])     # {10, 20, 30, 40, 50, 60, 70, 80, 90}

# 3. remove(x) - Remove x (ERROR if not found)
my_set.remove(90)               # {10, 20, 30, 40, 50, 60, 70, 80}

# 4. discard(x) - Remove x (NO ERROR if not found)
my_set.discard(100)             # {10, 20, 30, 40, 50, 60, 70, 80} (no error)

# 5. pop() - Remove and return arbitrary element
popped = my_set.pop()           # popped=some random element, set has one less

# 6. clear() - Remove all elements
my_set.clear()                  # set()

# Reset set for remaining examples
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

# 7. union() OR | - Combine sets (returns new set)
union_set = set_a.union(set_b)  # {1, 2, 3, 4, 5, 6, 7, 8}
# OR
union_set = set_a | set_b       # {1, 2, 3, 4, 5, 6, 7, 8}

# 8. intersection() OR & - Common elements (returns new set)
intersection = set_a.intersection(set_b)  # {4, 5}
# OR
intersection = set_a & set_b    # {4, 5}

# 9. difference() OR - - Elements in first but not second (returns new set)
difference = set_a.difference(set_b)  # {1, 2, 3}
# OR
difference = set_a - set_b      # {1, 2, 3}

# 10. symmetric_difference() OR ^ - Elements in either but not both (returns new set)
sym_diff = set_a.symmetric_difference(set_b)  # {1, 2, 3, 6, 7, 8}
# OR
sym_diff = set_a ^ set_b        # {1, 2, 3, 6, 7, 8}

# 11. copy() - Shallow copy
copied_set = set_a.copy()       # {1, 2, 3, 4, 5}

# 12. isdisjoint() - Check if NO common elements
no_common = set_a.isdisjoint({10, 11})  # True (no common elements)
has_common = set_a.isdisjoint({4, 5})   # False (has common elements)

# 13. issubset() OR <= - Check if all elements are in another set
is_subset = set_a.issubset({1, 2, 3, 4, 5, 6})  # True
# OR
is_subset = set_a <= {1, 2, 3, 4, 5, 6}        # True

# 14. issuperset() OR >= - Check if contains all elements of another set
is_superset = set_a.issuperset({1, 2})  # True
# OR
is_superset = set_a >= {1, 2}           # True

# ========== IN-PLACE VERSIONS (Modify original set) ==========
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

set_a.update(set_b)             # set_a = {1, 2, 3, 4, 5, 6, 7, 8}
set_a.intersection_update(set_b)# set_a = {4, 5, 6, 7, 8} (keeps only common)
set_a.difference_update(set_b)  # set_a = set() (removes common elements)
set_a.symmetric_difference_update(set_b)  # set_a = {4, 5} (keeps uncommon)

# ========== BUILT-IN FUNCTIONS ==========
numbers = {3, 1, 4, 1, 5}       # {1, 3, 4, 5} (duplicates removed)
length = len(numbers)           # length=4
max_num = max(numbers)          # max_num=5
min_num = min(numbers)          # min_num=1
total = sum(numbers)            # total=13
sorted_list = sorted(numbers)   # sorted_list=[1, 3, 4, 5] (returns list)

# ========== COMPLETE REFERENCE ==========
# add(x)                      → Add single element
# update(iterable)            → Add multiple elements
# remove(x)                   → Remove x (ERROR if missing)
# discard(x)                  → Remove x (NO ERROR if missing)
# pop()                       → Remove & return arbitrary element
# clear()                     → Remove all elements
# union() OR |                → Combine sets (returns new set)
# intersection() OR &         → Common elements (returns new set)
# difference() OR -           → Elements in first not second (returns new set)
# symmetric_difference() OR ^ → Elements in either but not both (returns new set)
# copy()                      → Shallow copy
# isdisjoint()                → Check if no common elements
# issubset() OR <=            → Check if subset
# issuperset() OR >=          → Check if superset
# intersection_update()       → Keep only common (modifies in-place)
# difference_update()         → Remove common elements (modifies in-place)
# symmetric_difference_update() → Keep uncommon (modifies in-place)

# ========== KEY DIFFERENCES FROM LISTS ==========
# ✓ Sets are UNORDERED - No indexing like list[0]
# ✓ Sets have UNIQUE elements - No duplicates allowed
# ✓ Sets are FASTER for membership testing (in operator)
# ✓ Sets support mathematical operations (union, intersection, etc.)