"""****************************************************************************"""
## factorial printer ( 1 * 2 * 3 * 4 * 5) = 120
def factorial(n):
    if n == 1 or n == 0:
        return 1
    else:
        return n * factorial(n-1)

n = int(input("Enter a number: "))
factorial(n)
print(factorial(n))
"""****************************************************************************"""

## factorial printer ( 1 + 2 + 3 + 4 + 5)  = 15
def total(numbers):
    if numbers == 0:
        return 0
    else:
        return numbers + total(numbers - 1)


numbers = int(input("Enter a number: "))
print(total(numbers))
"""****************************************************************************"""