# Input functionality alawys take input as a string., for example if we sum any two numbers normally like below it will concatinate like below
fake1 = input("Enter a fake1 number: ") #1  --> these are input examples
fake2 = input("Enter a fake2 number: ") #2    --> these are input examples

print("The sum of fake1 and fake2 is: ", fake1 + fake2) # it will resulting 12 instead of 3 cause it concatinate between 2 number cause its a string.


# If you want to change the datatypes you must do type conversion like below:::

num1 = int(input("Enter a first number: "))  #44     --> these are input examples
num2 = int(input("Enter a second number: "))  # 56    --> these are input examples

print("num1 is : ", num1)
print("num2 is : ", num2)
print("The sum of num1 and num2 is: ", num1 + num2)  #It will result 100 :) cause we change its datatypes from string to integer :)