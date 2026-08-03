import random
correct_pin  = random.randint(1, 5)
attempts = 0

while True:
    user_input = int(input("Enter your pin: "))

    if correct_pin == user_input:
        print("Access granted")
        break
    else:
        print("Wrong pin entered, try again")

    attempts += 1


# This is a while loop program and it will runs till you entered the correct number.