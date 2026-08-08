# 🐍 Comprehensive Guide to Functions in Python: From Basics to Advanced

Welcome to the ultimate reference guide for **Python Functions**. This document covers everything from fundamental function syntax to advanced paradigms like decorators, generators, asynchronous functions, and type hints.

---

## 📋 Table of Contents
1. [Introduction to Functions](#1-introduction-to-functions)
2. [Parameters and Arguments](#2-parameters-and-arguments)
3. [Variable Scope and Namespaces (LEGB)](#3-variable-scope-and-namespaces-legb)
4. [First-Class and Higher-Order Functions](#4-first-class-and-higher-order-functions)
5. [Lambda (Anonymous) Functions](#5-lambda-anonymous-functions)
6. [Decorators and Wrappers](#6-decorators-and-wrappers)
7. [Generators and `yield`](#7-generators-and-yield)
8. [Recursion and Optimization](#8-recursion-and-optimization)
9. [Type Hinting and Annotations](#9-type-hinting-and-annotations)
10. [Asynchronous Functions (`async` / `await`)](#10-asynchronous-functions-async--await)
11. [Best Practices and Design Patterns](#11-best-practices-and-design-patterns)

---

## 1. Introduction to Functions

A **function** in Python is a reusable block of code that performs a specific task. Functions allow you to modularize code, reduce repetition (DRY - Don't Repeat Yourself), and enhance readability.

### Basic Syntax
Functions are defined using the `def` keyword followed by the function name, parentheses `()`, and a colon `:`:

```python
def greet():
    """Docstring: Prints a friendly greeting message."""
    print("Hello, welcome to Python programming!")

# Executing (calling) the function
greet()
```

### Return Values
Functions can send data back to the caller using the `return` statement. If no `return` statement is specified, Python implicitly returns `None`.

```python
def add(a, b):
    return a + b

result = add(5, 10)  # result = 15

# Multiple Return Values (Returned as a tuple)
def min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = min_max([10, 20, 5, 80, 1])  # Tuple unpacking
```

---

## 2. Parameters and Arguments

Python provides flexible options for passing data into functions.

### Positional and Keyword Arguments
* **Positional Arguments:** Matched based on their position/order.
* **Keyword Arguments:** Matched explicitly by name.

```python
def describe_person(name, age, city):
    print(f"{name} is {age} years old and lives in {city}.")

# Positional
describe_person("Alice", 30, "New York")

# Keyword (Order does not matter)
describe_person(city="London", name="Bob", age=25)
```

### Default Parameters
Default parameters provide fallback values if arguments are omitted. Default values must follow non-default parameters.

```python
def power(base, exponent=2):
    return base ** exponent

print(power(4))     # 16 (uses default exponent=2)
print(power(4, 3))  # 64
```

> **⚠️ Warning:** Never use mutable objects (like lists or dictionaries) as default parameter values!
> 
> ```python
> # BAD
> def append_to(element, target=[]):
>     target.append(element)
>     return target
>
> # GOOD
> def append_to(element, target=None):
>     if target is None:
>         target = []
>     target.append(element)
>     return target
> ```

### Arbitrary Arguments (`*args` and `**kwargs`)
* `*args`: Collects extra positional arguments into a **tuple**.
* `**kwargs`: Collects extra keyword arguments into a **dictionary**.

```python
def flexible_function(*args, **kwargs):
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)

flexible_function(1, 2, 3, name="Eve", role="Developer")
# Output:
# Positional arguments: (1, 2, 3)
# Keyword arguments: {'name': 'Eve', 'role': 'Developer'}
```

### Special Parameters: Positional-Only (`/`) and Keyword-Only (`*`)
Python 3.8+ allows enforcement of parameter passing mechanisms:

```python
def specialized(pos_only, /, standard, *, kwd_only):
    print(pos_only, standard, kwd_only)

# pos_only MUST be positional
# standard can be positional or keyword
# kwd_only MUST be specified as a keyword
specialized(10, 20, kwd_only=30)
specialized(10, standard=20, kwd_only=30)
```

---

## 3. Variable Scope and Namespaces (LEGB)

Variable resolution in Python follows the **LEGB Rule**:
1. **L - Local:** Names assigned inside a function body.
2. **E - Enclosing:** Names in outer/enclosing functions (nested scope).
3. **G - Global:** Names assigned at the top-level of a module.
4. **B - Built-in:** Pre-defined Python names (e.g., `len`, `range`, `print`).

```python
x = "Global"

def outer():
    x = "Enclosing"
    def inner():
        x = "Local"
        print("Inner x:", x)
    inner()
    print("Outer x:", x)

outer()
print("Global x:", x)
```

### Modifying Outer Scopes: `global` and `nonlocal`
* `global`: Modifies variables at the module level.
* `nonlocal`: Modifies variables in the nearest enclosing (non-global) scope.

```python
count = 0

def increment_global():
    global count
    count += 1

def make_counter():
    value = 0
    def counter():
        nonlocal value
        value += 1
        return value
    return counter

c = make_counter()
print(c())  # 1
print(c())  # 2
```

---

## 4. First-Class and Higher-Order Functions

In Python, functions are **first-class citizens**, meaning they can be:
* Assigned to variables
* Passed as arguments to other functions
* Returned from other functions

### Assigning Functions & Passing as Arguments
```python
def square(x):
    return x * x

def apply_operation(func, value):
    return func(value)

f = square
print(apply_operation(f, 5))  # Output: 25
```

### Functions Returning Functions (Closures)
A **closure** occurs when a nested function retains access to variables from its enclosing scope even after the outer function has finished executing.

```python
def make_multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

---

## 5. Lambda (Anonymous) Functions

Lambda functions are small, single-expression anonymous functions defined with the `lambda` keyword:

$$\text{Syntax: } \text{lambda } \text{parameters} : \text{expression}$$

```python
square_lambda = lambda x: x ** 2
print(square_lambda(4))  # 16

# Common usage with sorting
data = [("Alice", 88), ("Bob", 95), ("Charlie", 78)]
sorted_data = sorted(data, key=lambda student: student[1])
# Output: [('Charlie', 78), ('Alice', 88), ('Bob', 95)]
```

### Functional Built-ins: `map`, `filter`, and `reduce`
```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map: apply function to all elements
squared = list(map(lambda x: x ** 2, numbers))  # [1, 4, 9, 16, 25]

# filter: keep elements matching condition
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]

# reduce: aggregate elements cumulatively
product = reduce(lambda x, y: x * y, numbers)  # 120
```

---

## 6. Decorators and Wrappers

A **decorator** is a higher-order function that modifies or enhances the behavior of another function without changing its source code.

### Basic Decorator
```python
import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[{func.__name__}] executed in {end_time - start_time:.4f}s")
        return result
    return wrapper

@timer_decorator
def heavy_computation():
    time.sleep(0.1)
    return sum(range(1000000))

heavy_computation()
```

### Preserving Metadata with `@functools.wraps`
When wrapping functions, docstrings and function names can be lost. Use `@wraps` to preserve them:

```python
from functools import wraps

def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}...")
        return func(*args, **kwargs)
    return wrapper

@log_decorator
def greet(name):
    """Greets the user."""
    return f"Hello, {name}!"

print(greet.__name__)  # 'greet' (without @wraps, it would be 'wrapper')
```

### Decorators with Arguments
To pass arguments to the decorator itself, add another level of nesting:

```python
def repeat(num_times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(num_times=3)
def say_hello():
    print("Hello!")

say_hello()  # Prints 'Hello!' 3 times
```

---

## 7. Generators and `yield`

Generators are functions that return an iterator and yield items one at a time using the `yield` keyword, preserving execution state between calls. They are memory-efficient for large data streams.

```python
def fibonacci_generator(limit):
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

# Using the generator
for num in fibonacci_generator(5):
    print(num)  # 0, 1, 1, 2, 3
```

### Generator Expressions
Similar to list comprehensions, but memory lazy:

```python
# Generator expression (lazy evaluation)
gen = (x ** 2 for x in range(1000000))

print(next(gen))  # 0
print(next(gen))  # 1
```

### Delegating Generators: `yield from`
```python
def generator_a():
    yield "A1"
    yield "A2"

def generator_b():
    yield from generator_a()
    yield "B1"

print(list(generator_b()))  # ['A1', 'A2', 'B1']
```

---

## 8. Recursion and Optimization

A function is **recursive** if it calls itself. Recursive functions must always have a **base case** to prevent infinite recursion.

```python
def factorial(n):
    if n <= 1:  # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case

print(factorial(5))  # 120
```

### Optimization: Memoization with `lru_cache`
Recursive functions can recompute identical subproblems. Use `functools.lru_cache` to cache results:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(50))  # Computed instantly!
```

---

## 9. Type Hinting and Annotations

Type hints improve code documentation, static analysis (with tools like `mypy`), and IDE auto-completion.

```python
from typing import List, Dict, Optional, Union, Callable

# Simple annotations
def greet(name: str) -> str:
    return f"Hello, {name}"

# Advanced typing
def process_scores(
    scores: List[float], 
    threshold: Optional[float] = None
) -> Dict[str, float]:
    if threshold is not None:
        scores = [s for s in scores if s >= threshold]
    return {"average": sum(scores) / len(scores) if scores else 0.0}

# Callable annotation (function as argument)
def compute(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)
```

---

## 10. Asynchronous Functions (`async` / `await`)

Asynchronous functions (coroutines) enable non-blocking concurrency, making them ideal for I/O-bound operations (network requests, database queries, file reading).

```python
import asyncio

async def fetch_data(source_id: int) -> dict:
    print(f"Fetching data from source {source_id}...")
    await asyncio.sleep(1)  # Non-blocking delay
    print(f"Received data from source {source_id}")
    return {"id": source_id, "status": "success"}

async def main():
    # Run multiple async functions concurrently
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    print("All results:", results)

# Run the async event loop
asyncio.run(main())
```

---

## 11. Best Practices and Design Patterns

### 1. Single Responsibility Principle (SRP)
Each function should do **one thing** well. If a function is doing multiple tasks, break it down.

### 2. Pure Functions
A function is pure if:
* It always produces the same output for the same input.
* It produces **no side effects** (does not modify global state, file systems, or passed mutable arguments).

```python
# Pure Function
def add_pure(a, b):
    return a + b

# Impure Function (has side effect)
total = 0
def add_impure(a):
    global total
    total += a
    return total
```

### 3. Clear Docstrings (Google / NumPy Style)
```python
def calculate_tax(price: float, tax_rate: float) -> float:
    """Calculates total tax for a given price and rate.

    Args:
        price (float): The base price of the item.
        tax_rate (float): The tax rate as a decimal (e.g., 0.15 for 15%).

    Returns:
        float: The calculated tax amount.

    Raises:
        ValueError: If price or tax_rate is negative.
    """
    if price < 0 or tax_rate < 0:
        raise ValueError("Price and tax rate must be non-negative.")
    return price * tax_rate
```

---

## 🎯 Quick Reference Cheat Sheet

| Feature | Syntax Example | Key Use Case |
| :--- | :--- | :--- |
| **Basic Function** | `def f(x): return x` | Code reuse |
| **`*args`** | `def f(*args):` | Variable positional arguments |
| **`**kwargs`** | `def f(**kwargs):` | Variable keyword arguments |
| **Lambda** | `lambda x: x + 1` | Inline short functions |
| **Closure** | Function returning nested function | Preserving state without classes |
| **Decorator** | `@my_decorator` | Extending function behavior |
| **Generator** | `yield x` | Memory-efficient sequence generation |
| **Async Function** | `async def f(): await ...` | Non-blocking asynchronous I/O |
| **Type Hinting** | `def f(x: int) -> str:` | Code clarity & static checking |

Happy Python Coding! 🚀