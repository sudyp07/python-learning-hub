# 🔍 Python Scopes & LEGB Rule – The Complete Guide

```markdown
# Python Scopes & LEGB Rule: The Complete Guide 🔍
> *Master variable visibility, namespace resolution, and the LEGB hierarchy – packed in one box.*

---

## 📌 Table of Contents
1. [What is a Scope?](#what-is-a-scope)
2. [The LEGB Rule Explained](#the-legb-rule-explained)
3. [Local Scope](#local-scope)
4. [Enclosing Scope](#enclosing-scope)
5. [Global Scope](#global-scope)
6. [Built-in Scope](#built-in-scope)
7. [The `global` Keyword](#the-global-keyword)
8. [The `nonlocal` Keyword](#the-nonlocal-keyword)
9. [Namespace Deep Dive](#namespace-deep-dive)
10. [Scope of Different Objects](#scope-of-different-objects)
11. [Closures](#closures)
12. [Common Pitfalls & Best Practices](#common-pitfalls--best-practices)
13. [Cheat Sheet](#cheat-sheet)

---

## 1️⃣ What is a Scope?
A **scope** is the region of a program where a variable is directly accessible.

- **Namespace** = a container that maps names to objects.
- **Scope** = the set of namespaces where you can look up variables.

```python
x = 10  # Global scope

def my_func():
    y = 20  # Local scope
    print(x)  # Can access global x
    print(y)  # Can access local y

