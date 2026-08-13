# 📦 Python Iterables – The Complete Boxed Guide

```markdown
# Python Iterables: The Complete Guide 📦
> *Everything you need to know about iterables, iterators, and generators – packed in one box.*

---

## 📌 Table of Contents
1. [What is an Iterable?](#what-is-an-iterable)
2. [The Iteration Protocol](#the-iteration-protocol)
3. [Built‑in Iterables](#builtin-iterables)
4. [Iterators vs. Iterables](#iterators-vs-iterables)
5. [Creating Custom Iterables](#creating-custom-iterables)
6. [Generators – The Easy Way](#generators--the-easy-way)
7. [Generator Expressions](#generator-expressions)
8. [The `itertools` Module](#the-itertools-module)
9. [Common Pitfalls & Best Practices](#common-pitfalls--best-practices)
10. [Cheat Sheet](#cheat-sheet)

---

## 1️⃣ What is an Iterable?
An **iterable** is any Python object that can return its elements one at a time.  
→ Anything you can loop over with a `for` loop is an iterable.

```python
# Examples of iterables
my_list = [1, 2, 3]
my_string = "hello"
my_dict = {"a": 1, "b": 2}

for item in my_list:   # works
    print(item)
```

Under the hood, an iterable implements the `__iter__()` method, which returns an **iterator**.

---

## 2️⃣ The Iteration Protocol
Python’s iteration protocol is built on two methods:

- `__iter__()` – returns the iterator object itself (used by `iter()`).
- `__next__()` – returns the next item; raises `StopIteration` when exhausted (used by `next()`).

When you write `for x in my_iterable`, Python:

1. Calls `iter(my_iterable)` to get an iterator.
2. Repeatedly calls `next(iterator)` until `StopIteration` is raised.

```python
my_list = [10, 20, 30]
it = iter(my_list)          # get iterator
print(next(it))             # 10
print(next(it))             # 20
print(next(it))             # 30
# next(it) would raise StopIteration
```

---

## 3️⃣ Built‑in Iterables
Many core Python types are iterable:

| Type          | Example                            | Iterates over        |
|---------------|------------------------------------|----------------------|
| `list`        | `[1, 2, 3]`                        | elements             |
| `tuple`       | `(1, 2, 3)`                        | elements             |
| `str`         | `"hello"`                          | characters           |
| `dict`        | `{"a": 1, "b": 2}`                 | keys (by default)    |
| `set`         | `{1, 2, 3}`                        | elements             |
| `range`       | `range(5)`                         | numbers              |
| `file`        | `open("file.txt")`                 | lines                |
| `enumerate`   | `enumerate([1, 2])`                | (index, value) pairs |

```python
# Dictionary iteration
for key in {"a": 1, "b": 2}:
    print(key)          # a, b

for key, value in {"a": 1, "b": 2}.items():
    print(key, value)   # a 1, b 2
```

---

## 4️⃣ Iterators vs. Iterables
| **Iterable**                            | **Iterator**                              |
|-----------------------------------------|-------------------------------------------|
| Has `__iter__()`                        | Has `__iter__()` AND `__next__()`         |
| Can be iterated multiple times          | Can be iterated only once                 |
| Returns a fresh iterator each time      | Consumes itself as it goes                |
| Examples: `list`, `tuple`, `str`        | Examples: `range_iterator`, `zip_iterator`|

```python
my_list = [1, 2, 3]
iterator = iter(my_list)

# Iterable can be iterated multiple times
for x in my_list: print(x)   # works
for x in my_list: print(x)   # works again

# Iterator can be iterated only once
for x in iterator: print(x)  # works
for x in iterator: print(x)  # does nothing (already exhausted)
```

---

## 5️⃣ Creating Custom Iterables
Make your own iterable class by implementing `__iter__()` and `__next__()`:

```python
class CountDown:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self  # iterator returns itself
    
    def __next__(self):
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

# Usage
for num in CountDown(5):
    print(num)  # 5, 4, 3, 2, 1, 0
