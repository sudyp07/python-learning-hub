# ========== PYTHON FUNCTIONS (DEF) - COMPLETE GUIDE ==========

# ========== 1. BASIC FUNCTION ==========
def greet():
    print("Hello World!")


greet()  # Hello World!


# ========== 2. FUNCTION WITH PARAMETERS ==========
def greet(name):
    print(f"Hello {name}!")


greet("Alice")  # Hello Alice!


# ========== 3. FUNCTION WITH RETURN ==========
def add(a, b):
    return a + b


result = add(5, 3)  # 8


# ========== 4. DEFAULT PARAMETERS ==========
def greet(name="Guest"):
    print(f"Hello {name}!")


greet()  # Hello Guest!
greet("Bob")  # Hello Bob!


# ========== 5. MULTIPLE RETURN VALUES (tuple) ==========
def get_user():
    return "Alice", 25, "NYC"


name, age, city = get_user()  # Unpacking


# ========== 6. *args (Variable number of arguments) ==========
def sum_all(*args):
    return sum(args)


sum_all(1, 2, 3, 4)  # 10
sum_all(5, 10)  # 15


# ========== 7. **kwargs (Variable number of keyword arguments) ==========
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")


print_info(name="Alice", age=25, city="NYC")


# name: Alice, age: 25, city: NYC

# ========== 8. COMBINING *args AND **kwargs ==========
def mixed(required, *args, **kwargs):
    print(f"Required: {required}")
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")


mixed("Hello", 1, 2, 3, name="Alice", age=25)


# Required: Hello
# Args: (1, 2, 3)
# Kwargs: {'name': 'Alice', 'age': 25}

# ========== 9. KEYWORD-ONLY ARGUMENTS (*) ==========
def greet(name, *, age, city):
    print(f"{name}, {age}, {city}")


greet("Alice", age=25, city="NYC")  # Must use keywords


# ========== 10. POSITIONAL-ONLY ARGUMENTS (/) ==========
def divide(a, b, /):
    return a / b


divide(10, 2)  # 5.0
# divide(a=10, b=2)  # ERROR! Positional only

# ========== 11. LAMBDA FUNCTION (Anonymous) ==========
square = lambda x: x ** 2
square(5)  # 25
# Used with map, filter, sorted
list(map(lambda x: x * 2, [1, 2, 3]))  # [2,4,6]


# ========== 12. RECURSIVE FUNCTION ==========
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


factorial(5)  # 120


# ========== 13. NESTED FUNCTION ==========
def outer(x):
    def inner(y):
        return y * 2

    return inner(x) + 5


outer(10)  # 25


# ========== 14. CLOSURE ==========
def multiplier(factor):
    def multiply(x):
        return x * factor

    return multiply


times2 = multiplier(2)
times2(5)  # 10


# ========== 15. DOCSTRING (Documentation) ==========
def add(a, b):
    """
    Adds two numbers and returns the result.

    Parameters:
    a (int): First number
    b (int): Second number

    Returns:
    int: Sum of a and b
    """
    return a + b


help(add)  # Shows docstring
add.__doc__  # Access docstring


# ========== 16. TYPE HINTS (Type Annotations) ==========
def greet(name: str, age: int) -> str:
    return f"Name: {name}, Age: {age}"


greet("Alice", 25)  # Name: Alice, Age: 25


# ========== 17. DECORATORS ==========
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time: {end - start} seconds")
        return result

    return wrapper


@timer
def slow_function():
    time.sleep(1)


slow_function()  # Time: ~1.0 seconds


# ========== 18. GENERATOR FUNCTION (yield) ==========
def count_down(n):
    while n > 0:
        yield n
        n -= 1


for num in count_down(5):
    print(num)  # 5,4,3,2,1


# ========== 19. ARGUMENT UNPACKING ==========
def add(a, b, c):
    return a + b + c


nums = [1, 2, 3]
add(*nums)  # 6 (unpack list)
nums_dict = {'a': 1, 'b': 2, 'c': 3}
add(**nums_dict)  # 6 (unpack dict)

# ========== 20. GLOBAL & NONLOCAL ==========
x = 10  # Global


def outer():
    y = 20  # Enclosing

    def inner():
        nonlocal y  # Access enclosing scope
        global x  # Access global scope
        y += 1
        x += 1

    inner()
    print(y)  # 21

# ========== COMPLETE REFERENCE ==========
# def function_name(params):    → Define function
# return value                  → Return value
# *args                         → Variable positional args
# **kwargs                      → Variable keyword args
# param=default                 → Default parameter
# /                             → Positional-only args
# *                             → Keyword-only args
# lambda x: x*2                 → Anonymous function
# yield value                   → Generator function
# @decorator                    → Decorator
# type hints (int, str, etc.)  → Type annotations
# docstring (""" """)          → Documentation

# ========== BEST PRACTICES ==========
# ✅ Use descriptive names: def calculate_average():
# ✅ Keep functions small & focused
# ✅ Use type hints for clarity
# ✅ Add docstrings
# ✅ Use default parameters wisely
# ✅ Return early when possible
# ❌ Avoid modifying global variables
# ❌ Don't use mutable default args (def func(list=[]):)  # BAD!