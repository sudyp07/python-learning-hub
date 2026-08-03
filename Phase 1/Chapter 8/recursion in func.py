## it is a function which calls itself
## ITS IS VERY IMPORTANT TO CODE A FULL ALGORITHM WITH SOME LINES OF CODE !!

"""
factorial(1!) = 1
factorial(0!) = 1
factorial(2!) = 2 x 1 = 2
factorial(3!) = 3 x 2 x 1 = 6
factorial(4!) = 4 x 3 x 2 x 1 = 24
factorial(5!) = 5 x 4 x 3 x 2 x 1 = 120

formula of factorial --> factorial(n) = n * factorial(n-1)
"""

def factorial(n):
    if (n == 0 or n == 1):
        return 1
    else:
        return n * factorial(n-1)

n = int(input("Enter a number: "))
print(f'Factorial of {n} is {factorial(n)}')

'''IMPORTANT:
The programmer needs to be extremely careful while working with recursion to ensure that the function
doesn’t infinitely keep calling itself. Recursion is sometimes the most direct way to code on algorithm.'''
