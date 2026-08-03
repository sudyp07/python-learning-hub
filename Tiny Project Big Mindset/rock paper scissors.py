import random
choices = ["rock", "paper", "scissors"]
user_input = input("Enter your choice: ").lower()
computer = random.choice(choices)


## raise system error if invalid input does by the user
if user_input not in choices:
    print("Invalid input!")
    raise SystemExit
else:
    print("*****************************")
    print(f"you chose {user_input}")
    print(f"Computer chooses: {computer}")
    print("*****************************")


## Logic of main game starts here:
if user_input == computer:
    print("Game Draw")

elif user_input == "rock" and computer == "scissors":
    print("You Win!🥇✅")

elif user_input == "paper" and computer == "rock":
    print("You Win!🥇✅")

elif user_input == "scissors" and computer == "paper":
    print("You Win!🥇✅")

else:
    print("Computer Wins!☠️")