my_func()
print(x)  # ✅ Works (global)
print(y)  # ❌ NameError (local not accessible outside)
```

---

## 2️⃣ The LEGB Rule Explained
Python resolves names in this order:

```
L → E → G → B
│   │   │   │
│   │   │   └─ Built-in (Python's pre-defined names)
│   │   └───── Global (module-level variables)
│   └───────── Enclosing (outer functions in nested scope)
└───────────── Local (inside current function)
```

**The search stops at the first match!**

```python
# LEGB Example
print = "Hello"  # Shadows built-in print (bad practice!)

def outer():
    x = "enclosing"
    
    def inner():
        x = "local"
        print(x)  # L: finds "local"
    
    inner()

outer()
```

---

## 3️⃣ Local Scope
Variables defined inside a function belong to the **local scope**.

```python
def my_function():
    local_var = 10          # Local variable
    another = 20            # Local variable
    return local_var + another

# local_var is NOT accessible outside
# print(local_var)  # NameError
```

**Local scope characteristics:**
- Created when function is called
- Destroyed when function returns
- Accessible only inside the function
- Different functions have separate local scopes

```python
def func1():
    x = 100
    print(x)

def func2():
    x = 200  # Different local scope
    print(x)

func1()  # 100
func2()  # 200
```

---

## 4️⃣ Enclosing Scope
Variables in **outer (enclosing) functions** are accessible in inner (nested) functions.

```python
def outer():
    outer_var = "I'm from outer"
    
    def inner():
        print(outer_var)  # Accesses enclosing variable
    
    inner()

outer()  # "I'm from outer"
```

**Multiple nesting levels:**

```python
def outer():
    x = "outer"
    
    def middle():
        x = "middle"
        
        def inner():
            print(x)  # Finds "middle" (nearest enclosing)
        
        inner()
    
    middle()

outer()  # "middle"
```

---

## 5️⃣ Global Scope
Variables defined at the **module level** (outside any function) are global.

```python
# Global scope
global_var = "I'm global"
PI = 3.14159
CONFIG = {"debug": True}

def show_global():
    print(global_var)  # Can READ global variables
    print(PI)

show_global()  # Works ✅
print(global_var)  # Also works outside function
```

**Reading vs. Writing global variables:**

```python
count = 0

def increment():
    # count += 1  # ❌ UnboundLocalError
    print(count)   # ✅ Can read

def increment_correct():
    global count   # ✅ Must declare global to modify
    count += 1

increment_correct()
print(count)  # 1
```

---

## 6️⃣ Built-in Scope
Python's **built-in scope** contains pre-defined names like `print`, `len`, `range`, `list`, `dict`, etc.

```python
# Built-in functions and exceptions
len([1, 2, 3])          # Built-in
print("Hello")          # Built-in
TypeError("Error")      # Built-in

# See all built-ins
import builtins
print(dir(builtins))    # List all built-in names
```

**Shadowing built-ins (BAD PRACTICE):**

```python
# ❌ DON'T DO THIS
len = 5                 # Shadows built-in len()
print(len([1,2,3]))     # TypeError: 'int' object is not callable

# ✅ Instead, avoid using built-in names as variables
my_len = 5
```

---

## 7️⃣ The `global` Keyword
Use `global` to **modify** a global variable from inside a function.

```python
# Basic usage
x = 10

def modify_global():
    global x
    x = 20          # Changes global x

modify_global()
print(x)  # 20 (global changed)
```

**Multiple global variables:**

```python
a = 1
b = 2
c = 3

def update_all():
    global a, b, c
    a = 10
    b = 20
    c = 30

update_all()
print(a, b, c)  # 10 20 30
```

**When is `global` NOT needed?**

```python
# Reading global variables (no global needed)
config = {"debug": True}

def get_debug():
    return config["debug"]  # ✅ Reading is fine

# Modifying mutable objects (no global needed)
def set_debug():
    config["debug"] = False  # ✅ Mutating, not reassigning

# Reassigning variable (global needed)
def reset_config():
    global config
    config = {"debug": False}  # ❌ Need global for reassignment
```

---

## 8️⃣ The `nonlocal` Keyword
Use `nonlocal` to **modify** variables in the **enclosing (outer)** scope from inside a nested function.

```python
def outer():
    x = "outer"
    
    def inner():
        nonlocal x      # Declare x from enclosing scope
        x = "modified"
    
    inner()
    print(x)  # "modified" (changed in outer scope)

outer()
```

**Without `nonlocal` (read-only):**

```python
def outer():
    x = 10
    
    def inner():
        print(x)  # ✅ Can read without nonlocal
        # x = 20  # ❌ Would create local x (not modifying outer)
    
    inner()
```

**Multiple `nonlocal` variables:**

```python
def outer():
    a = 1
    b = 2
    
    def middle():
        a = 10  # Local to middle
        
        def inner():
            nonlocal a, b  # a from middle, b from outer
            a = 20
            b = 30
        
        inner()
        print(a)  # 20 (changed)
    
    middle()
    print(b)  # 30 (changed)

outer()
```

**`nonlocal` vs `global` comparison:**

```python
x = "global"      # Global variable

def outer():
    x = "enclosing"  # Enclosing variable
    
    def inner():
        # x = "local"  # Would create local variable
        
        # Which x do we want to modify?
        # global x   # Modifies global x
        # nonlocal x # Modifies enclosing x
```

---

## 9️⃣ Namespace Deep Dive
Each scope has its own **namespace** (a dictionary of name→object mappings).

```python
def demo():
    x = 10
    y = 20
    print(locals())  # {'x': 10, 'y': 20}

demo()

# View global namespace
print(globals())  # Huge dictionary with all global names

# Access namespaces
x = 100
print(globals()['x'])  # 100 (access via dictionary)
```

**Namespace hierarchy:**

```
┌──────────────────────┐
│   Built-in Scope     │  ← Most outer
│   (builtins)         │
├──────────────────────┤
│   Global Scope       │  ← Module level
│   (globals())        │
├──────────────────────┤
│   Enclosing Scope    │  ← Outer function
│   (nonlocal)         │
├──────────────────────┤
│   Local Scope        │  ← Current function
│   (locals())         │
└──────────────────────┘
```

---

## 🔟 Scope of Different Objects

### Functions
```python
def factory():
    x = 10
    
    def inner():
        return x  # Closure - remembers x
    
    return inner

func = factory()
print(func())  # 10 (x is remembered via closure)
```

### Classes
```python
class MyClass:
    class_var = "class scope"  # Class variable
    
    def method(self):
        local_var = "local"    # Local variable
        print(MyClass.class_var)  # Access class variable
        print(self.class_var)     # Access via instance
```

### Comprehensions (Python 3)
```python
# List comprehension scope (Python 3)
x = 10
squares = [x**2 for x in range(5)]
print(x)  # 10 (x is NOT leaked in Python 3)

# In Python 2, x would be 4

# Generator expressions have their own scope
gen = (x**2 for x in range(5))
print(x)  # 10 (still global x)

# Dict and set comprehensions follow same rule
```

### Lambda Functions
```python
x = 10
func = lambda: x  # Captures x from enclosing scope
print(func())  # 10

# Be careful with loops and lambdas
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])  # [2, 2, 2] (all capture same i)

# Use default args to bind value
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])  # [0, 1, 2] ✅
```

---

## 1️⃣1️⃣ Closures
A **closure** occurs when a nested function references a variable from its enclosing scope.

```python
def make_multiplier(n):
    def multiplier(x):
        return x * n  # n is captured from enclosing scope
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

**Inspecting closures:**

```python
def outer(x):
    def inner():
        return x
    return inner

closure = outer(42)
print(closure.__closure__)        # Cell object
print(closure.__closure__[0].cell_contents)  # 42
print(closure.__code__.co_freevars)  # ('x',)
```

**Use cases for closures:**
- Function factories
- Decorators
- Callbacks with state
- Data hiding / encapsulation

```python
# Decorator example (uses closure)
def timer(func):
    import time
    
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Time: {time.time() - start} seconds")
        return result
    
    return wrapper

@timer
def slow_function():
    time.sleep(1)

slow_function()  # Prints execution time
```

---

## 1️⃣2️⃣ Common Pitfalls & Best Practices

### ❌ Pitfalls

**1. UnboundLocalError – modifying global without `global`**
```python
count = 0

def increment():
    # count += 1  # ❌ UnboundLocalError
    print(count)  # ✅ Works for reading
```

