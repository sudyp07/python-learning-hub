# CALCULATE THE AREA OF THE CIRCLE -->
import math
user_input = float(input('Enter the radius of the circle: '))  # Example: 5
area = math.pi * pow(user_input, 2)
print(f"The area of a circle is: {round(area, 2)} cm²")
# Output: The area of a circle is: 78.54 cm²

# Here, [math.pi * pow(user_input, 2)] means:
"""
math.pi
- Represents the mathematical constant π (pi), approximately 3.14159.

pow(user_input, 2)
- Raises the radius to the power of 2 (squares the radius).
- Example:
    pow(5, 2) = 25
    (Same as: 5 ** 2)

math.pi * pow(user_input, 2)
- Multiplies π by the square of the radius.
- Formula:
    Area = π × r²

round(area, 2)
- Rounds the calculated area to 2 decimal places.
- Example:
    78.5398163397 → 78.54
"""
