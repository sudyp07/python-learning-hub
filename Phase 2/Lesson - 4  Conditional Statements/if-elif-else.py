# if = Executes a block of code if the specified condition is True.
# else = Executes a block of code if none of the above conditions are True.

age = int(input("Enter your age: "))

if age >= 18:
    print("You are allowed to make a driving licence..")   #PRINT THIS IF CONDITIONS MATCHES
else:
    print("Sorry !!  You are not allowed to make a driving licence because of Age restriction..") # PRINTS THIS IF CONDITIONS FAILED !!


# if = Executes a block of code if the specified condition is True.
# elif = Checks another condition if the previous condition was False.
# else = Executes a block of code if none of the above conditions are True.

userage = int(input("Enter your age: "))

if userage >= 18 and userage <= 99:
    print("You are now signed up...")           # prints this if user enters age greater or equals to 18 or equals or less than 99
elif userage < 0 :
    print("Sorry ! Your age seems negative !")   # prints this if user enters age in negative
elif  userage > 100:
    print("Sorry ! You are too old to Sign Up !")   # prints this if user enters age 100+
else:
    print("You are not authorized !")           # prints this if above both condition failed.


