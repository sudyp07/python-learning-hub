# # python quiz game

questions = (
    "How many elements are there in the periodic table?: ",
    "Which animal lays the largest eggs?: ",
    "What is the most abundant gas in Earth's atmosphere?: ",
    "How many bones are there in the human body?: ",
    "Which planet is the hottest planet in the solar system?: ",
)

options = (
    ("A. 116", "B. 117", "C. 118", "D. 119"),
    ("A. Elephant", "B. Ostrich", "C. Crocodile", "D. Penguin"),
    ("A. Oxygen", "B. Carbon Dioxide", "C. Nitrogen", "D. Hydrogen"),
    ("A. 206", "B. 208", "C. 210", "D. 212"),
    ("A. Mercury", "B. Venus", "C. Mars", "D. Jupiter"),
)

answers = ("C", "B", "C", "A", "B")
guesses = []
score = 0
question_num = 0

for question in questions:
    print("-----------------------")
    print(question)
    for option in options[question_num]:
        print(option)

    guess = input("Enter your guess --> (A,B,C,D):  ").upper()
    guesses.append(guess)
    if guess == answers[question_num]:
        score += 1
        print("You guessed the answer!")
    else:
        print("Sorry, you did not guess the right answer!")
        print(f"{answers[question_num]} is the correct answer!")
    question_num = question_num + 1

print("---------------------")
print("       RESULT        ")
print("---------------------")

print('answers:  ', end = " ")
for answer in answers:
    print(answer, end = " ")
print()

print('Guesses:  ', end = " ")
for guess in guesses:
    print(guess, end = " ")
print()

score =  int(score / len(questions) * 100)
print(f"Your final score is: {score}%")








