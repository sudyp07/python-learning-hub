# 🧮 Comprehensive Guide to Python Math: Built-in Functions & Standard Math Modules

Welcome to the ultimate reference guide for mathematical operations in Python. This document covers everything from Python's built-in mathematical functions to standard library modules (`math`, `cmath`, `random`, `statistics`, and `decimal`).

---

## 📋 Table of Contents
1. [Built-in Math Functions](#1-built-in-math-functions)
2. [The `math` Module (Real Numbers)](#2-the-math-module-real-numbers)
   - [Constants](#math-constants)
   - [Number Theory & Representation](#number-theory--representation)
   - [Power, Exponential & Logarithmic Functions](#power-exponential--logarithmic-functions)
   - [Trigonometric & Hyperbolic Functions](#trigonometric--hyperbolic-functions)
   - [Special Functions](#special-functions)
3. [The `cmath` Module (Complex Numbers)](#3-the-cmath-module-complex-numbers)
4. [The `statistics` Module](#4-the-statistics-module)
5. [The `random` Module (Math & Sampling)](#5-the-random-module-math--sampling)
6. [The `decimal` Module (High-Precision Math)](#6-the-decimal-module-high-precision-math)
7. [Quick Reference Cheat Sheet](#7-quick-reference-cheat-sheet)

---

## 1. Built-in Math Functions

Python includes several mathematical functions by default—no `import` needed.

```python
# Absolute Value
print(abs(-10))       # 10
print(abs(-3.14))     # 3.14

# Quotient and Remainder together
q, r = divmod(17, 5)  # Returns tuple (17 // 5, 17 % 5)
print(q, r)           # 3, 2

# Power & Modular Exponentiation
print(pow(2, 3))      # 2**3 = 8
print(pow(2, 3, 5))   # (2**3) % 5 = 3 (Significantly faster for cryptographic math)

# Rounding
print(round(3.14159, 2))  # 3.14
print(round(2.5))          # 2 (Rounds to nearest even number)

# Min, Max, and Sum
numbers = [12, 45, 2, 89, 34]
print(min(numbers))   # 2
print(max(numbers))   # 89
print(sum(numbers))   # 182
print(sum(numbers, 100)) # 282 (Starts sum with initial value 100)
```

---

## 2. The `math` Module (Real Numbers)

Import the module first:
```python
import math
```

### Math Constants
* `math.pi`: $\pi  pprox 3.141592653589793$
* `math.e`: $e  pprox 2.718281828459045$
* `math.tau`: $	au = 2\pi  pprox 6.283185307179586$
* `math.inf`: Floating-point positive infinity (`-math.inf` for negative)
* `math.nan`: Floating-point "Not a Number"

---

### Number Theory & Representation

```python
import math

# Rounding Functions
print(math.ceil(4.2))   # 5  (Rounds UP to nearest integer)
print(math.floor(4.8))  # 4  (Rounds DOWN to nearest integer)
print(math.trunc(4.8))  # 4  (Truncates fractional part towards zero)

# GCD and LCM
print(math.gcd(12, 18))       # 6   (Greatest Common Divisor)
print(math.lcm(12, 18))       # 36  (Least Common Multiple)

# Factorial and Permutations/Combinations
print(math.factorial(5))      # 120 (5!)
print(math.comb(5, 2))        # 10  (5 choose 2)
print(math.perm(5, 2))        # 20  (5 P 2)

# Floating Point Operations
print(math.fsum([0.1] * 10))  # 1.0 (Exact floating-point sum, avoids precision errors)
print(math.fabs(-5.5))        # 5.5 (Float absolute value)
print(math.copysign(5, -1))   # -5.0 (Copies sign of 2nd arg to 1st)
print(math.remainder(9, 4))   # 1.0 (IEEE 754 style remainder)

# Checks
print(math.isnan(float('nan'))) # True
print(math.isinf(float('inf'))) # True
print(math.isclose(0.1 + 0.2, 0.3)) # True (Safe float comparison)
```

---

### Power, Exponential & Logarithmic Functions

```python
import math

# Roots and Powers
print(math.sqrt(16))      # 4.0 (Square root)
print(math.isqrt(17))     # 4   (Integer square root, truncated)
print(math.cbrt(27))      # 3.0 (Cube root)
print(math.pow(2, 3))     # 8.0 (Returns float)

# Exponentials
print(math.exp(2))        # e**2
print(math.exp2(3))       # 2**3 = 8.0
print(math.expm1(1e-10))  # exp(x) - 1 (Accurate for small x)

# Logarithms
print(math.log(math.e))   # 1.0 (Natural log base e)
print(math.log(100, 10))  # 2.0 (Log base 10)
print(math.log2(8))       # 3.0 (Log base 2)
print(math.log10(100))    # 2.0 (Log base 10)
print(math.log1p(1e-10))  # log(1 + x) (Accurate for small x)
```

---

### Trigonometric & Hyperbolic Functions

> ⚠️ All trigonometric functions expect angles in **radians**.

```python
import math

# Angle Conversions
rad = math.radians(180)   # 3.14159... (Degrees to Radians)
deg = math.degrees(math.pi) # 180.0     (Radians to Degrees)

# Standard Trigonometry
print(math.sin(rad))      # ~0.0
print(math.cos(rad))      # -1.0
print(math.tan(rad))      # ~0.0

# Inverse Trigonometry
print(math.asin(1))       # pi/2
print(math.acos(0))       # pi/2
print(math.atan(1))       # pi/4
print(math.atan2(1, 1))   # atan(y / x) - Handles quadrant correctly

# Distance / Euclidean Norm
print(math.hypot(3, 4))       # 5.0 (sqrt(3^2 + 4^2))
print(math.dist((0,0), (3,4)))# 5.0 (Euclidean distance between two points)

# Hyperbolic Functions
print(math.sinh(1))
print(math.cosh(1))
print(math.tanh(1))
```

---

## 3. The `cmath` Module (Complex Numbers)

For mathematical operations on complex numbers ($z = a + bi$):

```python
import cmath

z = 3 + 4j

# Polar / Rectangular Coordinates
r, phi = cmath.polar(z)      # r = 5.0, phi = angle in radians
print(r, phi)
z_rect = cmath.rect(r, phi)  # Converts back to (3+4j)

# Phase & Absolute Value
print(cmath.phase(z))        # Phase angle
print(abs(z))                # Magnitude (5.0)

# Square root of negative numbers
print(cmath.sqrt(-1))        # 1j
print(cmath.sin(z))          # Complex sine
```

---

## 4. The `statistics` Module

Provides functions for calculating mathematical statistics of numeric data.

```python
import statistics

data = [10, 20, 20, 30, 40, 50, 60]

# Measures of Central Tendency
print(statistics.mean(data))          # 32.857...
print(statistics.fmean(data))         # Faster float mean
print(statistics.median(data))        # 30
print(statistics.mode(data))          # 20
print(statistics.multimode([1,1,2,2]))# [1, 2]

# Measures of Spread
print(statistics.stdev(data))         # Sample standard deviation
print(statistics.variance(data))      # Sample variance
print(statistics.pvariance(data))     # Population variance

# Quantiles
print(statistics.quantiles(data, n=4))# Cut points for 4 intervals (Quartiles)
```

---

## 5. The `random` Module (Math & Sampling)

Functions for pseudo-random number generation.

```python
import random

# Random Integers & Floats
print(random.randint(1, 10))     # Integer between 1 and 10 (inclusive)
print(random.randrange(0, 10, 2))# Even integer between 0 and 8
print(random.random())           # Float between 0.0 and 1.0
print(random.uniform(1.5, 5.5))  # Float between 1.5 and 5.5

# Sequences & Sampling
items = ['A', 'B', 'C', 'D']
print(random.choice(items))      # Pick 1 random element
print(random.choices(items, k=2))# Pick 2 elements (with replacement)
print(random.sample(items, k=2)) # Pick 2 unique elements (without replacement)

random.shuffle(items)            # Shuffles list in-place
print(items)
```

---

## 6. The `decimal` Module (High-Precision Math)

Standard floating point numbers suffer from binary representation errors (e.g., `0.1 + 0.2 != 0.3`). Use `Decimal` for financial or exact precision math.

```python
from decimal import Decimal, getcontext

# Standard float issue:
print(0.1 + 0.2)  # 0.30000000000000004

# Fixed with Decimal (Pass values as strings!)
d1 = Decimal('0.1')
d2 = Decimal('0.2')
print(d1 + d2)    # Decimal('0.3')

# Customizing Precision
getcontext().prec = 6  # Set precision to 6 digits
print(Decimal(1) / Decimal(7))  # Decimal('0.142857')
```

---

## 7. Quick Reference Cheat Sheet

| Task | Code Example | Module |
| :--- | :--- | :--- |
| **Power** | `pow(b, e)` / `b ** e` | Built-in |
| **Exact Sum** | `math.fsum([0.1, 0.2])` | `math` |
| **Square Root** | `math.sqrt(x)` | `math` |
| **GCD / LCM** | `math.gcd(a, b)` / `math.lcm(a, b)` | `math` |
| **Factorial** | `math.factorial(n)` | `math` |
| **Distance** | `math.dist(p1, p2)` | `math` |
| **Degrees to Radians** | `math.radians(deg)` | `math` |
| **Complex Sqrt** | `cmath.sqrt(-1)` | `cmath` |
| **Average / Mean** | `statistics.mean(data)` | `statistics` |
| **Exact Decimals** | `Decimal('0.1') + Decimal('0.2')` | `decimal` |

Happy Coding! 🚀