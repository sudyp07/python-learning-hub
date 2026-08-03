## Hypotenuse of a Right-Angled Triangle
import math

a = float(input("Enter side a: "))   # Example: 3
b = float(input("Enter side b: "))   # Example: 4

# Calculate the hypotenuse using the Pythagorean theorem
c = math.sqrt(pow(a, 2) + pow(b, 2))

print(f"Side c = {round(c, 2)}")
# Output: Side c = 5.0


# Here, [math.sqrt(pow(a, 2) + pow(b, 2))] means:
"""
pow(a, 2)
- Raises side 'a' to the power of 2 (squares side a).
- Example:
    pow(3, 2) = 9
    (Same as: 3 ** 2)

pow(b, 2)
- Raises side 'b' to the power of 2 (squares side b).
- Example:
    pow(4, 2) = 16
    (Same as: 4 ** 2)

pow(a, 2) + pow(b, 2)
- Adds the squares of both sides.
- Example:
    9 + 16 = 25

math.sqrt(...)
- Returns the square root of the result.
- Example:
    math.sqrt(25) = 5

Formula:
- c = √(a² + b²)
- This is known as the Pythagorean theorem and is used to find the
  hypotenuse (longest side) of a right-angled triangle.

round(c, 2)
- Rounds the calculated hypotenuse to 2 decimal places.
- Example:
    5.123456 → 5.12
"""