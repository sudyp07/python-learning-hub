# Function that just prints
def greet():
    print("Hello, World!")

# Call the function
greet()  # Output: Hello, World!

# Function with docstring
def welcome():
    """Prints a welcome message"""
    print("Welcome to Python!")

welcome()

# One parameter
def greet_user(name):
    print(f"Hello, {name}!")

greet_user("Alice")  # Output: Hello, Alice!

# Multiple parameters
def add_numbers(a, b):
    sum = a + b
    print(f"{a} + {b} = {sum}")

add_numbers(5, 3)  # Output: 5 + 3 = 8

# With return value
def multiply(x, y):
    return x * y

result = multiply(4, 5)
print(result)  # Output: 20