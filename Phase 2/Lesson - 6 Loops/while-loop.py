# while loop = execute some code WHILE some condition remains true

name = input("Enter your name: ")

while name == "":
    print("Your name is empty")
    name = input("Enter your name: ")

print("Hello " + name)  ## Hello Sudip

# EXAMPLE - 1 --> Using and logical operator

age = int(input("Enter your age: "))

while age <= 0 and age > 100:
    print("Your age is too high")
    age = int(input("Enter your age: "))

print("Login Sucessful")

## EXAMPLE - 2 --> Using not logical operator

food = input("Enter your food you like (q to quit): ")

while not food == "q":
    print(f'You Choose {food}')
    food = input("Enter another food you like (q to quit): ")

print("Bye babee !")

## EXAMPLE - 3 --> Using or logical operator

number = int(input("Enter a number 1-10: "))

while   number < 1 or number > 10:
    print(f"{number} is out of range")
    number = int(input("Enter a number 1-10: "))

print(f"Your number is {number}.")














