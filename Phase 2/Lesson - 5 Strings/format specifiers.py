price_1 = 3.2346246
price_2 = -554.5643223
price_3 = 15.6784236


print(f"Price 1 is ${price_1:.2f}")  #  Price 1 is $3.23
print(f"Price 2 is ${price_2:.2f}")  #  Price 2 is $-554.56
print(f"Price 3 is ${price_3:.2f}")  #  Price 3 is $15.68

# ==========================
# Python Format Specifiers Demo
# ==========================

name = "Sudip"
age = 23
height = 5.789
salary = 1234567.891
score = 0.925

# Default output
print(f"Name: {name}") #Name: Sudip

# Right align inside 15 spaces
print(f"Right Align : |{name:>15}|")#Right Align : |          Sudip|

# Left align
print(f"Left Align  : |{name:<15}|") # Left Align  : |Sudip          |

# Center align
print(f"Center Align: |{name:^15}|") #Center Align: |     Sudip     |

# Fill empty spaces with *
print(f"Fill         : |{name:*^15}|") # Fill         : |*****Sudip*****|

# Integer formatting
print(f"Age          : {age:d}") # Age          : 23

# Zero padding
print(f"Age          : {age:04}") #Age          : 0023

# Float with 2 decimal places
print(f"Height       : {height:.2f}")#Height       : 5.79

# Float with 4 decimal places
print(f"Height       : {height:.4f}")# Height       : 5.7890

# Salary with commas
print(f"Salary       : {salary:,.2f}") # Salary       : 1,234,567.89

# Percentage
print(f"Score        : {score:.1%}") # Score        : 92.5%

# Binary
print(f"Binary Age   : {age:b}") #Binary Age   : 10111

# Octal
print(f"Octal Age    : {age:o}") #Octal Age    : 27

# Hexadecimal
print(f"Hex Lower    : {age:x}") # Hex Lower    : 17

# Hexadecimal Upper
print(f"Hex Upper    : {age:X}") # Hex Upper    : 17

# Scientific notation
print(f"Scientific   : {salary:e}")  # Scientific   : 1.234568e+06

# Always show sign
print(f"Positive     : {age:+}") # Positive     : +23

# Width + commas + decimals
print(f"Salary       : {salary:15,.2f}") # Salary       :    1,234,567.89

# String precision (first 3 characters only)
print(f"Short Name   : {name:.3}")  # Short Name   : Sud

# Width + precision for string
print(f"Width+Prec   : |{name:10.3}|")  # Width+Prec   : |Sud       |