**2. Using `global` unnecessarily**
```python
# ❌ Bad: global not needed
def get_constant():
    global PI
    return PI

# ✅ Good
PI = 3.14159
def get_constant():
    return PI
```

**3. Shadowing built-ins**
```python
# ❌ Don't do this
list = [1, 2, 3]
# list(range(5))  # ❌ TypeError

# ✅ Use meaningful names
my_list = [1, 2, 3]
```

**4. Variable leakage in loops (Python 2)**
```python
# Python 2 ONLY - not an issue in Python 3
for x in range(5):
    pass
print(x)  # 4 (leaked!) - Python 2 only
```

**5. Late binding in closures**
```python
# ❌ All functions use the same i
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])  # [2, 2, 2]

# ✅ Bind i at function creation
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])  # [0, 1, 2]
```

### ✅ Best Practices

1. **Minimize global variables** – use functions with parameters instead.
2. **Use constants in UPPER_CASE** – makes them recognizable as globals.
3. **Avoid `global` when possible** – prefer passing values as arguments.
4. **Use `nonlocal` sparingly** – it indicates complex nested logic.
5. **Keep functions small** – reduces scope complexity.
6. **Never shadow built-ins** – causes confusing errors.
7. **Use `__all__` to control exports**:
   ```python
   # module.py
   __all__ = ['public_function', 'PublicClass']
   
   def private_function(): ...
   ```

---

## 1️⃣3️⃣ Cheat Sheet

### Scope Keywords
| Keyword   | Usage                                 | Scope Affected     |
|-----------|---------------------------------------|--------------------|
| `global`  | Modify a variable in global scope    | Global             |
| `nonlocal`| Modify a variable in enclosing scope | Enclosing (outer)  |
| (none)    | Create/modify in current scope       | Local              |

### Variable Resolution
```python
# LEGB lookup order
x = "global"

def outer():
    x = "enclosing"
    
    def inner():
        x = "local"
        print(x)  # 1️⃣ Local: "local"
        print(x)  # 2️⃣ Enclosing: "enclosing"
        print(x)  # 3️⃣ Global: "global"
        print(x)  # 4️⃣ Built-in: built-in len()
    
    inner()

# To check current scope variables
locals()   # Local namespace
globals()  # Global namespace
```

### Scope Functions
```python
# Inspecting scope
dir()               # Names in current scope
globals()           # Global namespace dict
locals()            # Local namespace dict
vars()              # __dict__ of current scope
vars(obj)           # __dict__ of object

# Scope manipulation (use with caution!)
globals()['x'] = 100  # Create global variable dynamically
```

### Quick Reference Table

| Variable Location | Can Read | Can Modify | Keyword Needed |
|-------------------|----------|------------|----------------|
| Local             | ✅       | ✅         | -              |
| Enclosing         | ✅       | ✅         | `nonlocal`     |
| Enclosing (read)  | ✅       | ❌         | -              |
| Global            | ✅       | ✅         | `global`       |
| Global (read)     | ✅       | ❌         | -              |
| Built-in          | ✅       | ❌         | -              |
| Built-in (shadow) | ✅       | ✅         | (assign local) |

---

## 📚 Advanced Topics

### Dynamic Scope with `exec()`
```python
# Executing code in different scopes
scope = {}
exec("x = 42", scope)
print(scope['x'])  # 42

# But exec() is generally discouraged for production code
```

### Context Managers and Scope
```python
# Context managers don't create new scope
with open('file.txt') as f:
    content = f.read()
print(content)  # ✅ Still accessible (not scope-limited)
```

### Class Scope vs Instance Scope
```python
class MyClass:
    class_var = "shared"  # Class scope (shared across instances)
    
    def __init__(self, value):
        self.instance_var = value  # Instance scope (per instance)

# Class variables are shared
obj1 = MyClass(1)
obj2 = MyClass(2)
print(obj1.class_var)  # "shared"
print(obj2.class_var)  # "shared"
MyClass.class_var = "changed"
print(obj1.class_var)  # "changed"
```

---

## 💡 Summary

- **Scopes** determine where variables are accessible in your code.
- **LEGB** is the resolution order: **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in.
- Use **`global`** to modify global variables from inside functions.
- Use **`nonlocal`** to modify enclosing variables from nested functions.
- **Closures** capture variables from enclosing scopes for later use.
- Keep scopes **small and simple** for maintainable code.

> *"Understanding scope is understanding how Python thinks about your code."*

---

## 🔗 Further Learning

- [Python Docs – Execution Model](https://docs.python.org/3/reference/executionmodel.html)
- [Python Docs – `global` Statement](https://docs.python.org/3/reference/simple_stmts.html#global)
- [Python Docs – `nonlocal` Statement](https://docs.python.org/3/reference/simple_stmts.html#nonlocal)
- [PEP 3104 – Access to Names in Outer Scopes](https://www.python.org/dev/peps/pep-3104/)
- [Closures & Decorators – Real Python](https://realpython.com/primer-on-python-decorators/)

---

**Happy Coding! 🐍✨**
```
