# Conditional Expressions ( method of writing if else statement in shortform or in one line) -->

# Example 1: Normal if...else
age = 20

if age >= 18:
    message = "Adult"     ## THIS IS LONG VERSION THAT TAKES 4 LINES ATLEAST .
else:
    message = "Minor"
print(f'S/He is {message}.')


# Example 2: Conditional Expression (Shortcut)

age = 2

message = "Adult" if age >= 18 else "Minor"  ## THIS IS SHORT VERSION THAT TAKES A SINGLE LINE ONLY.
print(f'S/He is {message}.')


# Example 3 : Shortcut

number = int(input("Enter a number: "))

checker = "Even" if number % 2 == 0 else "Odd"
print(f'The number you have given is {checker}.')

# IMPORTANT ⚡‼️: You cannot use the elif keyword inside a conditional expression.