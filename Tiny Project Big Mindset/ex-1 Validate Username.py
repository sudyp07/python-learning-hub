# Taking the user input from user and checking the username is valid or not
## must not have space , numbers in name and must not more than 12 chars in username

username = input("Enter Your Username: ")


if (len(username)) > 12:
    print("Invalid Username Because it can't be more than 12 characters.")
elif not username.find(" ") == -1 : # if there is space it got true then it runs
    print("Invalid Username Because it contains a space.")
elif not  username.isalpha(): # if there is more than alphabets it runs too.
    print("Invalid Username Because it contains unauthorized characters.")
else:
    print("Login Successful...")