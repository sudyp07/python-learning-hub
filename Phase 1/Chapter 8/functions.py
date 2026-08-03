# # functions in py , whihch is a group of statement to perform a specific task with minimal code
# # making simple functions

def greet():
        print("Sudeep is a Boss✅")
greet()   ## functions call # when we call the functions it will Print Sudeep is a Boss✅

# # if you want to take a average of 3 numbers at once , you can just use it for once
num1 = 98
num2 = 55
num3 = 67
average = (num1 + num2 + num3 )/ 3
print(f"{average:.2f}")

# # but with function it will be more easy and can take input as much as you can by increasing functions call
# # functions definitions
def avg():
    user1 = int(input("Enter a number: "))
    user2 = int(input("Enter a number: "))
    user3 = int(input("Enter a number: "))

    average = (user1 + user2 + user3) / 3
    print(f"{average:.1f}")

# # you can ask for input as much as you can by increasing functions call
avg()  # # This is called functons call
avg()  # # This is called functons call
avg()  # # This is called functons call