```

**Alternative** – create an iterable that returns a separate iterator:

```python
class Squares:
    def __init__(self, n):
        self.n = n
    
    def __iter__(self):
        return SquaresIterator(self.n)

class SquaresIterator:
    def __init__(self, n):
        self.n = n
        self.i = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        result = self.i ** 2
        self.i += 1
        return result

# Allows multiple independent iterations
sq = Squares(3)
for x in sq: print(x)  # 0, 1, 4
for x in sq: print(x)  # 0, 1, 4 (fresh iterator each time)
```

---

## 6️⃣ Generators – The Easy Way
**Generators** are functions that use `yield` instead of `return`. They automatically implement the iterator protocol!

```python
def count_down(start):
    while start >= 0:
        yield start
        start -= 1

# Usage
for num in count_down(5):
    print(num)  # 5, 4, 3, 2, 1, 0

# Generators are single-use iterators
gen = count_down(3)
print(next(gen))  # 3
print(next(gen))  # 2
print(next(gen))  # 1
print(next(gen))  # 0
print(next(gen))  # StopIteration
```

**Generator with `send()`** – bidirectional communication:

```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)              # prime the generator
print(acc.send(10))    # 10
print(acc.send(20))    # 30
print(acc.send(5))     # 35
```

---

## 7️⃣ Generator Expressions
A compact way to create generators, similar to list comprehensions but with parentheses:

```python
# List comprehension (creates a full list in memory)
squares_list = [x**2 for x in range(10)]

# Generator expression (creates a generator, lazy evaluation)
squares_gen = (x**2 for x in range(10))

# Memory efficient – great for large datasets
for sq in squares_gen:
    print(sq)

# Can be used directly in functions
sum(x**2 for x in range(10))          # 285
max(x for x in range(100) if x % 2)   # 99
```

---

## 8️⃣ The `itertools` Module
Python's `itertools` provides powerful tools for working with iterables:

```python
import itertools

# Infinite iterators
itertools.count(10, 2)      # 10, 12, 14, ...
itertools.cycle('ABC')      # A, B, C, A, B, C, ...
itertools.repeat('x', 3)    # x, x, x

# Combinatorics
list(itertools.permutations([1, 2, 3], 2))  # [(1,2), (1,3), (2,1), ...]
list(itertools.combinations([1, 2, 3], 2))  # [(1,2), (1,3), (2,3)]
list(itertools.product([1,2], ['a','b']))   # [(1,'a'), (1,'b'), ...]

# Chaining & grouping
list(itertools.chain([1,2], [3,4]))         # [1,2,3,4]
list(itertools.islice(range(10), 2, 8, 2))  # [2,4,6]

# Grouping (requires sorted data)
data = [('a', 1), ('a', 2), ('b', 3)]
for key, group in itertools.groupby(data, lambda x: x[0]):
    print(key, list(group))  # a [(a,1),(a,2)], b [(b,3)]
```

---

## 9️⃣ Common Pitfalls & Best Practices

### ❌ Pitfalls

**1. Exhausting an iterator**
```python
gen = (x for x in range(3))
print(list(gen))  # [0, 1, 2]
print(list(gen))  # []  ← already exhausted!
```

**2. Modifying a list while iterating**
```python
# Bad – raises RuntimeError
for x in my_list:
    if x % 2 == 0:
        my_list.remove(x)

# Good – iterate over a copy
for x in my_list[:]:
    if x % 2 == 0:
        my_list.remove(x)
