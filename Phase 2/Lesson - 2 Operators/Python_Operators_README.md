# Python Operators: Complete Master Guide

> A practical beginner-to-advanced guide to Python arithmetic, assignment, comparison, logical, membership, identity, bitwise, conditional, matrix-multiplication, and walrus operators—with examples, common mistakes, exercises, and mastery tips.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Topic](https://img.shields.io/badge/Topic-Python%20Operators-2E8B57)](#)
[![Level](https://img.shields.io/badge/Level-Beginner%20to%20Advanced-orange)](#)

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Project Files](#2-project-files)
3. [Running the Examples](#3-running-the-examples)
4. [Operator Overview](#4-operator-overview)
5. [Arithmetic Operators](#5-arithmetic-operators)
6. [Comparison Operators](#6-comparison-operators)
7. [Logical Operators](#7-logical-operators)
8. [Assignment Operators](#8-assignment-operators)
9. [Walrus Operator](#9-walrus-operator)
10. [Membership Operators](#10-membership-operators)
11. [Identity Operators](#11-identity-operators)
12. [Bitwise Operators](#12-bitwise-operators)
13. [Conditional Expression](#13-conditional-expression)
14. [Operator Precedence](#14-operator-precedence)
15. [Operators with Collections and Strings](#15-operators-with-collections-and-strings)
16. [The `operator` Module](#16-the-operator-module)
17. [Operator Overloading](#17-operator-overloading)
18. [Common Mistakes and Fixes](#18-common-mistakes-and-fixes)
19. [Clean-Code, Performance, and Security Tips](#19-clean-code-performance-and-security-tips)
20. [Practice Exercises](#20-practice-exercises)
21. [Mini-Projects](#21-mini-projects)
22. [Mastery Roadmap](#22-mastery-roadmap)
23. [Complete Cheat Sheet](#23-complete-cheat-sheet)
24. [Official References](#24-official-references)

---

## 1. Introduction

Operators are symbols or keywords that tell Python to perform an operation on one or more values. The values used by an operator are called **operands**.

```python
total = 10 + 5
```

In this expression:

- `10` and `5` are operands;
- `+` is the addition operator; and
- `15` is the result.

Operators are essential because they allow programs to:

- calculate totals, averages, percentages, and powers;
- compare values and make decisions;
- combine conditions;
- assign and update variables;
- test membership and object identity;
- manipulate binary flags and permissions;
- process data efficiently inside expressions; and
- define meaningful behavior for custom classes.

### Learning outcomes

After studying this guide, you should be able to:

- identify every major category of Python operator;
- predict results using precedence and associativity;
- explain `=`, `==`, `is`, and `:=` correctly;
- use short-circuit evaluation safely;
- work with arithmetic, logical, membership, identity, and bitwise operations;
- choose between normal and augmented assignment;
- use the walrus operator only when it improves readability;
- avoid floating-point and mutable-object mistakes; and
- apply operators confidently in real programs.

---

## 2. Project Files

The original project contains these six demonstration files:

| File | Main topic |
|---|---|
| `Membership_operator.py` | `in` and `not in` |
| `arithmetic_operator.py` | Arithmetic operators such as `+`, `-`, `*`, `/`, and `%` |
| `assignment_operators.py` | Basic and augmented assignment |
| `bitwise_operators.py` | Binary operations such as `&`, `|`, `^`, `~`, `<<`, and `>>` |
| `comparision_operators.py` | Value comparison operators |
| `logical_operators.py` | `and`, `or`, and `not` |

### Recommended filename improvements

Python filenames normally use lowercase `snake_case`. For consistency and correct spelling, these names are recommended:

```text
python-operators/
├── README.md
├── arithmetic_operators.py
├── assignment_operators.py
├── bitwise_operators.py
├── comparison_operators.py
├── identity_operators.py
├── logical_operators.py
├── membership_operators.py
└── walrus_operator.py
```

> `comparision` should be spelled `comparison`. Rename the file only if your imports, submission instructions, or teacher's required filenames will not be affected.

---

## 3. Running the Examples

### Requirements

- Python 3.10 or later is recommended.
- The walrus operator requires Python 3.8 or later.
- The basic examples use only the Python standard library.

Check the installed version:

```bash
python --version
```

Run a file:

```bash
python arithmetic_operator.py
```

On systems where `python` points to an older version, use:

```bash
python3 arithmetic_operator.py
```

You can also test small expressions in the interactive shell:

```bash
python
```

```pycon
>>> 10 + 5
15
>>> 10 > 5
True
```

---

## 4. Operator Overview

| Category | Operators | Main purpose |
|---|---|---|
| Arithmetic | `+  -  *  /  //  %  **  @` | Mathematical and matrix operations |
| Unary arithmetic | `+x  -x` | Express positive or negative value |
| Comparison | `==  !=  >  <  >=  <=` | Compare values |
| Logical | `and  or  not` | Combine or reverse truth conditions |
| Basic assignment | `=` | Bind a name or target to a value |
| Augmented assignment | `+=  -=  *=  /=  //=  %=  **=  @=  &=  \|=  ^=  <<=  >>=` | Calculate and assign |
| Assignment expression | `:=` | Assign a name inside an expression |
| Membership | `in  not in` | Test whether a value is contained |
| Identity | `is  is not` | Test whether two references point to the same object |
| Bitwise | `&  \|  ^  ~  <<  >>` | Manipulate integer bits or compatible objects |
| Conditional expression | `x if condition else y` | Choose one of two values |

### Operator terminology

```python
result = left_operand + right_operand
```

- A **unary** operator uses one operand: `-number`, `not active`, `~mask`.
- A **binary** operator uses two operands: `a + b`, `x in values`.
- An **expression** produces a value.
- A **statement** performs an action and does not necessarily produce a reusable value.
- **Precedence** decides which operator is evaluated first.
- **Associativity** decides grouping when operators have equal precedence.

---

## 5. Arithmetic Operators

Arithmetic operators perform mathematical calculations. Several also work with strings, lists, tuples, sets, dictionaries, or custom objects.

### 5.1 Complete arithmetic table

| Operator | Name | Example | Result |
|---|---|---|---:|
| `+` | Addition | `10 + 3` | `13` |
| `-` | Subtraction | `10 - 3` | `7` |
| `*` | Multiplication | `10 * 3` | `30` |
| `/` | True division | `10 / 3` | `3.333...` |
| `//` | Floor division | `10 // 3` | `3` |
| `%` | Modulo/remainder | `10 % 3` | `1` |
| `**` | Exponentiation | `10 ** 3` | `1000` |
| `@` | Matrix multiplication | `matrix_a @ matrix_b` | Type-dependent |
| `+x` | Unary positive | `+10` | `10` |
| `-x` | Unary negative | `-10` | `-10` |

### 5.2 Addition: `+`

```python
first_number = 20
second_number = 5
total = first_number + second_number

print(total)  # 25
```

It also concatenates compatible sequences:

```python
full_name = "Ankita" + " " + "Adhikari"
numbers = [1, 2] + [3, 4]
coordinates = (10, 20) + (30, 40)
```

Python does not automatically combine incompatible types:

```python
age = 21
message = "Age: " + str(age)
```

### 5.3 Subtraction: `-`

```python
balance = 1_000
withdrawal = 250
remaining = balance - withdrawal

print(remaining)  # 750
```

With sets, `-` means set difference:

```python
required = {"Python", "SQL", "Git"}
known = {"Python", "Git"}
missing = required - known

print(missing)  # {'SQL'}
```

### 5.4 Multiplication: `*`

```python
price = 150
quantity = 4
total = price * quantity

print(total)  # 600
```

It repeats strings and sequences:

```python
separator = "-" * 20
zeros = [0] * 5
pattern = (1, 2) * 3
```

Be careful when repeating nested mutable objects:

```python
wrong_grid = [[0] * 3] * 3
wrong_grid[0][0] = 9
print(wrong_grid)  # all three rows change

correct_grid = [[0] * 3 for _ in range(3)]
```

### 5.5 True division: `/`

In Python 3, `/` produces a floating-point result even when the operands divide exactly.

```python
print(10 / 2)  # 5.0
print(7 / 2)   # 3.5
```

Division by zero raises `ZeroDivisionError`:

```python
divisor = 0

if divisor != 0:
    result = 10 / divisor
else:
    print("Cannot divide by zero")
```

### 5.6 Floor division: `//`

Floor division rounds the mathematical quotient **down toward negative infinity**, not simply toward zero.

```python
print(10 // 3)   # 3
print(-10 // 3)  # -4
print(10 // -3)  # -4
```

Practical use: calculate the number of complete groups.

```python
students = 23
group_size = 5
complete_groups = students // group_size
```

### 5.7 Modulo: `%`

Modulo returns the remainder associated with floor division.

```python
print(10 % 3)  # 1
```

Test whether a number is even:

```python
number = 24
is_even = number % 2 == 0
```

Wrap an index into a repeating range:

```python
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
day_index = 9 % len(days)
print(days[day_index])  # Wed
```

For integer operands, Python maintains this relationship when `b != 0`:

```python
a == (a // b) * b + (a % b)
```

### 5.8 Exponentiation: `**`

```python
square = 5 ** 2
cube = 5 ** 3
square_root = 25 ** 0.5
```

Exponentiation groups from right to left:

```python
print(2 ** 3 ** 2)    # 2 ** (3 ** 2) = 512
print((2 ** 3) ** 2)  # 64
```

Unary minus has a subtle interaction with exponentiation:

```python
print(-3 ** 2)    # -(3 ** 2) = -9
print((-3) ** 2)  # 9
```

### 5.9 Matrix multiplication: `@`

`@` asks compatible objects to perform matrix multiplication. Built-in lists do not implement it, but numerical libraries such as NumPy do.

```python
# Optional example: pip install numpy
import numpy as np

matrix_a = np.array([[1, 2], [3, 4]])
matrix_b = np.array([[5, 6], [7, 8]])
product = matrix_a @ matrix_b

print(product)
# [[19 22]
#  [43 50]]
```

Do not confuse matrix multiplication `@` inside an expression with `@decorator` syntax above a function or class.

### 5.10 Unary positive and negative

```python
temperature = 7
positive = +temperature
negative = -temperature
```

Unary `+` usually leaves a number unchanged. Unary `-` negates it. Custom numeric types may define specialized behavior.

### 5.11 Helpful arithmetic functions

```python
quotient, remainder = divmod(17, 5)
absolute_value = abs(-12)
rounded = round(3.14159, 2)
power = pow(2, 5)
modular_power = pow(2, 5, 3)
```

`divmod(a, b)` returns `(a // b, a % b)`. Three-argument `pow(base, exponent, modulus)` is useful for efficient modular arithmetic.

---

## 6. Comparison Operators

Comparison operators normally return `True` or `False`.

| Operator | Meaning | Example |
|---|---|---|
| `==` | Equal values | `5 == 5` → `True` |
| `!=` | Unequal values | `5 != 3` → `True` |
| `>` | Greater than | `5 > 3` → `True` |
| `<` | Less than | `5 < 3` → `False` |
| `>=` | Greater than or equal to | `5 >= 5` → `True` |
| `<=` | Less than or equal to | `5 <= 4` → `False` |

### 6.1 Basic comparisons

```python
age = 21

print(age == 21)  # True
print(age != 18)  # True
print(age > 18)   # True
print(age <= 25)  # True
```

### 6.2 `=` is not `==`

```python
score = 80       # assignment
passed = score == 80  # equality comparison
```

- `=` assigns a value.
- `==` compares values.

### 6.3 Chained comparisons

Python supports mathematical-style chains:

```python
score = 75
valid = 0 <= score <= 100
```

This is similar to:

```python
valid = 0 <= score and score <= 100
```

The middle expression is evaluated only once in a chained comparison.

Useful examples:

```python
age = 21
is_working_age = 18 <= age < 65

x, y, z = 10, 20, 15
result = x < y > z  # legal: x < y and y > z
```

### 6.4 String comparisons

Strings compare lexicographically using Unicode code points.

```python
print("apple" < "banana")  # True
print("Zebra" < "apple")   # True in code-point ordering
```

For case-insensitive user-facing comparison:

```python
first = "PYTHON"
second = "python"
same_text = first.casefold() == second.casefold()
```

Human-language sorting and comparison may require locale-aware or Unicode-normalized processing.

### 6.5 Sequence comparisons

Lists and tuples of the same type compare lexicographically:

```python
print([1, 2, 3] < [1, 3, 0])  # True
print((1, 2) == (1, 2))        # True
print([1, 2] == (1, 2))        # False: different collection types
```

Dictionary equality compares key-value contents, not insertion order:

```python
left = {"a": 1, "b": 2}
right = {"b": 2, "a": 1}
print(left == right)  # True
```

Ordering dictionaries with `<` or `>` is not supported.

### 6.6 Set comparisons mean subset and superset

```python
required = {"read", "write"}
granted = {"read", "write", "admin"}

print(required <= granted)  # subset: True
print(required < granted)   # proper subset: True
print(granted >= required)  # superset: True
print(granted > required)   # proper superset: True
```

This is not numeric or lexicographic ordering.

### 6.7 Floating-point comparison

Binary floating-point values may not represent decimal fractions exactly:

```python
print(0.1 + 0.2 == 0.3)  # False
```

For approximate numeric comparison:

```python
from math import isclose

print(isclose(0.1 + 0.2, 0.3))  # True
```

For financial calculations requiring exact decimal behavior, consider `decimal.Decimal`.

---

## 7. Logical Operators

Logical operators combine or reverse truth conditions.

| Operator | General meaning | Result condition |
|---|---|---|
| `and` | Both conditions | Truthy only if both are truthy |
| `or` | At least one condition | Truthy if either is truthy |
| `not` | Reverse truth value | Boolean opposite |

### 7.1 Boolean examples

```python
age = 21
has_id = True

can_enter = age >= 18 and has_id
needs_help = age < 18 or not has_id
```

### 7.2 Truthiness

Python treats these common values as false:

- `False` and `None`;
- numeric zero such as `0`, `0.0`, and `0j`;
- empty strings and bytes;
- empty lists, tuples, sets, dictionaries, and ranges; and
- custom objects whose `__bool__()` returns `False` or whose `__len__()` returns `0`.

Most other values are true.

```python
items = []

if not items:
    print("The list is empty")
```

### 7.3 Short-circuit evaluation

Python stops evaluating when the result is already determined.

```python
denominator = 0

if denominator != 0 and 100 / denominator > 2:
    print("Valid result")
```

The division is not attempted when `denominator != 0` is false.

Safe attribute access pattern:

```python
user = None

if user is not None and user.is_active:
    print("Active user")
```

### 7.4 `and` and `or` return operands

They do not always return literal `True` or `False`.

```python
print("Python" and "SQL")  # SQL
print("" and "SQL")        # ''
print("Python" or "SQL")   # Python
print("" or "Guest")       # Guest
print(not "Python")        # False
```

Rules:

- `x and y` returns `x` when `x` is falsy; otherwise it returns `y`.
- `x or y` returns `x` when `x` is truthy; otherwise it returns `y`.
- `not x` always returns a Boolean.

Default-value pattern:

```python
display_name = entered_name or "Guest"
```

Be careful: this replaces every falsy value, including `0`, `False`, and empty collections—not only `None`.

### 7.5 `any()` and `all()`

```python
checks = [True, True, False]

print(any(checks))  # True
print(all(checks))  # False
```

Practical example:

```python
password = "Secure123!"

has_upper = any(character.isupper() for character in password)
has_digit = any(character.isdigit() for character in password)
is_long_enough = len(password) >= 8

is_strong = all([has_upper, has_digit, is_long_enough])
```

### 7.6 Logical precedence

The order is:

1. `not`
2. `and`
3. `or`

```python
result = True or False and False
# True or (False and False) -> True
```

Use parentheses whenever they make the intention easier to see.

---

## 8. Assignment Operators

In precise Python terminology, `=` is part of an assignment statement. It is commonly called the assignment operator in beginner materials. It binds a name or other valid target to an object.

### 8.1 Basic assignment: `=`

```python
name = "Ankita"
score = 92
active = True
```

The right-hand side is evaluated before assignment:

```python
total = 10 + 5 * 2  # 20 is calculated, then assigned
```

### 8.2 Every augmented assignment operator

| Operator | Similar basic form | Example purpose |
|---|---|---|
| `+=` | `x = x + y` | Add/concatenate and assign |
| `-=` | `x = x - y` | Subtract and assign |
| `*=` | `x = x * y` | Multiply/repeat and assign |
| `/=` | `x = x / y` | Divide and assign |
| `//=` | `x = x // y` | Floor-divide and assign |
| `%=` | `x = x % y` | Take remainder and assign |
| `**=` | `x = x ** y` | Raise to power and assign |
| `@=` | `x = x @ y` | Matrix-multiply and assign |
| `&=` | `x = x & y` | Bitwise/set intersection and assign |
| `\|=` | `x = x \| y` | Bitwise/set/dictionary union and assign |
| `^=` | `x = x ^ y` | Bitwise/set symmetric difference and assign |
| `<<=` | `x = x << y` | Left-shift and assign |
| `>>=` | `x = x >> y` | Right-shift and assign |

Examples:

```python
number = 10
number += 5   # 15
number *= 2   # 30
number //= 4  # 7
number **= 2  # 49
```

### 8.3 Augmented assignment is not always identical to long form

`x += y` evaluates the target only once and may mutate an object in place. `x = x + y` normally creates a new result and rebinds the target.

```python
original = [1, 2]
alias = original

original += [3]
print(alias)  # [1, 2, 3] because the list changed in place
```

Compare:

```python
original = [1, 2]
alias = original

original = original + [3]
print(alias)     # [1, 2]
print(original)  # [1, 2, 3]
```

Immutable objects such as integers, strings, and tuples cannot be changed in place, so augmented assignment binds the name to a new object.

### 8.4 Multiple assignment and unpacking

```python
x, y = 10, 20
first, second, third = [1, 2, 3]
```

Extended unpacking:

```python
first, *middle, last = [10, 20, 30, 40, 50]

print(first)   # 10
print(middle)  # [20, 30, 40]
print(last)    # 50
```

Swap values safely:

```python
x, y = y, x
```

### 8.5 Chained assignment and aliasing

```python
x = y = 0
```

This is normally safe for immutable values. With a mutable value, both names reference the same object:

```python
first = second = []
first.append("shared")
print(second)  # ['shared']
```

Create separate objects instead:

```python
first = []
second = []
```

---

## 9. Walrus Operator

The **walrus operator** `:=` is an assignment expression introduced in Python 3.8. It assigns a value to a simple name and also returns that value as part of a larger expression.

### 9.1 Basic example

Without the walrus operator:

```python
length = len("Cybersecurity")

if length > 10:
    print(f"Long word: {length} characters")
```

With the walrus operator:

```python
if (length := len("Cybersecurity")) > 10:
    print(f"Long word: {length} characters")
```

The value from `len(...)` is calculated once, assigned to `length`, and used in the comparison.

### 9.2 Reading input in a loop

```python
while (command := input("Command (quit to stop): ").strip().lower()) != "quit":
    print(f"Running: {command}")
```

### 9.3 Reading file chunks

```python
with open("example.bin", "rb") as file:
    while chunk := file.read(4096):
        process(chunk)
```

Parentheses are not required in this simple `while` condition, although some teams may include them for visibility.

### 9.4 Regular-expression matching

```python
import re

message = "Incident ID: 4821"

if match := re.search(r"\d+", message):
    incident_id = match.group()
    print(incident_id)
```

### 9.5 In a comprehension

```python
raw_values = ["10", "", "25", "0", "8"]
positive_values = [number for value in raw_values if value and (number := int(value)) > 0]
```

The assignment expression avoids converting the same string more than once.

### 9.6 `=` versus `==` versus `:=`

| Syntax | Meaning | Produces a reusable expression value? |
|---|---|---:|
| `x = value` | Assignment statement | No |
| `x == value` | Equality comparison | Yes, Boolean |
| `x := value` | Assignment expression | Yes, assigned value |

```python
x = 5
is_five = x == 5

if (current := x) == 5:
    print(current)
```

### 9.7 Parentheses rules

Parentheses are required in several contexts and often improve clarity even when optional.

```python
(value := 10)          # valid expression statement
result = (size := 5)   # parentheses required in assignment statement
assert (count := 3)    # parentheses required here
```

The target must be a simple identifier:

```python
# object.attribute := value  # invalid
# items[0] := value          # invalid
```

### 9.8 When to use the walrus operator

Use it when:

- one moderately expensive expression would otherwise be repeated;
- a loop needs both a fetched value and a stopping condition;
- a regex match is tested and then used; or
- a clear comprehension benefits from retaining an intermediate result.

Avoid it when:

- normal assignment is clearer;
- it hides side effects inside a complex condition;
- the expression becomes difficult to explain;
- several walrus assignments are nested together; or
- the saved line of code is not worth the extra mental effort.

Readability matters more than cleverness.

---

## 10. Membership Operators

Membership operators test whether an item appears in a container.

| Operator | Meaning |
|---|---|
| `in` | Is the item present? |
| `not in` | Is the item absent? |

### 10.1 Lists, tuples, and sets

```python
numbers = [10, 20, 30]
coordinates = (27.7, 85.3)
roles = {"admin", "editor", "viewer"}

print(20 in numbers)            # True
print(50 not in numbers)        # True
print(27.7 in coordinates)      # True
print("admin" in roles)         # True
```

### 10.2 Strings

For strings, membership tests substrings:

```python
message = "Learn Python operators"

print("Python" in message)      # True
print("python" in message)      # False: case-sensitive
print("Java" not in message)    # True
print("" in message)            # True: empty string is a substring
```

Case-insensitive test:

```python
contains_python = "python" in message.casefold()
```

### 10.3 Dictionaries

Membership checks dictionary **keys**, not values:

```python
student = {"name": "Ankita", "score": 92}

print("name" in student)             # True
print("Ankita" in student)           # False
print("Ankita" in student.values())  # True
```

### 10.4 Performance insight

Membership in lists and tuples normally scans values from the beginning, giving O(n) average search time. Sets and dictionary keys normally provide O(1) average membership tests.

```python
blocked_users = {"user12", "user45", "user78"}

if username in blocked_users:
    deny_access()
```

Choose a set when frequent membership testing is central to the problem and unique values are appropriate.

---

## 11. Identity Operators

Identity operators test whether two references point to the **same object**, not merely objects with equal values.

| Operator | Meaning |
|---|---|
| `is` | Same object |
| `is not` | Different objects |

### 11.1 Equality versus identity

```python
first = [1, 2, 3]
second = [1, 2, 3]
alias = first

print(first == second)  # True: equal contents
print(first is second)  # False: different list objects
print(first is alias)   # True: same object
```

### 11.2 Correct use with `None`

```python
result = None

if result is None:
    print("No result")

if result is not None:
    print(result)
```

Use `is None` and `is not None`, as recommended by Python style conventions.

### 11.3 Do not use `is` for normal value comparison

```python
name = "Ankita"

if name == "Ankita":
    print("Correct value comparison")
```

Python may reuse some small integers or strings internally, but that is an implementation detail. Code such as `value is 100` is incorrect for value comparison.

### 11.4 `id()`

```python
first = []
alias = first

print(id(first) == id(alias))  # True while both objects exist
```

In normal application code, direct identity checks are clearer than comparing numeric IDs.

---

## 12. Bitwise Operators

Bitwise operators work with the binary representation of integers. Some are also overloaded by sets, dictionaries, and custom types.

Suppose:

```text
a = 10 = 1010₂
b =  6 = 0110₂
```

| Operator | Name | Example | Binary result | Decimal result |
|---|---|---|---|---:|
| `&` | Bitwise AND | `10 & 6` | `0010` | `2` |
| `\|` | Bitwise OR | `10 \| 6` | `1110` | `14` |
| `^` | Bitwise XOR | `10 ^ 6` | `1100` | `12` |
| `~` | Bitwise NOT | `~10` | Two's-complement concept | `-11` |
| `<<` | Left shift | `10 << 1` | `10100` | `20` |
| `>>` | Right shift | `10 >> 1` | `0101` | `5` |

### 12.1 View binary values

```python
a = 10
b = 6

print(bin(a))  # 0b1010
print(bin(b))  # 0b110
print(f"{a:08b}")  # 00001010
```

### 12.2 Bitwise AND: `&`

A result bit is `1` only when both corresponding bits are `1`.

```python
print(10 & 6)  # 2
```

Common use: test whether a flag is enabled.

### 12.3 Bitwise OR: `|`

A result bit is `1` when at least one corresponding bit is `1`.

```python
print(10 | 6)  # 14
```

Common use: combine flags.

### 12.4 Bitwise XOR: `^`

A result bit is `1` when exactly one corresponding bit is `1`.

```python
print(10 ^ 6)  # 12
print(8 ^ 8)   # 0
```

XOR is useful in low-level transformations and flag toggling, but XOR by itself is not secure encryption.

### 12.5 Bitwise NOT: `~`

For Python integers:

```python
~x == -(x + 1)
```

```python
print(~10)  # -11
print(~0)   # -1
```

Python integers are not limited to a fixed number of bits, so NOT is best understood using this formula unless a fixed-width mask is applied.

Eight-bit inversion example:

```python
value = 10
inverted_8_bit = (~value) & 0xFF

print(inverted_8_bit)       # 245
print(f"{inverted_8_bit:08b}")  # 11110101
```

### 12.6 Left shift: `<<`

For non-negative integers, shifting left by `n` positions is equivalent to multiplying by `2 ** n`.

```python
print(5 << 1)  # 10
print(5 << 3)  # 40
```

### 12.7 Right shift: `>>`

For non-negative integers, shifting right by `n` positions is equivalent to floor division by `2 ** n`.

```python
print(40 >> 1)  # 20
print(40 >> 3)  # 5
```

A negative shift count raises `ValueError`.

### 12.8 Permission flags example

```python
READ = 1 << 0     # 001
WRITE = 1 << 1    # 010
EXECUTE = 1 << 2  # 100

permissions = READ | WRITE

can_read = bool(permissions & READ)
can_execute = bool(permissions & EXECUTE)

permissions |= EXECUTE   # add permission
permissions &= ~WRITE    # remove permission
permissions ^= READ      # toggle permission
```

For many business applications, a set of named permissions is clearer. Bitmasks are valuable when data must be compact or compatible with low-level protocols.

### 12.9 Bitwise operators on sets

```python
a = {1, 2, 3}
b = {3, 4, 5}

print(a & b)  # intersection: {3}
print(a | b)  # union: {1, 2, 3, 4, 5}
print(a ^ b)  # symmetric difference: {1, 2, 4, 5}
print(a - b)  # difference: {1, 2}
```

### 12.10 Logical versus bitwise operators

| Logical | Bitwise |
|---|---|
| `and`, `or`, `not` | `&`, `|`, `^`, `~` |
| Use truthiness | Operate on bits or overloaded objects |
| `and` and `or` short-circuit | Both operands are normally evaluated |
| May return operands | Integer bitwise operations return integers |

Use logical operators for conditions:

```python
if is_logged_in and has_permission:
    grant_access()
```

Use bitwise operators for integer masks, flags, or types that intentionally overload them.

---

## 13. Conditional Expression

Python's conditional expression is often called the **ternary operator**.

```python
value_if_true if condition else value_if_false
```

Example:

```python
score = 75
status = "Pass" if score >= 50 else "Fail"
```

It evaluates only the selected branch:

```python
denominator = 0
result = 100 / denominator if denominator != 0 else None
```

Use it for simple value selection. Prefer a normal `if`/`else` statement when logic, side effects, or nested conditions become difficult to read.

Avoid deeply nested expressions:

```python
# Hard to read
label = "High" if score >= 80 else "Medium" if score >= 50 else "Low"

# Clearer
if score >= 80:
    label = "High"
elif score >= 50:
    label = "Medium"
else:
    label = "Low"
```

---

## 14. Operator Precedence

Precedence determines which parts of an expression bind most tightly. The following table is ordered from **highest** to **lowest** precedence.

| Level | Operators or expressions | Description |
|---:|---|---|
| 1 | `(…)`, `[…]`, `{…}` | Parenthesized expression and displays |
| 2 | `x[i]`, `x[i:j]`, `x(…)`, `x.attribute` | Indexing, slicing, call, attribute access |
| 3 | `await x` | Await expression |
| 4 | `**` | Exponentiation |
| 5 | `+x`, `-x`, `~x` | Unary positive, negative, bitwise NOT |
| 6 | `*`, `@`, `/`, `//`, `%` | Multiplicative operations |
| 7 | `+`, `-` | Addition and subtraction |
| 8 | `<<`, `>>` | Bit shifts |
| 9 | `&` | Bitwise AND |
| 10 | `^` | Bitwise XOR |
| 11 | `\|` | Bitwise OR |
| 12 | `in`, `not in`, `is`, `is not`, `<`, `<=`, `>`, `>=`, `!=`, `==` | Membership, identity, and value comparisons |
| 13 | `not` | Logical NOT |
| 14 | `and` | Logical AND |
| 15 | `or` | Logical OR |
| 16 | `x if condition else y` | Conditional expression |
| 17 | `lambda` | Lambda expression |
| 18 | `:=` | Assignment expression |

### 14.1 Examples

```python
result = 2 + 3 * 4
print(result)  # 14
```

Multiplication occurs first:

```python
result = 2 + (3 * 4)
```

Parentheses change grouping:

```python
result = (2 + 3) * 4
print(result)  # 20
```

Comparison occurs before logical `and`:

```python
age = 21
has_id = True
allowed = age >= 18 and has_id
```

### 14.2 Associativity

Most same-precedence binary operators group left to right:

```python
print(20 / 5 / 2)  # (20 / 5) / 2 = 2.0
```

Exponentiation groups right to left:

```python
print(2 ** 3 ** 2)  # 2 ** (3 ** 2)
```

Conditional expressions also group right to left. Assignment expressions have the lowest precedence.

### 14.3 Best practice

Do not force readers to memorize the whole table. Use parentheses to make non-obvious intent explicit, but avoid unnecessary parentheses around very simple expressions.

```python
valid = is_active and (age >= 18 or has_permission)
```

---

## 15. Operators with Collections and Strings

The meaning of an operator depends on its operand types.

| Expression | Meaning |
|---|---|
| `"Py" + "thon"` | String concatenation |
| `[1, 2] + [3]` | List concatenation |
| `(1, 2) + (3,)` | Tuple concatenation |
| `"ha" * 3` | String repetition |
| `[0] * 3` | List repetition |
| `{1, 2} \| {2, 3}` | Set union |
| `{1, 2} & {2, 3}` | Set intersection |
| `{"a": 1} \| {"b": 2}` | Dictionary merge in Python 3.9+ |
| `value in collection` | Membership test |

### 15.1 Dictionary merge

```python
defaults = {"theme": "light", "language": "en"}
choices = {"theme": "dark"}

merged = defaults | choices
print(merged)  # {'theme': 'dark', 'language': 'en'}
```

When keys collide, the right-hand value wins.

### 15.2 In-place collection operations

```python
numbers = [1, 2]
numbers += [3, 4]

roles = {"reader"}
roles |= {"editor"}

settings = {"theme": "light"}
settings |= {"theme": "dark", "language": "en"}
```

Mutability and aliasing matter when augmented operators are used on collections.

---

## 16. The `operator` Module

The standard-library `operator` module provides function versions of many operators. It is useful with tools that expect a callable.

```python
import operator

print(operator.add(10, 5))       # 15
print(operator.mul(4, 3))        # 12
print(operator.eq("a", "a"))    # True
print(operator.contains([1, 2], 2))  # True
```

Sort records by a field:

```python
from operator import itemgetter

students = [
    {"name": "Maya", "score": 82},
    {"name": "Asha", "score": 91},
]

students.sort(key=itemgetter("score"), reverse=True)
```

Access object attributes:

```python
from operator import attrgetter

users.sort(key=attrgetter("username"))
```

Common mappings include:

| Syntax | Function |
|---|---|
| `a + b` | `operator.add(a, b)` |
| `a - b` | `operator.sub(a, b)` |
| `a * b` | `operator.mul(a, b)` |
| `a / b` | `operator.truediv(a, b)` |
| `a // b` | `operator.floordiv(a, b)` |
| `a % b` | `operator.mod(a, b)` |
| `a ** b` | `operator.pow(a, b)` |
| `a == b` | `operator.eq(a, b)` |
| `a < b` | `operator.lt(a, b)` |
| `a & b` | `operator.and_(a, b)` |
| `a \| b` | `operator.or_(a, b)` |
| `a ^ b` | `operator.xor(a, b)` |
| `b in a` | `operator.contains(a, b)` |

---

## 17. Operator Overloading

Python classes can define how operators behave through special methods.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y})"


first = Vector(2, 3)
second = Vector(4, 1)

print(first + second)  # Vector(x=6, y=4)
print(first == second) # False
```

Common special methods:

| Operator | Special method |
|---|---|
| `+` | `__add__()` |
| `-` | `__sub__()` |
| `*` | `__mul__()` |
| `/` | `__truediv__()` |
| `//` | `__floordiv__()` |
| `%` | `__mod__()` |
| `**` | `__pow__()` |
| `@` | `__matmul__()` |
| `==` | `__eq__()` |
| `<` | `__lt__()` |
| `in` | Usually uses the container's `__contains__()` |
| `&` | `__and__()` |
| `\|` | `__or__()` |

Only overload an operator when its meaning is natural and unsurprising. Return `NotImplemented` for unsupported operand types so Python can try reflected operations or raise an appropriate error.

---

## 18. Common Mistakes and Fixes

### Mistake 1: Confusing assignment and equality

```python
score = 80       # assign
score == 80      # compare
```

### Mistake 2: Using `is` instead of `==`

```python
name == "Ankita"  # value comparison
result is None    # identity check for singleton
```

### Mistake 3: Expecting exact floating-point equality

```python
from math import isclose

isclose(0.1 + 0.2, 0.3)
```

### Mistake 4: Forgetting that `/` returns a float

```python
print(8 / 2)   # 4.0
print(8 // 2)  # 4
```

### Mistake 5: Assuming floor division truncates toward zero

```python
print(-7 // 2)  # -4, not -3
```

### Mistake 6: Dividing or taking modulo by zero

```python
if denominator == 0:
    raise ValueError("denominator must not be zero")
```

### Mistake 7: Confusing logical and bitwise operators

```python
if active and authorized:  # logical condition
    grant_access()

combined_flags = flag_a | flag_b  # bitwise combination
```

### Mistake 8: Expecting `and` or `or` to always return a Boolean

```python
value = entered_value or "default"
is_available = bool(entered_value or fallback)
```

### Mistake 9: Forgetting dictionary membership checks keys

```python
"name" in profile
"Ankita" in profile.values()
```

### Mistake 10: Misreading exponentiation grouping

```python
2 ** 3 ** 2     # 2 ** (3 ** 2)
(2 ** 3) ** 2   # explicit alternative
```

### Mistake 11: Ignoring precedence

```python
average = (first + second) / 2
```

### Mistake 12: Using a complicated walrus expression

If the reader has to stop and decode it, use a normal assignment on the previous line.

### Mistake 13: Assuming `+=` always creates a new object

Augmented assignment may mutate lists, sets, dictionaries, and user-defined objects in place. Consider aliases before using it.

### Mistake 14: Treating XOR as encryption

XOR is a low-level operation, not a secure encryption system by itself. Use reviewed cryptographic libraries for sensitive data.

### Mistake 15: Using `eval()` to calculate user-entered expressions

```python
# Dangerous with untrusted input:
# result = eval(user_expression)
```

`eval()` can execute arbitrary Python code. Parse and validate allowed operations explicitly or use a safely designed expression parser.

### Mistake 16: Overloading operators with surprising behavior

`invoice_a + invoice_b` should not silently delete records or perform unrelated network actions. Operator meanings should be predictable and mostly free of unexpected side effects.

---

## 19. Clean-Code, Performance, and Security Tips

### Prefer clarity over compactness

```python
# Clear
is_eligible = age >= 18 and has_id and not is_blocked
```

Use intermediate variables when a long condition contains separate business rules.

### Use parentheses for intention

```python
allowed = is_admin or (is_active and has_permission)
```

### Rely on short-circuiting deliberately

Put a safety or inexpensive check before an expensive or potentially invalid operation:

```python
if items and expensive_check(items):
    process(items)
```

### Use the correct numeric type

- `int` for whole numbers and exact bit operations;
- `float` for approximate scientific calculations;
- `Decimal` for decimal financial rules;
- `Fraction` for exact rational arithmetic; and
- NumPy types for large numerical arrays when appropriate.

### Validate operands from untrusted sources

```python
if not isinstance(quantity, int) or isinstance(quantity, bool):
    raise TypeError("quantity must be an integer")

if quantity < 0:
    raise ValueError("quantity must not be negative")
```

`bool` is a subclass of `int`, so exclude it explicitly when `True` and `False` should not count as quantities.

### Watch for resource-exhaustion expressions

Exponentiation, huge shifts, and sequence repetition can create enormous values:

```python
# Validate limits before performing operations such as:
# 2 ** user_supplied_exponent
# 1 << user_supplied_shift
# "x" * user_supplied_count
```

### Do not optimize without measuring

Use readable expressions first. Benchmark only code that matters, with realistic data and tools such as `timeit`.

### Follow style conventions

```python
total = price * quantity
remainder = total % group_size
is_valid = minimum <= value <= maximum
```

Use spaces around binary operators. Operators with different priorities may be spaced to highlight grouping, but consistency is important.

---

## 20. Practice Exercises

### Beginner

1. Read two numbers and display their sum, difference, product, quotient, floor quotient, remainder, and power.
2. Determine whether a number is positive, negative, or zero.
3. Check whether a number is even or odd using `%`.
4. Check whether a student passed using comparison and logical operators.
5. Test whether a username exists in a list.
6. Compare two lists using both `==` and `is`, then explain the results.
7. Convert an integer to binary and apply every bitwise operator.

### Intermediate

1. Validate that a score is between `0` and `100` with a chained comparison.
2. Build a simple calculator with safe division-by-zero handling.
3. Use a conditional expression to assign a grade status.
4. Create a login rule using `and`, `or`, and `not`.
5. Use assignment operators to maintain a bank balance.
6. Use a set and membership testing to detect duplicate usernames.
7. Use the walrus operator to read commands until the user enters `quit`.
8. Build permission flags with `READ`, `WRITE`, and `EXECUTE` bits.

### Advanced

1. Compare `list_a += list_b` with `list_a = list_a + list_b` when aliases exist.
2. Write a safe function that evaluates only `+`, `-`, `*`, and `/` operations without using `eval()`.
3. Create a `Vector` class supporting `+`, `-`, `==`, and scalar multiplication.
4. Implement a role-permission system once with sets and once with bitmasks; compare readability.
5. Benchmark list membership against set membership using `timeit`.
6. Demonstrate every precedence level with a small expression.
7. Use `operator.itemgetter` to sort structured records by multiple fields.

### Output-prediction challenge

Predict every result before running the code:

```python
print(2 + 3 * 4)
print((2 + 3) * 4)
print(2 ** 3 ** 2)
print(-3 ** 2)
print(-7 // 2)
print(-7 % 2)
print("" or "Guest")
print("Python" and 0)
print(1 < 2 < 3)
print({1, 2} <= {1, 2, 3})
print(10 & 6)
print(10 ^ 6)
```

---

## 21. Mini-Projects

### 21.1 Secure login decision system

Use comparison, logical, membership, and identity operators to evaluate:

- correct username;
- password verification result;
- account status;
- allowed role membership;
- failed-attempt threshold; and
- whether optional account data is `None`.

### 21.2 Scientific calculator

Support arithmetic operators, parentheses, powers, modulo, and clear error messages. Do not pass raw user input to `eval()`.

### 21.3 File-permission simulator

Represent read, write, and execute permissions with bitmasks. Add, remove, toggle, and test each permission.

### 21.4 Student grading system

Use chained comparisons, arithmetic averages, logical requirements, augmented assignment, and conditional expressions to calculate final results.

### 21.5 Shopping-cart calculator

Calculate subtotal, percentage discount, tax, delivery cost, and final total. Validate quantities and prevent negative prices.

### 21.6 Log filter with the walrus operator

Read one log line at a time, match suspicious patterns, retain the matched result, and stop at the end of the file.

---

## 22. Mastery Roadmap

### Stage 1: Understand the symbols

- Memorize the major operator categories.
- Type each basic example yourself.
- Learn the difference between `=`, `==`, `is`, and `:=`.

### Stage 2: Predict before running

- Practise mixed arithmetic expressions.
- Learn floor division and modulo with negative numbers.
- Explain short-circuit behavior.
- Use the precedence table when unsure.

### Stage 3: Apply operators to data structures

- Use membership with strings, lists, sets, and dictionaries.
- Use `+`, `*`, `|`, `&`, `^`, and augmented forms with collections.
- Explore equality versus identity and mutable aliases.

### Stage 4: Write robust programs

- Validate divisor values and operand types.
- Compare floats appropriately.
- Avoid unsafe `eval()`;
- limit expensive user-controlled operations; and
- keep conditions readable.

### Stage 5: Explore advanced behavior

- Use `operator` functions as callables.
- Implement natural operator overloading.
- Learn reflected and in-place special methods.
- Compare bitmask and set-based designs.

### Recommended study method

1. Read one operator category.
2. Type every example rather than copying it.
3. Change the operands and predict the output.
4. Trigger expected errors intentionally.
5. Explain the behavior in plain language.
6. Solve one practice exercise without notes.
7. Apply the operator in a mini-project.

---

## 23. Complete Cheat Sheet

### Arithmetic

```python
a + b    # addition or concatenation
a - b    # subtraction or set difference
a * b    # multiplication or repetition
a / b    # true division
a // b   # floor division
a % b    # remainder
a ** b   # exponentiation
a @ b    # matrix multiplication for supported types
+a       # unary positive
-a       # unary negative
```

### Comparison

```python
a == b
a != b
a > b
a < b
a >= b
a <= b
minimum <= value <= maximum
```

### Logical

```python
a and b
a or b
not a
```

### Assignment

```python
x = value
x += value
x -= value
x *= value
x /= value
x //= value
x %= value
x **= value
x @= value
x &= value
x |= value
x ^= value
x <<= value
x >>= value
```

### Walrus

```python
if (length := len(items)) > 10:
    print(length)
```

### Membership

```python
value in collection
value not in collection
```

### Identity

```python
left is right
left is not right
value is None
```

### Bitwise

```python
a & b
a | b
a ^ b
~a
a << count
a >> count
```

### Conditional expression

```python
result = value_if_true if condition else value_if_false
```

### Essential memory rules

- `=` assigns, `==` compares values, `is` compares identities, and `:=` assigns inside an expression.
- `/` performs true division; `//` performs floor division.
- `**` groups right to left.
- `and` and `or` short-circuit and may return operands.
- `in` checks dictionary keys unless a view is specified.
- Use `is None`, not `== None`.
- `&`, `|`, `^`, and `~` are bitwise, not logical.
- Parentheses are a communication tool, not only a way to change precedence.
- Augmented assignment may mutate a mutable object in place.
- Use the walrus operator only when it makes code easier to understand.

---

## 24. Official References

- [Python Language Reference: Expressions](https://docs.python.org/3/reference/expressions.html)
- [Python Language Reference: Simple Statements](https://docs.python.org/3/reference/simple_stmts.html)
- [Python Standard Library: `operator`](https://docs.python.org/3/library/operator.html)
- [Python Standard Library: Numeric and Mathematical Modules](https://docs.python.org/3/library/numeric.html)
- [Python Tutorial: More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html)
- [PEP 572: Assignment Expressions](https://peps.python.org/pep-0572/)
- [PEP 465: Matrix Multiplication Operator](https://peps.python.org/pep-0465/)
- [PEP 8: Style Guide for Python Code](https://peps.python.org/pep-0008/)

---

## Final Note

Mastering operators is not about memorizing symbols alone. It means understanding operand types, evaluation order, return values, mutability, and the situations in which an operator expresses an idea clearly. Start with simple examples, predict results before running them, and then reinforce the concepts in small real-world programs.
