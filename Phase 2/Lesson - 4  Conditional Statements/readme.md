# Python Conditional Expressions: From Beginner to Pro

A comprehensive, hands-on guide to mastering decision-making logic, control flow, truthiness, pattern matching, and performance optimization in Python.

---

## Table of Contents
1. [Chapter 1: Beginner — Fundamentals of Decision Making](#chapter-1-beginner--fundamentals-of-decision-making)
   - 1.1 What is Conditional Logic?
   - 1.2 Comparison Operators
   - 1.3 `if`, `elif`, and `else` Statements
   - 1.4 Indentation and Code Blocks
2. [Chapter 2: Intermediate — Combining Logic & Inlining](#chapter-2-intermediate--combining-logic--inlining)
   - 2.1 Logical Operators (`and`, `or`, `not`)
   - 2.2 Short-Circuit Evaluation
   - 2.3 The Ternary Operator (`value if condition else alternative`)
   - 2.4 Chained Comparison Operators
3. [Chapter 3: Advanced — Truthiness & Assignment Expressions](#chapter-3-advanced--truthiness--assignment-expressions)
   - 3.1 Truth Value Testing (Truthy vs. Falsy)
   - 3.2 Customizing Truthiness with `__bool__` and `__len__`
   - 3.3 The Walrus Operator (`:=`) in Conditionals
4. [Chapter 4: Master — Structural Pattern Matching (`match/case`)](#chapter-4-master--structural-pattern-matching-matchcase)
   - 4.1 Syntax and Basics
   - 4.2 Sequence & Mapping Patterns
   - 4.3 Guard Conditions (`if`)
   - 4.4 Object/Class Pattern Matching
5. [Chapter 5: Pro — Architecture, Performance & Refactoring](#chapter-5-pro--architecture-performance--refactoring)
   - 5.1 Replacing Deeply Nested Logic with Guard Clauses
   - 5.2 Dispatch Tables (Dictionaries vs. Conditionals)
   - 5.3 Performance Overhead of Dynamic Evaluations
   - 5.4 Common Anti-Patterns and Refactoring Exercises

---

# Chapter 1: Beginner — Fundamentals of Decision Making

## 1.1 What is Conditional Logic?
In programming, conditional logic allows code to execute different instructions based on whether a specified condition evaluates to `True` or `False`. It forms the backbone of dynamic decision-making in software.

## 1.2 Comparison Operators
Python provides six primary comparison operators that return boolean values (`True` or `False`):

| Operator | Meaning | Example | Result |
| :--- | :--- | :--- | :--- |
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `7 > 10` | `False` |
| `<` | Less than | `3 < 8` | `True` |
| `>=` | Greater than or equal to | `5 >= 5` | `True` |
| `<=` | Less than or equal to | `4 <= 2` | `False` |

## 1.3 `if`, `elif`, and `else` Statements
The standard syntax evaluates conditions sequentially from top to bottom. Once a condition evaluates to `True`, its corresponding block executes, and the rest of the chain is skipped.

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"Grade: {grade}")  # Grade: B
```

## 1.4 Indentation and Code Blocks
Unlike languages that use braces `{}` (like C++ or JavaScript), Python relies strictly on **whitespace indentation** (conventionally 4 spaces) to define execution scopes.

```python
is_admin = True

if is_admin:
    print("Access Granted")
    print("Welcome to the Admin Console")
print("System Check Complete")  # Runs regardless of condition
```

---

# Chapter 2: Intermediate — Combining Logic & Inlining

## 2.1 Logical Operators (`and`, `or`, `not`)
Logical operators combine multiple boolean expressions.

- `and`: Evaluates to `True` only if **all** expressions are `True`.
- `or`: Evaluates to `True` if **at least one** expression is `True`.
- `not`: Inverts the boolean result of an expression.

```python
age = 25
has_license = True
is_intoxicated = False

if age >= 18 and has_license and not is_intoxicated:
    print("Allowed to drive.")
```

## 2.2 Short-Circuit Evaluation
Python optimizes condition evaluation by stopping as soon as the final result is determined.

- **For `and`**: If the first condition is `False`, remaining conditions are ignored.
- **For `or`**: If the first condition is `True`, remaining conditions are ignored.

```python
def expensive_check():
    print("Executing expensive query...")
    return True

# expensive_check() IS NOT EXECUTED because the first argument is False
if False and expensive_check():
    pass
```

## 2.3 The Ternary Operator
Python allows concise inline conditional assignment using the ternary syntax:

$$	ext{value\_if\_true} \quad 	ext{if} \quad 	ext{condition} \quad 	ext{else} \quad 	ext{value\_if\_false}$$

```python
age = 20
status = "Adult" if age >= 18 else "Minor"

# Useful in string formatting
print(f"User is an {'active' if is_active else 'inactive'} member.")
```

## 2.4 Chained Comparison Operators
Python permits mathematical range chaining without needing explicit `and` clauses.

```python
x = 15

# Instead of: if x > 10 and x < 20:
if 10 < x < 20:
    print("x is strictly between 10 and 20")
```

---

# Chapter 3: Advanced — Truthiness & Assignment Expressions

## 3.1 Truth Value Testing (Truthy vs. Falsy)
Objects in Python evaluate to either `True` or `False` when placed inside a boolean context.

### Falsy Objects in Python:
- `None` and `False`
- Numeric zeros: `0`, `0.0`, `0j`, `Decimal(0)`
- Empty sequences and collections: `""`, `()`, `[]`, `{}`, `set()`, `range(0)`

```python
items = []

# Pythonic check for non-empty sequence
if items:
    print("Processing items...")
else:
    print("No items to process.")
```

## 3.2 Customizing Truthiness with `__bool__` and `__len__`
You can define how custom objects evaluate in boolean contexts by implementing `__bool__()` or `__len__()` methods.

```python
class Account:
    def __init__(self, balance):
        self.balance = balance

    def __bool__(self):
        return self.balance > 0

acc1 = Account(100)
acc2 = Account(0)

if acc1:
    print("Account 1 active")  # Executed

if not acc2:
    print("Account 2 inactive")  # Executed
```

## 3.3 The Walrus Operator (`:=`) in Conditionals
Introduced in Python 3.8, the assignment expression operator enables variable assignment *within* a conditional evaluation.

```python
import re

text = "Error Code: 404 Found"

# Assign match inside the condition
if (match := re.search(r'\d+', text)):
    print(f"Extracted code: {match.group(0)}")
```

---

# Chapter 4: Master — Structural Pattern Matching (`match/case`)

Introduced in Python 3.10, structural pattern matching replaces verbose `if/elif` chains with declarative pattern recognition.

## 4.1 Syntax and Basics
```python
def process_command(command):
    match command.split():
        case ["quit"]:
            print("Exiting...")
        case ["load", filename]:
            print(f"Loading {filename}...")
        case ["save", filename]:
            print(f"Saving {filename}...")
        case _:
            print("Unknown command")

process_command("load data.csv")  # Output: Loading data.csv...
```

## 4.2 Sequence & Mapping Patterns
`match/case` can decompose structured data like dictionaries and nested lists directly.

```python
user = {"name": "Alice", "role": "admin"}

match user:
    case {"name": name, "role": "admin"}:
        print(f"Admin user detected: {name}")
    case {"name": name}:
        print(f"Standard user: {name}")
```

## 4.3 Guard Conditions (`if`)
You can append an `if` guard to a `case` block for refined filtering.

```python
def evaluate_number(n):
    match n:
        case x if x < 0:
            print("Negative number")
        case x if x % 2 == 0:
            print("Even positive number")
        case _:
            print("Odd positive number")
```

---

# Chapter 5: Pro — Architecture, Performance & Refactoring

## 5.1 Replacing Deeply Nested Logic with Guard Clauses
Nested conditions reduce readability and maintainability. Guard clauses fail fast and exit early.

### Bad (Deeply Nested):
```python
def process_payment(user, amount):
    if user is not None:
        if user.is_active:
            if user.balance >= amount:
                user.balance -= amount
                return True
            else:
                raise ValueError("Insufficient funds")
        else:
            raise PermissionError("User inactive")
    else:
        raise ValueError("User not found")
```

### Pro Refactoring (Guard Clauses):
```python
def process_payment(user, amount):
    if user is None:
        raise ValueError("User not found")
    if not user.is_active:
        raise PermissionError("User inactive")
    if user.balance < amount:
        raise ValueError("Insufficient funds")

    user.balance -= amount
    return True
```

## 5.2 Dispatch Tables (Dictionaries vs. Conditionals)
For static mapping operations, dictionary lookup tables are $O(1)$ and cleaner than long `elif` chains.

```python
# Instead of long if/elif chain for operations:
def add(x, y): return x + y
def sub(x, y): return x - y
def mul(x, y): return x * y

OPERATIONS = {
    "add": add,
    "sub": sub,
    "mul": mul
}

def execute(op, x, y):
    handler = OPERATIONS.get(op)
    if not handler:
        raise ValueError(f"Unsupported operation: {op}")
    return handler(x, y)
```

## 5.3 Anti-Patterns and Best Practices
1. **Never explicitly compare to `True`/`False`**: Write `if is_valid:` instead of `if is_valid == True:`.
2. **Never check length for empty sequences**: Write `if not items:` instead of `if len(items) == 0:`.
3. **Avoid overly complex ternary expressions**: If a ternary spans multiple lines or nested conditions, refactor to standard block syntax for readability.