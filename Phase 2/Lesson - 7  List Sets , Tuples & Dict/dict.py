# ========== DICTIONARY METHODS - SHORT & SWEET ==========

my_dict = {'name': 'Alice', 'age': 25, 'city': 'NYC'}

# 1. ACCESSING
my_dict['name']                 # 'Alice' (ERROR if missing)
my_dict.get('name')             # 'Alice' (NO error if missing)
my_dict.get('salary', 0)        # 0 (default value)
my_dict.setdefault('country', 'USA')  # Get or set default

# 2. ADD/UPDATE
my_dict['age'] = 26             # Update existing
my_dict['email'] = 'a@b.com'    # Add new
my_dict.update({'age': 27, 'phone': '123'})  # Merge dict

# 3. REMOVE
my_dict.pop('age')              # Remove & return (ERROR if missing)
my_dict.pop('invalid', None)    # Remove & return default (NO error)
my_dict.popitem()               # Remove & return last pair
del my_dict['city']             # Delete key (ERROR if missing)
my_dict.clear()                 # Remove all

# 4. VIEWS
my_dict.keys()                  # All keys
my_dict.values()                # All values
my_dict.items()                 # All (key,value) pairs

# 5. COPY
my_dict.copy()                  # Shallow copy

# 6. CHECK EXISTENCE
'name' in my_dict               # True (key exists)
'Alice' in my_dict.values()     # True (value exists)

# 7. CREATE DICT
dict.fromkeys(['a','b','c'], 0) # {'a':0, 'b':0, 'c':0}

# 8. DICT COMPREHENSION
{x: x**2 for x in range(5)}     # {0:0, 1:1, 2:4, 3:9, 4:16}
{k: v for k,v in my_dict.items() if v > 20}  # Filter

# 9. MERGE (Python 3.9+)
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}
merged = dict1 | dict2          # {'a':1, 'b':2, 'c':3, 'd':4}
dict1 |= dict2                  # Update in-place

'''
# 10. ITERATION
for key in my_dict:             # Iterate keys
for key, value in my_dict.items():  # Iterate pairs
'''

# ========== QUICK REFERENCE ==========
# get()          → Safe access
# update()       → Merge dicts
# pop()          → Remove & return
# popitem()      → Remove & return last
# keys/values/items() → Views
# copy()         → Shallow copy
# clear()        → Empty dict
# fromkeys()     → Create from list

# ========== BONUS: DEFAULTDICT & COUNTER ==========
from collections import defaultdict, Counter

# Auto-create missing keys
dd = defaultdict(int)           # Default 0
dd['count'] += 1                # Works!

# Count occurrences
Counter(['a','b','a','c','a'])  # {'a':3, 'b':1, 'c':1}