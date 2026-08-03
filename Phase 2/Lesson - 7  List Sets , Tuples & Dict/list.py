# ========== LIST METHODS WITH SINGLE LIST EXAMPLE ==========

# Our main list for all examples
my_list = [10, 20, 30, 40, 50]

# 1. append(x) - Add item to end
my_list.append(60)              # [10, 20, 30, 40, 50, 60]

# 2. extend(iterable) - Add multiple items
my_list.extend([70, 80])        # [10, 20, 30, 40, 50, 60, 70, 80]

# 3. insert(index, x) - Insert at specific position
my_list.insert(2, 25)           # [10, 20, 25, 30, 40, 50, 60, 70, 80]

# 4. remove(x) - Remove first occurrence
my_list.remove(25)              # [10, 20, 30, 40, 50, 60, 70, 80]

# 5. pop(index) - Remove & return item (default: last)
popped = my_list.pop()          # popped=80, list=[10, 20, 30, 40, 50, 60, 70]
popped_first = my_list.pop(0)   # popped_first=10, list=[20, 30, 40, 50, 60, 70]

# 6. clear() - Remove all items
my_list.clear()                 # []

# Reset list for remaining examples
my_list = [10, 20, 30, 20, 40, 20]

# 7. index(x) - Find first index
idx = my_list.index(20)         # idx=1 (first 20 at index 1)

# 8. count(x) - Count occurrences
cnt = my_list.count(20)         # cnt=3

# 9. sort() - Sort in-place
my_list.sort()                  # [10, 20, 20, 20, 30, 40]
my_list.sort(reverse=True)      # [40, 30, 20, 20, 20, 10]

# 10. reverse() - Reverse in-place
my_list.reverse()               # [10, 20, 20, 20, 30, 40]

# 11. copy() - Shallow copy
copied_list = my_list.copy()    # copied_list=[10, 20, 20, 20, 30, 40]

# ========== BUILT-IN FUNCTIONS ==========
numbers = [3, 1, 4, 1, 5]
length = len(numbers)           # length=5
max_num = max(numbers)          # max_num=5
min_num = min(numbers)          # min_num=1
total = sum(numbers)            # total=14
sorted_list = sorted(numbers)   # sorted_list=[1, 1, 3, 4, 5] (new list)
reversed_list = list(reversed(numbers))  # reversed_list=[5, 1, 4, 1, 3] (new list)

# ========== COMPLETE REFERENCE ==========
# append(x)        → Add x to end
# extend(iter)     → Add all from iterable
# insert(i, x)     → Insert x at index i
# remove(x)        → Remove first x (ERROR if missing)
# pop(i)           → Remove & return item at i (default: last)
# clear()          → Remove all items
# index(x)         → Return first index of x (ERROR if missing)
# count(x)         → Count occurrences of x
# sort()           → Sort in-place (ascending/descending)
# reverse()        → Reverse in-place
# copy()           → Shallow copy