```

**3. Using `range()` incorrectly**
```python
# range returns a range object, NOT a list
r = range(1000000)  # memory efficient
nums = list(range(1000000))  # memory heavy (use only when needed)
```

### ✅ Best Practices

1. **Use generators for large datasets** – saves memory.
2. **Prefer generator expressions over list comprehensions** when you only need to iterate once.
3. **Use `iter()` to check if something is iterable**:
   ```python
   def is_iterable(obj):
       try:
           iter(obj)
           return True
       except TypeError:
           return False
   ```
4. **Use `itertools` for complex iteration patterns** – don't reinvent the wheel!
5. **Be explicit about one‑time vs. reusable** – if you need to reuse, convert to a list/tuple.
6. **Lazy evaluation is your friend** – it delays computation until needed.

---

## 🎯 Cheat Sheet

| Concept                | Code                                      | Description                       |
|------------------------|-------------------------------------------|-----------------------------------|
| **Check iterable**     | `hasattr(obj, '__iter__')`                | Returns `True` if iterable        |
| **Get iterator**       | `it = iter(obj)`                          | Creates an iterator               |
| **Get next item**      | `next(it)`                                | Returns next item or raises       |
| **StopIteration**      | `try: next(it) except StopIteration: pass`| Handle exhaustion                 |
| **Generator function** | `def gen(): yield value`                  | Lazy producer                     |
| **Generator expr**     | `(x*2 for x in range(5))`                 | Compact generator                 |
| **List comprehension** | `[x*2 for x in range(5)]`                 | Eager (creates list)              |
| **`for` loop**         | `for item in iterable:`                   | Built‑in iteration                |
| **Unpacking**          | `a, b, c = iterable`                      | Unpacks first N items             |
| **`*` operator**       | `*iterable`                               | Unpacks into function args/list   |
| **`zip()`**            | `zip(list1, list2)`                       | Pair up iterables                 |
| **`enumerate()`**      | `enumerate(list)`                         | Add index to items                |
| **`sorted()`**         | `sorted(iterable, key=...)`               | Returns sorted list               |
| **`reversed()`**       | `reversed(iterable)`                      | Returns reversed iterator         |

---

## 📚 Quick Reference: Built-in Functions for Iterables

```python
# Convert to container
list(iterable)    # Convert to list
tuple(iterable)   # Convert to tuple
set(iterable)     # Convert to set

# Aggregate
sum(iterable)     # Sum all items
max(iterable)     # Maximum item
min(iterable)     # Minimum item
any(iterable)     # True if any item is truthy
all(iterable)     # True if all items are truthy

# Filter & map
filter(func, iterable)   # Keep items where func(item) is True
map(func, iterable)      # Apply func to every item

# Reduce (from functools)
from functools import reduce
reduce(lambda x, y: x + y, [1, 2, 3, 4])  # 10
```

---

## 🚀 Pro Tips

1. **Memory comparison**:
   ```python
   # List: stores everything
   sum([x for x in range(1000000)])  # Uses ~8MB
   
   # Generator: processes one at a time
   sum(x for x in range(1000000))    # Uses ~few bytes
   ```

2. **Chain multiple iterables**:
   ```python
   from itertools import chain
   for item in chain(range(3), 'abc', [1, 2, 3]):
       print(item)  # 0,1,2,a,b,c,1,2,3
   ```

3. **Make a reusable iterator** – convert to list when needed:
   ```python
   data = list(generator_function())  # now reusable
   ```

4. **Custom `__iter__` for infinite streams** – use `while True` with `yield`.

---

## 💡 Summary

- **Iterables** are objects you can loop over (implement `__iter__`).
- **Iterators** are objects that produce values (implement `__iter__` + `__next__`).
- **Generators** are the easiest way to create iterators (use `yield`).
- **Always prefer generators** for large or infinite sequences.
- **`itertools`** has everything you need for complex iteration.

> *"Iteration is the heartbeat of Python – master it, and you master the language."*

---

## 🔗 Further Learning

- [Python Docs – Iterators](https://docs.python.org/3/tutorial/classes.html#iterators)
- [Python Docs – Generators](https://docs.python.org/3/tutorial/classes.html#generators)
- [Python Docs – itertools](https://docs.python.org/3/library/itertools.html)
- [Fluent Python – Chapter 14: Iterables, Iterators, and Generators](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/)

---

**Happy Coding! 🐍✨**
```