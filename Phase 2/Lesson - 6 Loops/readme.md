# 🔄 Python Loops & Iteration Mastery: From Basic to Pro

Welcome to the definitive guide to **Loops and Iteration in Python**. This document bridges the gap between fundamental loop structures (`for`, `while`) and advanced iteration patterns (custom iterators, `itertools`, asynchronous loops, and memory-efficient generator workflows).

---

## 📋 Table of Contents
1. [Loop Fundamentals](#1-loop-fundamentals)
2. [Loop Control Statements](#2-loop-control-statements)
3. [Iterating Over Data Structures](#3-iterating-over-data-structures)
4. [Built-in Iteration Utilities](#4-built-in-iteration-utilities)
5. [Comprehensions & Generator Expressions](#5-comprehensions--generator-expressions)
6. [Under the Hood: Iterators & Protocols](#6-under-the-hood-iterators--protocols)
7. [Pro-Level Iteration with `itertools`](#7-pro-level-iteration-with-itertools)
8. [Asynchronous Loops (`async for`)](#8-asynchronous-loops-async-for)
9. [Performance & Anti-Patterns](#9-performance--anti-patterns)
10. [Quick Reference Cheat Sheet](#10-quick-reference-cheat-sheet)

---

## 1. Loop Fundamentals

Python provides two main looping constructs: `for` loops (for definite iteration) and `while` loops (for indefinite iteration).

### The `for` Loop and `range()`
In Python, `for` loops iterate over the items of any sequence or iterable object (like a list, string, or range).

```python
# Iterating over a sequence
for char in "Python":
    print(char)

# Using range(start, stop, step)
for i in range(1, 10, 2):  # 1, 3, 5, 7, 9
    print(i)
```

### The `while` Loop
Executes code repeatedly as long as the given condition evaluates to `True`.

```python
count = 5
while count > 0:
    print(f"Countdown: {count}")
    count -= 1
```

> **⚠️ Infinite Loops:** Be careful to update variables involved in `while` loop conditions, otherwise you get infinite execution:
> ```python
> # Emergency break in CLI: Ctrl + C
> while True:
>     # Pro-pattern: break on condition
>     user_input = input("Enter 'exit' to quit: ")
>     if user_input.lower() == "exit":
>         break
> ```

---

## 2. Loop Control Statements

### `break`, `continue`, and `pass`
* **`break`**: Immediately terminates the innermost loop.
* **`continue`**: Skips the remaining code in the current iteration and jumps to the next.
* **`pass`**: A syntactical placeholder that does nothing.

```python
for num in range(1, 10):
    if num % 2 == 0:
        continue  # Skip even numbers
    if num == 7:
        break     # Stop loop when num is 7
    print(num)    # Prints 1, 3, 5
```

### The Unique `for...else` & `while...else` Construct
Python supports an `else` block attached to loops! The `else` block executes **only if the loop completes normally without encountering a `break` statement**.

```python
# Searching for a prime number
numbers = [10, 14, 22, 25, 33]

for num in numbers:
    if num % 7 == 0 and num % 2 != 0:
        print(f"Found match: {num}")
        break
else:
    # Executed ONLY if no break occurred
    print("No odd multiple of 7 found in list.")
```

---

## 3. Iterating Over Data Structures

### Dictionaries
```python
user = {"name": "Alice", "role": "Admin", "active": True}

# Keys only (default)
for key in user:
    print(key)

# Values only
for val in user.values():
    print(val)

# Key-Value pairs (Unpacking)
for key, value in user.items():
    print(f"{key}: {value}")
```

### Nested Loops
When nesting loops, keep time complexity in mind (e.g., nested loops often lead to $O(N^2)$ or $O(N \times M)$ complexity).

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for row in matrix:
    for val in row:
        print(val, end=" ")
    print()
```

---

## 4. Built-in Iteration Utilities

Instead of manual index management (`i = 0; i += 1`), Python provides clean functional iteration utilities.

### `enumerate()` - Index & Value Pair
```python
fruits = ["apple", "banana", "cherry"]

# Bad practice: range(len(fruits))
# Pythonic practice:
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")
```

### `zip()` - Parallel Iteration
Combines multiple iterables pairwise. Stops when the shortest iterable is exhausted.

```python
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
teams = ["Red", "Blue"]

for name, score, team in zip(names, scores, teams):
    print(f"{name} ({team}): {score}")
# Stops after "Bob" because 'teams' has only 2 items
```

### `reversed()` and `sorted()`
```python
nums = [3, 1, 4, 1, 5, 9]

for n in sorted(nums):  # Yields elements in ascending order without modifying original
    print(n)

for n in reversed(nums): # Iterates backwards efficiently
    print(n)
```

---

## 5. Comprehensions & Generator Expressions

Comprehensions provide a concise syntax for constructing new sequences from existing iterables.

### List, Set, and Dict Comprehensions
```python
# List Comprehension with Filter
squares_of_evens = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]

# If-Else Transformation in List Comprehension
labels = ["Even" if x % 2 == 0 else "Odd" for x in range(5)]
# ['Even', 'Odd', 'Even', 'Odd', 'Even']

# Set Comprehension (Automatic Deduplication)
unique_lengths = {len(word) for word in ["apple", "banana", "fig", "apple"]}
# {3, 5, 6}

# Dict Comprehension
square_map = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### Generator Expressions (Memory Efficient)
Generator expressions use parentheses `()` and compute values lazily on-demand rather than building entire lists in memory.

```python
import sys

# Huge list in memory
big_list = [x for x in range(1_000_000)]
print(f"List memory: {sys.getsizeof(big_list)} bytes") # ~8MB

# Generator expression
big_gen = (x for x in range(1_000_000))
print(f"Gen memory: {sys.getsizeof(big_gen)} bytes")   # ~200 bytes!
```

---

## 6. Under the Hood: Iterators & Protocols

Every Python `for` loop operates on the **Iteration Protocol** using `iter()` and `next()`.

```python
numbers = [10, 20]

# What `for num in numbers:` actually does behind the scenes:
iterator = iter(numbers)  # Calls numbers.__iter__()

try:
    print(next(iterator)) # Calls iterator.__next__() -> 10
    print(next(iterator)) -> 20
    print(next(iterator)) # Raises StopIteration!
except StopIteration:
    pass
```

### Building a Custom Iterable Class
To make a class iterable, implement `__iter__()` and `__next__()`:

```python
class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val

for num in CountDown(3):
    print(num)  # 3, 2, 1
```

---

## 7. Pro-Level Iteration with `itertools`

The `itertools` standard library module provides high-performance, memory-efficient tools for complex loop constructs.

```python
import itertools

# 1. Infinite Iterators
# count(start, step)
for i in itertools.count(10, 2):
    if i > 16: break
    print(i)  # 10, 12, 14, 16

# cycle(iterable)
colors = itertools.cycle(["Red", "Green", "Blue"])

# 2. Combining Iterables
# chain() - Flattens multiple iterables into one continuous stream
combined = list(itertools.chain([1, 2], ["a", "b"])) # [1, 2, 'a', 'b']

# zip_longest() - Zips filled with fillvalue until longest iterable ends
zipped = list(itertools.zip_longest([1, 2], ["a", "b", "c"], fillvalue="-"))
# [(1, 'a'), (2, 'b'), ('-', 'c')]

# 3. Combinatorics (Permutations, Combinations, Cartesian Product)
product = list(itertools.product([1, 2], ["A", "B"]))
# [(1, 'A'), (1, 'B'), (2, 'A'), (2, 'B')]

perms = list(itertools.permutations(["A", "B", "C"], 2))
# [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

combs = list(itertools.combinations(["A", "B", "C"], 2))
# [('A', 'B'), ('A', 'C'), ('B', 'C')]

# 4. Grouping Data with groupby()
data = [("fruit", "apple"), ("fruit", "banana"), ("veg", "carrot")]
for category, group in itertools.groupby(data, key=lambda item: item[0]):
    items = [item[1] for item in group]
    print(f"{category}: {items}")
```

---

## 8. Asynchronous Loops (`async for`)

In asynchronous code (`asyncio`), `async for` allows iterating over asynchronous streams of data (e.g., websockets, paginated API requests, database cursors) without blocking the thread.

```python
import asyncio

class AsyncDataStream:
    """Simulates an async iterator fetching data chunks."""
    def __init__(self, limit):
        self.limit = limit
        self.count = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.count >= self.limit:
            raise StopAsyncIteration
        await asyncio.sleep(0.5)  # Simulate non-blocking I/O operation
        self.count += 1
        return f"Data Chunk {self.count}"

async def main():
    async for chunk in AsyncDataStream(3):
        print(f"Received: {chunk}")

asyncio.run(main())
```

---

## 9. Performance & Anti-Patterns

### ❌ Anti-Pattern 1: Modifying a Collection While Iterating
Modifying a list while looping over it causes skipped indices or unpredictable bugs.

```python
# BAD
nums = [1, 2, 3, 4, 5]
for n in nums:
    if n % 2 == 0:
        nums.remove(n)  # ⚠️ Mutating sequence during iteration!

# GOOD: Use comprehension to build a new list
nums = [n for n in nums if n % 2 != 0]
```

### ❌ Anti-Pattern 2: Manual Index Access Instead of Direct Iteration
```python
items = ["a", "b", "c"]

# BAD (C-style loop)
for i in range(len(items)):
    print(i, items[i])

# GOOD (Pythonic)
for i, item in enumerate(items):
    print(i, item)
```

### 🚀 Optimization Tip: Vectorization over Python Loops
For numeric or data analysis tasks, standard Python `for` loops are slow. Use **NumPy** or **Pandas** vectorization for orders of magnitude higher speed.

```python
import numpy as np

# Python loop approach (Slow)
arr = np.arange(1_000_000)
# result = [x * 2 for x in arr]

# Vectorized approach (100x+ Faster)
result = arr * 2
```

---

## 10. Quick Reference Cheat Sheet

| Task | Syntax Example | Key Benefit |
| :--- | :--- | :--- |
| **Indexed Loop** | `for i, item in enumerate(lst):` | Clean access to index and value |
| **Multi-Sequence** | `for x, y in zip(a, b):` | Parallel element processing |
| **Loop Fallback** | `for ... break else: ...` | Triggers if loop finishes without `break` |
| **Lazy Evaluation** | `(x**2 for x in data)` | Memory efficiency ($O(1)$ RAM) |
| **Combine Chains** | `itertools.chain(a, b)` | Stream multiple iterables effortlessly |
| **Combinatorics** | `itertools.product(a, b)` | Cartesian product without nested loops |
| **Async Stream** | `async for item in stream:` | Non-blocking asynchronous processing |

Happy Python Coding! 🚀