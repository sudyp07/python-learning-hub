# Python Collections Master Guide

> A complete beginner-to-advanced guide to Python **lists**, **tuples**, **sets**, and **dictionaries**—including every public built-in method, practical examples, comparisons, performance notes, common mistakes, exercises, and mastery tips.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Topic](https://img.shields.io/badge/Topic-Data%20Structures-2E8B57)](#)
[![Level](https://img.shields.io/badge/Level-Beginner%20to%20Advanced-orange)](#)

---

## Table of Contents

1. [Why Collections Matter](#1-why-collections-matter)
2. [Quick Comparison](#2-quick-comparison)
3. [Lists](#3-lists)
4. [Tuples](#4-tuples)
5. [Sets](#5-sets)
6. [Dictionaries](#6-dictionaries)
7. [Operations Shared by Collections](#7-operations-shared-by-collections)
8. [Comprehensions](#8-comprehensions)
9. [Mutability, Identity, and Copying](#9-mutability-identity-and-copying)
10. [Nested Collections](#10-nested-collections)
11. [Time-Complexity Guide](#11-time-complexity-guide)
12. [How to Choose the Correct Collection](#12-how-to-choose-the-correct-collection)
13. [Common Mistakes and Their Fixes](#13-common-mistakes-and-their-fixes)
14. [Clean-Code and Safety Tips](#14-clean-code-and-safety-tips)
15. [Practice Exercises](#15-practice-exercises)
16. [Mini-Projects](#16-mini-projects)
17. [Mastery Roadmap](#17-mastery-roadmap)
18. [Final Cheat Sheet](#18-final-cheat-sheet)
19. [Official References](#19-official-references)

---

## 1. Why Collections Matter

A collection stores multiple values inside one variable. Choosing the correct collection makes a program clearer, faster, safer, and easier to maintain.

Python's four core collection types solve different problems:

- A **list** stores an ordered sequence that may change.
- A **tuple** stores an ordered sequence that should not change.
- A **set** stores unique values and provides fast membership testing.
- A **dictionary** connects unique keys to values.

Collections are used almost everywhere: user records, shopping carts, API responses, configuration settings, database results, log analysis, cybersecurity tools, machine-learning datasets, and much more.

### Learning outcomes

After completing this guide, you should be able to:

- create, access, update, and delete collection items;
- use every public method of `list`, `tuple`, `set`, and `dict`;
- explain ordering, duplicates, mutability, and hashability;
- write collection comprehensions and nested structures;
- avoid aliasing and shallow-copy mistakes;
- estimate the performance of common operations; and
- choose the best collection for a real problem.

---

## 2. Quick Comparison

| Feature | List | Tuple | Set | Dictionary |
|---|---|---|---|---|
| Example | `[1, 2, 3]` | `(1, 2, 3)` | `{1, 2, 3}` | `{"a": 1, "b": 2}` |
| Ordered | Yes | Yes | No positional order | Yes, insertion order |
| Indexed by position | Yes | Yes | No | No; accessed by key |
| Mutable | Yes | No | Yes | Yes |
| Allows duplicate items | Yes | Yes | No | Values: yes; keys: no |
| Supports slicing | Yes | Yes | No | No |
| Typical purpose | Changing sequence | Fixed record | Unique items | Key-value lookup |
| Empty syntax | `[]` | `()` | `set()` | `{}` |

> **Important:** “Ordered” does not mean “sorted.” Lists, tuples, and dictionaries preserve a meaningful order, but Python does not automatically sort their contents.

### The four key questions

Before choosing a collection, ask:

1. Must every item be unique?
2. Do I need key-based lookup?
3. Does position or insertion order matter?
4. Should the collection be allowed to change?

---

## 3. Lists

A list is an **ordered, mutable sequence**. It allows duplicates and can contain values of different types, although consistently typed contents are usually easier to understand.

### 3.1 Creating lists

```python
empty = []
numbers = [10, 20, 30]
mixed = [1, "Python", True, 3.14]
from_iterable = list(range(5))       # [0, 1, 2, 3, 4]
characters = list("cat")            # ['c', 'a', 't']
```

### 3.2 Accessing, slicing, and updating

```python
languages = ["Python", "Java", "C++", "Go"]

print(languages[0])       # Python
print(languages[-1])      # Go
print(languages[1:3])     # ['Java', 'C++']
print(languages[:2])      # ['Python', 'Java']
print(languages[::2])     # ['Python', 'C++']
print(languages[::-1])    # reversed copy

languages[1] = "Rust"
languages[2:4] = ["Kotlin", "Swift"]
```

The general slice form is:

```python
sequence[start:stop:step]
```

`start` is included, `stop` is excluded, and omitted values use sensible defaults.

### 3.3 Every list method

| Method | Purpose | Changes the list? | Important result/error |
|---|---|---:|---|
| `append(x)` | Add one item at the end | Yes | Returns `None` |
| `extend(iterable)` | Add every item from an iterable | Yes | Returns `None` |
| `insert(i, x)` | Insert before index `i` | Yes | Returns `None` |
| `remove(x)` | Remove first matching value | Yes | `ValueError` if absent |
| `pop([i])` | Remove and return an item | Yes | Default index is `-1` |
| `clear()` | Remove every item | Yes | Returns `None` |
| `index(x[, start[, stop]])` | Find first matching index | No | `ValueError` if absent |
| `count(x)` | Count equal values | No | Returns an integer |
| `sort(key=None, reverse=False)` | Sort in place | Yes | Returns `None` |
| `reverse()` | Reverse in place | Yes | Returns `None` |
| `copy()` | Create a shallow copy | No | Returns a new list |

#### `append(x)`

Adds exactly **one object** to the end.

```python
tasks = ["study"]
tasks.append("exercise")
tasks.append(["email", "backup"])

print(tasks)
# ['study', 'exercise', ['email', 'backup']]
```

#### `extend(iterable)`

Adds each item from an iterable.

```python
tasks = ["study"]
tasks.extend(["exercise", "email"])
print(tasks)  # ['study', 'exercise', 'email']
```

`append()` versus `extend()`:

```python
a = [1, 2]
a.append([3, 4])     # [1, 2, [3, 4]]

b = [1, 2]
b.extend([3, 4])     # [1, 2, 3, 4]
```

#### `insert(i, x)`

Inserts an item before a given index.

```python
names = ["Asha", "Chetan"]
names.insert(1, "Bikash")
print(names)  # ['Asha', 'Bikash', 'Chetan']
```

Frequent insertion at the beginning is slow because existing elements must shift. For a queue, prefer `collections.deque`.

#### `remove(x)`

Removes the first item equal to `x`.

```python
scores = [70, 85, 70, 90]
scores.remove(70)
print(scores)  # [85, 70, 90]
```

Safe removal when absence is acceptable:

```python
if 100 in scores:
    scores.remove(100)
```

#### `pop([i])`

Removes and returns the item at index `i`. Without an index, it removes the last item.

```python
stack = ["first", "second", "third"]
last = stack.pop()       # 'third'
first = stack.pop(0)     # 'first'
print(stack)             # ['second']
```

#### `clear()`

Removes all items while keeping the same list object.

```python
records = [1, 2, 3]
records.clear()
print(records)  # []
```

#### `index(x[, start[, stop]])`

Returns the index of the first matching value.

```python
colors = ["red", "blue", "green", "blue"]
print(colors.index("blue"))        # 1
print(colors.index("blue", 2))     # 3
print(colors.index("blue", 2, 4))  # 3
```

#### `count(x)`

Counts how many items are equal to `x`.

```python
votes = ["yes", "no", "yes", "yes"]
print(votes.count("yes"))  # 3
```

For counting many different values, use `collections.Counter` instead of repeatedly calling `count()`.

#### `sort(key=None, reverse=False)`

Sorts the original list in place.

```python
numbers = [4, 1, 10, 3]
numbers.sort()
print(numbers)  # [1, 3, 4, 10]

numbers.sort(reverse=True)
print(numbers)  # [10, 4, 3, 1]
```

Custom sort key:

```python
students = [
    {"name": "Maya", "score": 82},
    {"name": "Aarav", "score": 91},
    {"name": "Nima", "score": 82},
]

students.sort(key=lambda student: (-student["score"], student["name"]))
```

Use `sorted(iterable)` when you want a new list and must preserve the original:

```python
original = [3, 1, 2]
new_list = sorted(original)
# original: [3, 1, 2]
# new_list: [1, 2, 3]
```

Python sorting is **stable**: items with equal keys keep their previous relative order.

#### `reverse()`

Reverses the original list in place; it does not sort.

```python
values = [1, 2, 3]
values.reverse()
print(values)  # [3, 2, 1]
```

Other choices:

```python
reversed_copy = values[::-1]
iterator = reversed(values)
```

#### `copy()`

Returns a **shallow copy**.

```python
original = [1, 2, 3]
duplicate = original.copy()
duplicate.append(4)

print(original)   # [1, 2, 3]
print(duplicate)  # [1, 2, 3, 4]
```

Nested mutable objects are still shared; see [Mutability, Identity, and Copying](#9-mutability-identity-and-copying).

### 3.4 Adding, changing, and deleting without methods

```python
items = [10, 20, 30]

items += [40, 50]       # extend-like operation
items[0] = 99           # update one item
items[1:3] = [7, 8]     # update a slice
del items[0]            # delete by index
del items[1:3]          # delete a slice
```

### 3.5 Lists as stacks and queues

List as a **LIFO stack**:

```python
stack = []
stack.append("A")
stack.append("B")
print(stack.pop())  # B
```

For a **FIFO queue**, use a deque:

```python
from collections import deque

queue = deque(["A", "B"])
queue.append("C")
print(queue.popleft())  # A
```

### 3.6 List mastery tips

- Use `append()` for one item and `extend()` for several items.
- Use `enumerate()` when both index and item are needed.
- Use `zip()` to traverse related sequences together.
- Use `sorted()` to preserve the original; use `.sort()` to modify it.
- Avoid repeated `insert(0, value)` and `pop(0)` on large lists.
- Never assign the result of an in-place method: `numbers = numbers.sort()` makes `numbers` become `None`.

---

## 4. Tuples

A tuple is an **ordered, immutable sequence**. It supports indexing, slicing, duplicates, iteration, and unpacking, but its item references cannot be added, removed, or reassigned.

### 4.1 Creating tuples

```python
empty = ()
point = (10, 20)
also_a_tuple = 10, 20
single = (5,)             # comma is required
not_a_tuple = (5)         # this is an int
from_iterable = tuple("AI")  # ('A', 'I')
```

> The comma creates a tuple; parentheses mainly improve clarity and control grouping.

### 4.2 Accessing and slicing

```python
rgb = (255, 128, 0)
print(rgb[0])      # 255
print(rgb[-1])     # 0
print(rgb[0:2])    # (255, 128)
```

This is invalid because tuples are immutable:

```python
# rgb[0] = 0  # TypeError
```

### 4.3 Every tuple method

Tuples intentionally have only two public methods.

| Method | Purpose | Important result/error |
|---|---|---|
| `count(x)` | Count values equal to `x` | Returns an integer |
| `index(x[, start[, stop]])` | Find first matching index | `ValueError` if absent |

#### `count(x)`

```python
grades = ("A", "B", "A", "C", "A")
print(grades.count("A"))  # 3
```

#### `index(x[, start[, stop]])`

```python
grades = ("A", "B", "A", "C")
print(grades.index("A"))        # 0
print(grades.index("A", 1))     # 2
print(grades.index("A", 1, 3))  # 2
```

### 4.4 Packing and unpacking

```python
# Packing
user = "Ankita", 21, "Nepal"

# Unpacking
name, age, country = user
```

Extended unpacking:

```python
first, *middle, last = (10, 20, 30, 40, 50)

print(first)   # 10
print(middle)  # [20, 30, 40]
print(last)    # 50
```

Swapping uses tuple packing and unpacking:

```python
a, b = 10, 20
a, b = b, a
```

Returning multiple values:

```python
def minimum_and_maximum(numbers):
    return min(numbers), max(numbers)

low, high = minimum_and_maximum([8, 2, 10, 5])
```

### 4.5 Immutability versus hashability

A tuple is immutable, but it is hashable only when **all of its elements are hashable**.

```python
valid_key = {(27.7, 85.3): "Kathmandu"}

# invalid_key = {([27.7, 85.3], "location"): "Kathmandu"}
# TypeError: the tuple contains a list, which is unhashable
```

A tuple may contain a mutable object; that inner object can still change:

```python
data = ([1, 2], "fixed label")
data[0].append(3)
print(data)  # ([1, 2, 3], 'fixed label')
```

### 4.6 When tuples are useful

- fixed coordinates such as `(latitude, longitude)`;
- database rows and small records;
- returning several values from a function;
- dictionary keys made entirely of hashable values;
- values that should communicate “do not modify”; and
- safe unpacking of structured results.

For records where field names matter, consider `typing.NamedTuple`, `collections.namedtuple`, or a `dataclass`.

### 4.7 Tuple mastery tips

- Remember the comma in a one-item tuple: `(value,)`.
- Prefer unpacking to unexplained numeric indexes.
- Use tuples to express fixed structure, not merely to prevent accidental editing.
- Do not assume every tuple can be a set element or dictionary key; its contents must also be hashable.

---

## 5. Sets

A set is a **mutable collection of unique, hashable values**. It has no positional indexing and is ideal for membership tests, duplicate removal, and mathematical set operations.

### 5.1 Creating sets

```python
empty = set()                 # {} would create an empty dictionary
numbers = {1, 2, 3}
unique = set([1, 2, 2, 3])   # {1, 2, 3}
letters = set("hello")       # unique characters; display order may vary
```

Do not rely on a set's printed or iteration order. If output order matters, sort it explicitly:

```python
print(sorted(numbers))
```

### 5.2 Every set method

| Method | Purpose | Changes the set? |
|---|---|---:|
| `add(x)` | Add one element | Yes |
| `update(*others)` | Add elements from one or more iterables | Yes |
| `remove(x)` | Remove an element; error if absent | Yes |
| `discard(x)` | Remove an element if present | Yes |
| `pop()` | Remove and return an arbitrary element | Yes |
| `clear()` | Remove all elements | Yes |
| `copy()` | Return a shallow copy | No |
| `union(*others)` | Return all elements from either side | No |
| `intersection(*others)` | Return common elements | No |
| `difference(*others)` | Return elements absent from the others | No |
| `symmetric_difference(other)` | Return elements in exactly one side | No |
| `intersection_update(*others)` | Keep only common elements | Yes |
| `difference_update(*others)` | Remove elements found in others | Yes |
| `symmetric_difference_update(other)` | Keep elements in exactly one side | Yes |
| `isdisjoint(other)` | Test whether there is no overlap | No |
| `issubset(other)` | Test whether every element occurs in other | No |
| `issuperset(other)` | Test whether all other's elements occur here | No |

#### `add(x)`

```python
permissions = {"read", "write"}
permissions.add("execute")
permissions.add("read")  # duplicate has no effect
```

The new element must be hashable. A tuple of hashable values is valid; a list, set, or dictionary is not.

#### `update(*others)`

Adds all elements from one or more iterables.

```python
skills = {"Python"}
skills.update(["SQL", "Linux"], {"Git", "Python"})
```

`add(["SQL", "Linux"])` would fail because a list is unhashable; `update(...)` reads its individual elements.

#### `remove(x)` and `discard(x)`

```python
active = {"user1", "user2"}

active.remove("user1")     # raises KeyError if absent
active.discard("unknown")  # does nothing if absent
```

Use `remove()` when absence indicates a bug. Use `discard()` when absence is acceptable.

#### `pop()`

Removes and returns an **arbitrary** element.

```python
pending = {"scan-1", "scan-2"}
job = pending.pop()
```

It raises `KeyError` on an empty set. Never use `pop()` when a specific element or predictable order is required.

#### `clear()`

```python
cache_keys = {"a", "b", "c"}
cache_keys.clear()
```

#### `copy()`

```python
original = {1, 2, 3}
duplicate = original.copy()
```

#### `union(*others)` or `|`

Returns values that appear in at least one collection.

```python
a = {1, 2, 3}
b = {3, 4, 5}

print(a.union(b))  # {1, 2, 3, 4, 5}
print(a | b)       # same result
```

#### `intersection(*others)` or `&`

Returns values common to every collection.

```python
print(a.intersection(b))  # {3}
print(a & b)              # {3}
```

#### `difference(*others)` or `-`

Returns values in the left set but not the others. Direction matters.

```python
print(a.difference(b))  # {1, 2}
print(a - b)            # {1, 2}
print(b - a)            # {4, 5}
```

#### `symmetric_difference(other)` or `^`

Returns values in exactly one of the sets, excluding the overlap.

```python
print(a.symmetric_difference(b))  # {1, 2, 4, 5}
print(a ^ b)                       # {1, 2, 4, 5}
```

#### Update versions of mathematical operations

These change the original set:

```python
x = {1, 2, 3, 4}
x.intersection_update({3, 4, 5})
print(x)  # {3, 4}

x = {1, 2, 3, 4}
x.difference_update({3, 4, 5})
print(x)  # {1, 2}

x = {1, 2, 3}
x.symmetric_difference_update({3, 4})
print(x)  # {1, 2, 4}
```

`update()` is the in-place union operation. The compound operators `|=`, `&=`, `-=`, and `^=` provide equivalent set-style updates.

#### `isdisjoint(other)`

Returns `True` when the collections share no elements.

```python
print({1, 2}.isdisjoint({3, 4}))  # True
```

#### `issubset(other)` and subset operators

```python
required = {"read", "write"}
granted = {"read", "write", "admin"}

print(required.issubset(granted))  # True
print(required <= granted)         # subset
print(required < granted)          # proper subset: subset but not equal
```

#### `issuperset(other)` and superset operators

```python
print(granted.issuperset(required))  # True
print(granted >= required)           # superset
print(granted > required)            # proper superset
```

### 5.3 Method form versus operator form

Set methods accept general iterables, while operators normally require set-like operands.

```python
letters = {"a", "b"}
print(letters.intersection("banana"))  # {'a', 'b'}

# letters & "banana"  # TypeError
```

Methods are often clearer with several inputs; operators are concise when all operands are sets.

### 5.4 `frozenset`: the immutable set

`frozenset` supports the non-mutating set operations but cannot be changed. Because its elements and the object itself are hashable, a suitable `frozenset` can be a dictionary key or an element of another set.

```python
roles = frozenset({"reader", "editor"})
permission_map = {roles: "standard staff"}
```

### 5.5 Practical set patterns

Remove duplicates without preserving order:

```python
unique_ids = set([101, 102, 101, 103])
```

Remove duplicates while preserving the first-seen order:

```python
values = [3, 1, 3, 2, 1]
unique_in_order = list(dict.fromkeys(values))
```

Find common skills:

```python
applicant = {"Python", "SQL", "Git"}
required = {"Python", "Linux", "Git"}
common = applicant & required
missing = required - applicant
```

### 5.6 Set mastery tips

- Use a set when you frequently ask, “Have I seen this value before?”
- Never depend on set order.
- Use `discard()` for optional removal and `remove()` for strict removal.
- Remember that set elements must be hashable.
- Convert to `sorted(...)` when deterministic display or testing is required.

---

## 6. Dictionaries

A dictionary is a **mutable mapping of unique, hashable keys to values**. Values may be duplicated and may be of any type. Dictionaries preserve insertion order in modern Python.

### 6.1 Creating dictionaries

```python
empty = {}
student = {"name": "Ankita", "score": 92}
from_pairs = dict([("name", "Ankita"), ("score", 92)])
from_keywords = dict(name="Ankita", score=92)
```

Keys must be unique. Repeating a key replaces its earlier value:

```python
data = {"status": "pending", "status": "complete"}
print(data)  # {'status': 'complete'}
```

### 6.2 Reading, adding, updating, and deleting

```python
user = {"name": "Ankita", "active": True}

print(user["name"])           # strict access; KeyError if missing
print(user.get("email"))      # safe access; None if missing

user["email"] = "a@example.com"  # add
user["active"] = False            # update
del user["email"]                 # delete; KeyError if missing
```

Membership checks dictionary **keys**, not values:

```python
print("name" in user)              # True
print("Ankita" in user)            # False
print("Ankita" in user.values())   # True
```

### 6.3 Every dictionary method

| Method | Purpose | Changes dictionary? |
|---|---|---:|
| `clear()` | Remove all key-value pairs | Yes |
| `copy()` | Return a shallow copy | No |
| `dict.fromkeys(iterable, value=None)` | Build keys with one shared value | Creates new dictionary |
| `get(key, default=None)` | Read safely with a fallback | No |
| `items()` | Return a dynamic key-value view | No |
| `keys()` | Return a dynamic key view | No |
| `pop(key[, default])` | Remove a key and return its value | Yes |
| `popitem()` | Remove and return the last inserted pair | Yes |
| `setdefault(key, default=None)` | Read existing value or insert default | Maybe |
| `update([other], **kwargs)` | Merge pairs into the dictionary | Yes |
| `values()` | Return a dynamic value view | No |

#### `clear()`

```python
settings = {"theme": "dark", "sound": True}
settings.clear()
print(settings)  # {}
```

#### `copy()`

```python
original = {"name": "Ankita", "score": 92}
duplicate = original.copy()
```

This is a shallow copy; nested mutable values remain shared.

#### `dict.fromkeys(iterable, value=None)`

Creates a new dictionary whose keys come from an iterable.

```python
fields = ["name", "email", "phone"]
form = dict.fromkeys(fields, "unknown")
```

Be careful with a mutable shared default:

```python
bad = dict.fromkeys(["a", "b"], [])
bad["a"].append(1)
print(bad)  # {'a': [1], 'b': [1]}

good = {key: [] for key in ["a", "b"]}
good["a"].append(1)
print(good)  # {'a': [1], 'b': []}
```

#### `get(key, default=None)`

Returns the value if the key exists; otherwise returns the default without inserting it.

```python
profile = {"name": "Ankita"}
print(profile.get("name"))                 # Ankita
print(profile.get("city"))                 # None
print(profile.get("city", "Kathmandu"))   # Kathmandu
print(profile)                              # unchanged
```

#### `keys()`

Returns a dynamic view of keys.

```python
profile = {"name": "Ankita", "city": "Kathmandu"}
keys = profile.keys()
profile["active"] = True
print(list(keys))  # includes 'active'
```

Key views support useful set-like operations:

```python
old = {"name": "A", "email": "a@example.com"}
new = {"name": "A", "phone": "9800000000"}
print(old.keys() & new.keys())  # {'name'}
```

#### `values()`

Returns a dynamic view of values.

```python
scores = {"Asha": 80, "Bikash": 90}
print(sum(scores.values()))  # 170
```

#### `items()`

Returns a dynamic view of `(key, value)` pairs.

```python
for name, score in scores.items():
    print(f"{name}: {score}")
```

Dictionary views are iterable and reversible, but they are not lists. Convert with `list(...)` only when a real list is required.

#### `pop(key[, default])`

Removes a key and returns its value.

```python
account = {"user": "ankita", "temporary_code": 1234}
code = account.pop("temporary_code")
missing = account.pop("not_there", None)
```

Without a default, a missing key raises `KeyError`.

#### `popitem()`

Removes and returns the most recently inserted key-value pair as a tuple.

```python
data = {"a": 1, "b": 2, "c": 3}
pair = data.popitem()
print(pair)  # ('c', 3)
```

It raises `KeyError` when the dictionary is empty.

#### `setdefault(key, default=None)`

Returns the existing value. If the key is missing, it inserts and returns the default.

```python
groups = {}
groups.setdefault("admin", []).append("Ankita")
groups.setdefault("admin", []).append("Maya")

print(groups)  # {'admin': ['Ankita', 'Maya']}
```

For more extensive grouping, `collections.defaultdict` is often cleaner.

`get()` does not insert; `setdefault()` may insert:

```python
data = {}
data.get("x", 0)         # returns 0; data stays {}
data.setdefault("x", 0)  # returns 0; data becomes {'x': 0}
```

#### `update([other], **kwargs)`

Adds or overwrites key-value pairs.

```python
settings = {"theme": "light", "volume": 50}
settings.update({"theme": "dark", "language": "en"})
settings.update(volume=75)
```

Inputs may be another mapping, an iterable of key-value pairs, and/or keyword arguments.

### 6.4 Dictionary merge operators

Python 3.9+ supports `|` and `|=`:

```python
defaults = {"theme": "light", "language": "en"}
choices = {"theme": "dark"}

merged = defaults | choices  # new dictionary; right side wins
defaults |= choices          # updates defaults in place
```

### 6.5 Iterating correctly

```python
student = {"name": "Ankita", "score": 92}

for key in student:                  # keys by default
    print(key)

for value in student.values():
    print(value)

for key, value in student.items():
    print(key, value)

for key in reversed(student):        # reverse insertion order
    print(key)
```

Do not change the dictionary's size while iterating over it. Iterate over a snapshot when deletion is needed:

```python
scores = {"A": 90, "B": 45, "C": 75}

for name, score in list(scores.items()):
    if score < 50:
        del scores[name]
```

### 6.6 Counting and grouping patterns

Manual frequency table:

```python
words = ["red", "blue", "red", "green", "red"]
counts = {}

for word in words:
    counts[word] = counts.get(word, 0) + 1
```

Professional alternative:

```python
from collections import Counter

counts = Counter(words)
```

Grouping:

```python
from collections import defaultdict

students = [("AI", "Asha"), ("Cybersecurity", "Maya"), ("AI", "Nima")]
groups = defaultdict(list)

for course, name in students:
    groups[course].append(name)
```

### 6.7 Dictionary mastery tips

- Use `d[key]` when a missing key is an error; use `get()` when it is expected.
- Iterate with `.items()` when both keys and values are needed.
- Remember that `in` checks keys.
- Do not use mutable objects as keys.
- Do not modify dictionary size during direct iteration.
- Be deliberate about collisions during `update()` or `|`; later values win.
- Prefer a dataclass or class when a record has fixed fields and behavior.

---

## 7. Operations Shared by Collections

### 7.1 Common built-in functions

| Function | Meaning | Example |
|---|---|---|
| `len(x)` | Number of items | `len([10, 20]) == 2` |
| `min(x)` | Smallest item | `min({4, 2, 8}) == 2` |
| `max(x)` | Largest item | `max((4, 2, 8)) == 8` |
| `sum(x)` | Sum numeric items | `sum([1, 2, 3]) == 6` |
| `sorted(x)` | New sorted list | `sorted({3, 1, 2})` |
| `reversed(x)` | Reverse iterator for reversible objects | `list(reversed([1, 2]))` |
| `any(x)` | Is at least one item truthy? | `any([False, True])` |
| `all(x)` | Are all items truthy? | `all([True, True])` |
| `enumerate(x)` | Produce index-item pairs | `enumerate(names, start=1)` |
| `zip(a, b)` | Pair related iterables | `zip(names, scores)` |

On a dictionary, `len()`, iteration, `min()`, `max()`, `sorted()`, and membership operate on keys unless a view such as `.values()` is supplied.

### 7.2 Membership

```python
print(3 in [1, 2, 3])
print("a" in ("a", "b"))
print("admin" in {"admin", "user"})
print("name" in {"name": "Ankita"})
```

Membership in a list or tuple usually scans from the start. Set and dictionary-key membership is usually much faster for large collections.

### 7.3 Concatenation and repetition

Lists and tuples support `+` and `*`:

```python
print([1, 2] + [3, 4])    # [1, 2, 3, 4]
print((1, 2) * 3)         # (1, 2, 1, 2, 1, 2)
```

Beware of repeating nested mutable values:

```python
bad_grid = [[0] * 3] * 3
bad_grid[0][0] = 9
print(bad_grid)  # every row changes at position 0

good_grid = [[0] * 3 for _ in range(3)]
```

### 7.4 Truthiness

Empty collections are false; non-empty collections are true.

```python
items = []

if not items:
    print("The collection is empty")
```

This is clearer than `if len(items) == 0:`.

### 7.5 Converting between collection types

```python
numbers = [3, 1, 3, 2]

as_tuple = tuple(numbers)
as_set = set(numbers)
back_to_list = list(as_set)

pairs = [("a", 1), ("b", 2)]
as_dictionary = dict(pairs)
```

Conversion may change properties: converting a list to a set removes duplicates and positional order.

---

## 8. Comprehensions

Comprehensions create collections from iterables in a concise, readable form.

### 8.1 List comprehension

```python
squares = [number**2 for number in range(1, 6)]
even_squares = [number**2 for number in range(1, 11) if number % 2 == 0]
```

General form:

```python
[expression for item in iterable if condition]
```

### 8.2 Set comprehension

```python
unique_lengths = {len(word) for word in ["cat", "python", "dog", "code"]}
```

### 8.3 Dictionary comprehension

```python
square_map = {number: number**2 for number in range(1, 6)}
passed = {name: score for name, score in scores.items() if score >= 50}
```

### 8.4 There is no tuple comprehension

Parentheses create a generator expression, not a tuple:

```python
generator = (number**2 for number in range(5))
squares_tuple = tuple(number**2 for number in range(5))
```

### 8.5 Nested comprehensions

Flatten a matrix:

```python
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [value for row in matrix for value in row]
```

Transpose a rectangular matrix:

```python
matrix = [[1, 2, 3], [4, 5, 6]]
transposed = [list(column) for column in zip(*matrix)]
```

### 8.6 Readability rule

Use a comprehension for a simple transformation or filter. Use a normal loop when there are multiple conditions, side effects, exception handling, or complicated logic.

---

## 9. Mutability, Identity, and Copying

### 9.1 Mutable and immutable collections

- Lists, sets, and dictionaries are mutable.
- Tuples are immutable, although they may contain mutable objects.

### 9.2 Assignment does not copy

```python
original = [1, 2]
alias = original
alias.append(3)

print(original)          # [1, 2, 3]
print(alias is original) # True
```

Both names refer to the same object.

### 9.3 Shallow copy

```python
original = [[1, 2], [3, 4]]
shallow = original.copy()

shallow.append([5, 6])   # outer list is independent
shallow[0].append(99)    # inner list is shared
print(original)          # [[1, 2, 99], [3, 4]]
```

Shallow-copy options include:

```python
list_copy = original.copy()
list_copy_2 = original[:]
set_copy = {1, 2}.copy()
dict_copy = {"a": 1}.copy()
```

### 9.4 Deep copy

```python
from copy import deepcopy

original = [[1, 2], [3, 4]]
independent = deepcopy(original)
independent[0].append(99)

print(original)  # [[1, 2], [3, 4]]
```

Use deep copying deliberately: it may be expensive and may not be appropriate for objects representing external resources.

### 9.5 Equality versus identity

```python
a = [1, 2]
b = [1, 2]

print(a == b)  # True: same values
print(a is b)  # False: different objects
```

Use `==` for value comparison. Use `is` mainly for singleton checks such as `value is None`.

### 9.6 Hashability

Hashable objects have a stable hash value and may be used as set elements or dictionary keys.

Usually hashable:

- integers, floats, strings, bytes;
- immutable enums;
- tuples containing only hashable values; and
- frozensets containing only hashable values.

Usually unhashable:

- lists;
- sets; and
- dictionaries.

---

## 10. Nested Collections

Real programs combine collection types.

### 10.1 List of dictionaries

```python
students = [
    {"name": "Asha", "scores": [80, 85, 90]},
    {"name": "Nima", "scores": [75, 88, 92]},
]

for student in students:
    average = sum(student["scores"]) / len(student["scores"])
    print(student["name"], average)
```

### 10.2 Dictionary of sets

```python
permissions = {
    "admin": {"read", "write", "delete"},
    "user": {"read"},
}

if "delete" in permissions["admin"]:
    print("Allowed")
```

### 10.3 Dictionary with tuple keys

```python
temperature = {
    (2026, 8, 8): 28.5,
    (2026, 8, 9): 29.1,
}
```

### 10.4 Safe nested access

For uncertain external data, access step by step:

```python
response = {"user": {"profile": {"city": "Kathmandu"}}}
city = response.get("user", {}).get("profile", {}).get("city", "Unknown")
```

For fixed application data, validation tools such as dataclasses, TypedDict, Pydantic, or schema validation can provide clearer guarantees.

---

## 11. Time-Complexity Guide

The following table describes typical **average-case CPython behavior**, not a promise for every Python implementation or input.

| Operation | List | Tuple | Set | Dictionary |
|---|---:|---:|---:|---:|
| `len(x)` | O(1) | O(1) | O(1) | O(1) |
| Access by index | O(1) | O(1) | N/A | N/A |
| Access by key | N/A | N/A | N/A | O(1) average |
| Membership test | O(n) | O(n) | O(1) average | O(1) average for keys |
| Append at end | O(1) amortized | N/A | N/A | N/A |
| Insert/delete at beginning | O(n) | N/A | N/A | N/A |
| Add/remove by value | O(n) search | N/A | O(1) average | O(1) average by key |
| Copy | O(n) | O(1) for `tuple(t)` when already tuple | O(n) | O(n) |
| Iteration | O(n) | O(n) | O(n) | O(n) |
| Sort | O(n log n) | Use `sorted()` | Use `sorted()` | Use `sorted()` on a view |

### Performance lessons

- Choose a set or dictionary for frequent membership checks.
- Choose a list or tuple for positional access.
- Avoid removing from the front of a large list; use `deque`.
- A theoretically fast structure is not automatically the best choice—clarity, ordering, memory, and actual data size also matter.
- Measure important code with realistic data rather than guessing.

---

## 12. How to Choose the Correct Collection

| Requirement | Best starting choice | Reason |
|---|---|---|
| Ordered values that will change | List | Mutable sequence |
| Fixed ordered record | Tuple | Immutable sequence and unpacking |
| Unique values | Set | Enforces uniqueness |
| Fast “seen before?” check | Set | Fast average membership |
| Key-to-value lookup | Dictionary | Direct lookup by key |
| Preserve first-seen order while deduplicating | `list(dict.fromkeys(values))` | Keys preserve insertion order |
| FIFO queue | `collections.deque` | Fast operations at both ends |
| Count frequencies | `collections.Counter` | Designed for counting |
| Group many values per key | `collections.defaultdict(list)` | Convenient default containers |
| Fixed record with named fields | Dataclass or `NamedTuple` | More descriptive than indexes |

### Quick decision tree

1. Need key-value relationships? Use a **dictionary**.
2. Otherwise, need unique items or set mathematics? Use a **set**.
3. Otherwise, must the sequence remain fixed? Use a **tuple**.
4. Otherwise, use a **list**.

---

## 13. Common Mistakes and Their Fixes

### Mistake 1: Creating an empty set with `{}`

```python
wrong = {}       # dictionary
correct = set()  # set
```

### Mistake 2: Forgetting the comma in a one-item tuple

```python
wrong = (5)      # int
correct = (5,)   # tuple
```

### Mistake 3: Assigning an in-place method result

```python
numbers = [3, 1, 2]
numbers = numbers.sort()  # wrong: numbers becomes None

numbers = [3, 1, 2]
numbers.sort()            # correct
```

### Mistake 4: Confusing `append()` and `extend()`

```python
items.append([3, 4])  # adds one nested list
items.extend([3, 4])  # adds two individual values
```

### Mistake 5: Accessing a missing dictionary key directly

```python
city = profile.get("city", "Unknown")
```

Use `profile["city"]` instead when missing data should raise an error.

### Mistake 6: Expecting `in` to search dictionary values

```python
"name" in profile.values()  # search values explicitly
```

### Mistake 7: Using an unhashable key or set element

```python
# { [1, 2]: "value" }  # invalid list key
valid = {(1, 2): "value"}
```

### Mistake 8: Changing collection size while iterating

```python
for key in list(data):
    if should_delete(key):
        del data[key]
```

For lists, a comprehension is often better:

```python
numbers = [number for number in numbers if number >= 0]
```

### Mistake 9: Assuming assignment makes a copy

```python
duplicate = original.copy()
```

Use `deepcopy()` when nested objects must also be independent.

### Mistake 10: Using mutable defaults with `fromkeys()`

```python
correct = {key: [] for key in keys}
```

### Mistake 11: Relying on set order

```python
for value in sorted(my_set):
    print(value)
```

### Mistake 12: Using a list for a large queue

```python
from collections import deque

queue = deque()
queue.append("job")
queue.popleft()
```

### Mistake 13: Shadowing built-in names

```python
# Avoid: list = [1, 2], dict = {}, set = {1}
numbers = [1, 2]
user_by_id = {}
```

### Mistake 14: Depending on a mutating method inside an expression

Mutating methods generally return `None` by design. Separate mutation from later use:

```python
records.append(new_record)
process(records)
```

---

## 14. Clean-Code and Safety Tips

### Use descriptive plural names

```python
students = []
scores_by_name = {}
unique_permissions = set()
coordinates = (27.7172, 85.3240)
```

### Use type hints

```python
names: list[str] = []
point: tuple[float, float] = (27.7172, 85.3240)
permissions: set[str] = {"read"}
scores: dict[str, int] = {"Ankita": 92}
```

Variable-length tuple hint:

```python
measurements: tuple[float, ...] = (1.2, 3.4, 5.6)
```

### Validate untrusted data

Data from users, files, APIs, and databases may have missing keys, wrong types, or unexpected nesting. Validate before depending on its structure.

```python
if not isinstance(payload, dict):
    raise TypeError("payload must be a dictionary")

required = {"username", "email"}
missing = required - payload.keys()
if missing:
    raise ValueError(f"Missing fields: {sorted(missing)}")
```

### Avoid exposing secrets

Do not print complete dictionaries containing passwords, tokens, API keys, or personal information.

```python
safe_log = {key: value for key, value in account.items() if key not in {"password", "token"}}
```

### Prefer explicit transformations

Do not hide complicated state changes inside a dense expression. Clear intermediate names make collection code easier to test and debug.

### Use `collections` when the problem is specialized

```python
from collections import Counter, defaultdict, deque
```

- `Counter`: frequency counting;
- `defaultdict`: automatic default values;
- `deque`: efficient queues and operations at both ends;
- `ChainMap`: search across multiple mappings; and
- `namedtuple`: lightweight immutable named records.

---

## 15. Practice Exercises

Try each task before reading or searching for a solution.

### Beginner

1. Create a list of five subjects, add one, remove one, and print the sorted result.
2. Create a one-item tuple correctly and prove its type with `type()`.
3. Convert `[1, 2, 2, 3, 1, 4]` to a set and count the unique values.
4. Create a student dictionary with name, course, and score; update the score.
5. Loop over a dictionary and print each key with its value.
6. Find the second occurrence of a value in a list using `index()` with `start`.

### Intermediate

1. Remove duplicate words while preserving their original order.
2. Count word frequencies without using `Counter`, then solve it again with `Counter`.
3. Find common, missing, and extra permissions using set operations.
4. Sort a list of student dictionaries by score descending, then name ascending.
5. Group names by course using `setdefault()`, then repeat with `defaultdict(list)`.
6. Flatten a nested list with a comprehension.
7. Build a dictionary mapping numbers `1` through `20` to their squares, keeping only even numbers.

### Advanced

1. Compare two configuration dictionaries and report added, removed, and changed keys.
2. Build an inverted index mapping each word to the set of document IDs containing it.
3. Implement a small LIFO stack with a list and a FIFO queue with `deque`.
4. Write a function that safely walks a nested dictionary using a sequence of keys.
5. Explain with code why shallow copying fails for nested lists, then repair it.
6. Given user-role mappings, calculate each user's effective permissions using set union.
7. Benchmark membership tests for a large list and set using `timeit`.

### Challenge: collection method lab

Create a script that demonstrates every method from the four method tables. For methods that may raise errors, demonstrate both the successful case and safe error handling with `try`/`except`.

---

## 16. Mini-Projects

### 16.1 Student result manager

Use:

- a dictionary keyed by student ID;
- a list of scores for each student;
- a tuple for fixed course information; and
- a set to track registered subjects.

Features: add a student, update scores, calculate averages, list top performers, and find shared subjects.

### 16.2 Cybersecurity log analyser

Use:

- a set of blocked IP addresses;
- a dictionary counting attempts per IP;
- a list of chronological events; and
- tuples for fixed `(timestamp, ip_address, event)` records.

Features: identify repeated failed logins, block an address after a threshold, and report unique attackers.

### 16.3 Inventory tracker

Use a dictionary keyed by product ID. Each value can hold name, price, quantity, and a set of tags. Add functions for restocking, sales, low-stock reports, and category filtering.

### 16.4 Contact book

Use a dictionary keyed by a unique contact ID. Store phone numbers in a set to prevent duplicates and addresses in structured dictionaries.

### 16.5 Text analyser

Read text, normalize words, count frequencies, report unique words, find the most common terms, and group words by length.

---

## 17. Mastery Roadmap

### Stage 1: Foundations

- Memorize syntax for empty and populated collections.
- Practice indexing, slicing, membership, and iteration.
- Understand ordered versus unordered and mutable versus immutable.

### Stage 2: Methods

- Recreate every example in the four method tables.
- Predict the output before running each example.
- Learn which methods mutate and which return new objects.

### Stage 3: Transformations

- Master list, set, and dictionary comprehensions.
- Practice sorting with `key=`.
- Convert safely between collection types.
- Use unpacking, `enumerate()`, and `zip()` naturally.

### Stage 4: Correctness

- Understand aliases, shallow copies, and deep copies.
- Learn hashability and valid dictionary keys.
- Handle missing values and method-specific exceptions.
- Validate nested external data.

### Stage 5: Performance and design

- Learn common complexity costs.
- Use sets and dictionaries for fast membership.
- Use `deque`, `Counter`, and `defaultdict` for specialized work.
- Select structures based on semantics first, then measure performance.

### A strong study routine

1. Read one section.
2. Type every example yourself.
3. Change the inputs and predict the result.
4. Trigger the documented error deliberately.
5. Solve one exercise without notes.
6. Explain the concept aloud in simple language.
7. Apply it in a mini-project.

---

## 18. Final Cheat Sheet

### List

```python
items = []
items.append(x)
items.extend(iterable)
items.insert(index, x)
items.remove(x)
value = items.pop(index)  # index optional
items.clear()
position = items.index(x, start, stop)  # start/stop optional
amount = items.count(x)
items.sort(key=func, reverse=False)
items.reverse()
copy_of_items = items.copy()
```

### Tuple

```python
items = (a, b, c)
single = (a,)
amount = items.count(x)
position = items.index(x, start, stop)  # start/stop optional
a, b, c = items
```

### Set

```python
items = set()
items.add(x)
items.update(iterables)
items.remove(x)
items.discard(x)
value = items.pop()
items.clear()
copy_of_items = items.copy()

result = a.union(b)                 # a | b
result = a.intersection(b)          # a & b
result = a.difference(b)            # a - b
result = a.symmetric_difference(b)  # a ^ b

a.update(b)                         # a |= b
a.intersection_update(b)            # a &= b
a.difference_update(b)              # a -= b
a.symmetric_difference_update(b)    # a ^= b

a.isdisjoint(b)
a.issubset(b)                       # a <= b
a.issuperset(b)                     # a >= b
```

### Dictionary

```python
data = {}
data[key] = value
value = data[key]
value = data.get(key, default)
del data[key]

data.clear()
copy_of_data = data.copy()
new_data = dict.fromkeys(keys, value)
data.keys()
data.values()
data.items()
value = data.pop(key, default)
key, value = data.popitem()
value = data.setdefault(key, default)
data.update(other)

merged = left | right
left |= right
```

### Core memory rules

- **List:** ordered, mutable, duplicates allowed.
- **Tuple:** ordered, immutable, duplicates allowed.
- **Set:** unique hashable items, no positional indexing.
- **Dictionary:** insertion-ordered mapping with unique hashable keys.
- Assignment creates another reference, not a copy.
- In-place mutating methods usually return `None`.
- Set elements and dictionary keys must be hashable.

---

## 19. Official References

- [Python Tutorial: Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python Standard Types](https://docs.python.org/3/library/stdtypes.html)
- [Python `collections` Module](https://docs.python.org/3/library/collections.html)
- [Python Sorting HOW TO](https://docs.python.org/3/howto/sorting.html)
- [Python Time Complexity Wiki](https://wiki.python.org/moin/TimeComplexity)
- [PEP 584: Dictionary Union Operators](https://peps.python.org/pep-0584/)

---

## Closing Note

Knowing method names is only the first step. Mastery means understanding what each collection promises, how operations affect the original object, what errors can occur, and why one structure fits a problem better than another. Practice with small experiments, then reinforce the ideas through real projects.

If this guide helps you, keep extending it with your own examples, mistakes, solutions, and mini-project notes.

