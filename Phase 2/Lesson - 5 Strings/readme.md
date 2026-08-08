# 🔤 Master Class: Python Strings & Methods (0 to Hero)

Welcome to the ultimate guide to **Python Strings**. This document takes you from absolute beginner concepts—like creation and slicing—to advanced topics like encoding, memory optimization, and regex-free string transformations.

---

## 📋 Table of Contents
1. [String Fundamentals & Immutability](#1-string-fundamentals--immutability)
2. [Indexing and Slicing](#2-indexing-and-slicing)
3. [Escape Sequences & Raw Strings](#3-escape-sequences--raw-strings)
4. [String Formatting Techniques](#4-string-formatting-techniques)
5. [Complete String Methods Reference](#5-complete-string-methods-reference)
   - [Case Conversions](#case-conversions)
   - [Searching & Counting](#searching--counting)
   - [Validation & Checks](#validation--checks)
   - [Trimming & Alignment](#trimming--alignment)
   - [Splitting, Partitioning & Joining](#splitting-partitioning--joining)
   - [Replacing & Translation Tables](#replacing--translation-tables)
6. [Unicode, Encoding & Decoding](#6-unicode-encoding--decoding)
7. [Performance & Memory Considerations](#7-performance--memory-considerations)
8. [Quick Reference Cheat Sheet](#8-quick-reference-cheat-sheet)

---

## 1. String Fundamentals & Immutability

A **string** in Python is a sequence of Unicode characters enclosed in single quotes (`'...'`), double quotes (`"..."`), or triple quotes (`'''...'''` / `"""..."""`).

```python
# Creating strings
single = 'Hello'
double = "World"
multiline = """This is a 
multi-line string."""
```

### 🔒 Immutability
Strings in Python are **immutable**. Once created, their contents cannot be altered in memory.

```python
s = "Python"
# s[0] = "J"  # ❌ TypeError: 'str' object does not support item assignment

# Correct approach: Create a new string
s = "J" + s[1:]  # Creates "Jython"
```

---

## 2. Indexing and Slicing

Strings are zero-indexed sequences. Python supports both positive (left-to-right) and negative (right-to-left) indexing.

### Indexing Map (`"PYTHON"`)
```
 Forward Index:    0    1    2    3    4    5
 Character:        P    Y    T    H    O    N
 Reverse Index:   -6   -5   -4   -3   -2   -1
```

```python
s = "PYTHON"
print(s[0])   # 'P'
print(s[-1])  # 'N'
```

### Slicing Syntax
$$\text{string}[\text{start} : \text{stop} : \text{step}]$$

* `start`: Inclusive starting index (default: 0)
* `stop`: Exclusive ending index (default: end of string)
* `step`: Increment value (default: 1)

```python
s = "Hello World"

print(s[0:5])      # 'Hello' (index 0 to 4)
print(s[6:])       # 'World' (index 6 to end)
print(s[:5])       # 'Hello' (start to index 4)
print(s[::2])      # 'HloWrd' (every 2nd character)
print(s[::-1])     # 'dlroW olleH' (Reverses string)
```

---

## 3. Escape Sequences & Raw Strings

### Common Escape Characters
| Sequence | Description | Example Output |
| :--- | :--- | :--- |
| `\n` | Newline | Breaks line |
| `\t` | Horizontal Tab | Indents text |
| `\\` | Backslash (`\`) | Includes `\` |
| `\'` | Single Quote | Includes `'` |
| `\"` | Double Quote | Includes `"` |

### Raw Strings (`r"..."`)
Prefixing a string with `r` or `R` treats backslashes as literal characters. Crucial for file paths and Regular Expressions.

```python
path = r"C:\Users\Name\Documents"
print(path)  # Outputs: C:\Users\Name\Documents
```

---

## 4. String Formatting Techniques

### 1. f-Strings (PEP 498 - Python 3.6+) **[Recommended]**
Fast, readable, and supports inline Python expressions.

```python
name = "Alice"
age = 25

# Basic interpolation
print(f"Name: {name}, Age: {age}")

# Expressions inside f-strings
print(f"Next year: {age + 1}")
print(f"Uppercase: {name.upper()}")

# Self-documenting expressions (Python 3.8+)
print(f"{name=}, {age=}")  # Outputs: name='Alice', age=25

# Formatting number specifiers
pi = 3.14159265
print(f"Pi to 2 decimal places: {pi:.2f}")  # 3.14
large_num = 1000000000
print(f"Formatted: {large_num:,}")         # 1,000,000,000
```

### 2. `.format()` Method
```python
print("Hello {}, you are {} years old.".format(name, age))
print("Hello {1}, you are {0} years old.".format(age, name))  # Positional
```

### 3. `%` Formatting (Legacy)
```python
print("Hello %s, pi is %.2f" % ("Bob", 3.14159))
```

---

## 5. Complete String Methods Reference

Python provides over 40 built-in methods for string manipulation.

### Case Conversions

```python
s = "python PROGRAMMING"

print(s.upper())      # "PYTHON PROGRAMMING"
print(s.lower())      # "python programming"
print(s.capitalize()) # "Python programming"
print(s.title())      # "Python Programming"
print(s.swapcase())   # "PYTHON programming"
print(s.casefold())   # Aggressive lowercasing for caseless matching (e.g., German 'ß' -> 'ss')
```

### Searching & Counting

```python
text = "Python is awesome, Python is fast."

# .find() & .rfind() - Return index or -1 if not found
print(text.find("Python"))     # 0
print(text.rfind("Python"))    # 19
print(text.find("Java"))       # -1

# .index() & .rindex() - Same as find, but raises ValueError if missing
print(text.index("awesome"))   # 10

# .count() - Occurrences of substring
print(text.count("Python"))    # 2
```

### Validation & Checks
All return boolean `True` or `False`.

```python
s = "Python3"

print(s.isalpha())   # False (has digit 3)
print(s.isdigit())   # False
print(s.isalnum())   # True (letters and numbers only)
print(s.isnumeric()) # False

s2 = "   "
print(s2.isspace())  # True

s3 = "Hello World"
print(s3.istitle())  # True
print(s3.islower())  # False
print(s3.isupper())  # False

# Prefix and Suffix
filename = "data_report.csv"
print(filename.startswith("data")) # True
print(filename.endswith(".csv"))   # True
```

### Trimming & Alignment

```python
raw = "   hello world   "

# Trimming whitespace
print(raw.strip())   # "hello world"
print(raw.lstrip())  # "hello world   "
print(raw.rstrip())  # "   hello world"

# Custom character trimming
code = "###python###"
print(code.strip("#")) # "python"

# Padding & Alignment
word = "Python"
print(word.center(10, "*")) # "**Python**"
print(word.ljust(10, "-"))  # "Python----"
print(word.rjust(10, "-"))  # "----Python"
print("42".zfill(5))         # "00042" (Zero-padding)
```

### Splitting, Partitioning & Joining

```python
csv = "apple,banana,cherry,date"

# .split() - Splits by delimiter into a list
fruits = csv.split(",")  # ['apple', 'banana', 'cherry', 'date']

# .rsplit() - Splits from right with maxsplit
print(csv.rsplit(",", maxsplit=2)) # ['apple,banana', 'cherry', 'date']

# .join() - Joins iterable into a string (High performance)
print(" | ".join(fruits))  # "apple | banana | cherry | date"

# .partition() - Returns 3-tuple: (before, separator, after)
data = "user@domain.com"
username, sep, domain = data.partition("@")
print(username) # "user"
print(domain)   # "domain.com"

# .splitlines() - Splits at line breaks
multi = "Line 1\nLine 2\nLine 3"
print(multi.splitlines()) # ['Line 1', 'Line 2', 'Line 3']
```

### Replacing & Translation Tables

```python
text = "I love Java. Java is great."

# Simple replacement
print(text.replace("Java", "Python")) # "I love Python. Python is great."
print(text.replace("Java", "Python", 1)) # Replaces first occurrence only

# Advanced multi-character mapping via .maketrans() and .translate()
vowels = "aeiou"
replacement = "12345"
trans_table = str.maketrans(vowels, replacement)

code_phrase = "hello world"
print(code_phrase.translate(trans_table)) # "h2ll4 w4rld"
```

---

## 6. Unicode, Encoding & Decoding

Python strings are UTF-8 Unicode by default.

```python
# Character to ASCII/Unicode code point
print(ord("A"))  # 65
print(ord("🐍")) # 128013

# Code point to character
print(chr(65))     # 'A'
print(chr(128013)) # '🐍'

# Encoding str -> bytes
text = "Python 🐍"
encoded_bytes = text.encode("utf-8")
print(encoded_bytes) # b'Python \xf0\x9f\x90\x8d'

# Decoding bytes -> str
decoded_text = encoded_bytes.decode("utf-8")
print(decoded_text)  # "Python 🐍"
```

---

## 7. Performance & Memory Considerations

### 1. Efficient Concatenation
Avoid using `+` in loops because strings are immutable; every `+` allocates a new string in memory ($O(N^2)$ complexity).

```python
# ❌ BAD: Memory inefficient O(N^2)
result = ""
for char in ["P", "y", "t", "h", "o", "n"]:
    result += char

# ✅ GOOD: Memory efficient O(N)
char_list = ["P", "y", "t", "h", "o", "n"]
result = "".join(char_list)
```

### 2. String Interning
Python automatically caches (interns) certain small strings or identifier-like strings to save memory and optimize comparisons.

```python
import sys

a = "python"
b = "python"
print(a is b)  # True (Points to exact same memory object)

# Manual interning for dynamically generated strings
c = sys.intern("a long dynamic string")
d = sys.intern("a long dynamic string")
print(c is d)  # True
```

---

## 8. Quick Reference Cheat Sheet

| Category | Method | Description |
| :--- | :--- | :--- |
| **Case** | `.upper()` / `.lower()` | Convert all chars to upper/lower case |
| **Case** | `.title()` / `.capitalize()` | Capitalize words or first letter |
| **Search** | `.find(sub)` | Return index of sub or `-1` |
| **Search** | `.count(sub)` | Count non-overlapping occurrences |
| **Check** | `.isalpha()` / `.isdigit()` | Check if string contains only letters / digits |
| **Check** | `.startswith(sub)` / `.endswith(sub)` | Check prefix or suffix |
| **Trim** | `.strip()` | Remove leading & trailing whitespace |
| **Split/Join**| `.split(sep)` | Split string into list by separator |
| **Split/Join**| `.join(iterable)` | Combine iterable elements into string |
| **Modify** | `.replace(old, new)` | Replace occurrences of substring |
| **Format** | `f"{var}"` | Interpolate expressions directly |

Happy Coding! 🚀