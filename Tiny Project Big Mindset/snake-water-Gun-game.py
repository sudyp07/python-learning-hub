## snake water gun game is as same as ROCK, PAPER , SCISSORS gamee --> LETS MAKE IT
import random
user_input = input("Please Select One: Snake, Water or Gun: ").lower()
choice = ["snake", "water", "gun"]
computer = random.choice(choice)


## checking userinput is right or wrong, if right continue , if wrong it exit
if user_input not in choice:
    print("Invalid input!")
    raise SystemExit
else:
    print(f"Computer chooses: {computer}")


## from here real game starts working :)
if user_input == computer:
    print("GAME DRAW 🤝")

elif user_input == "snake" and computer == "water":
    print("Snake Won the game 🐍🥇")

elif user_input == "water" and computer == "gun":
    print("Water Won the game 💧🥇")

elif user_input == "gun" and computer == "snake":
    print("Gun Won the game 🔫🥇")

else:
    print("Computer Wins! 😢")