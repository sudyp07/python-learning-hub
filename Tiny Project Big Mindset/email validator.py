## Email validator program
email = input("Enter your email address: ")

if (
    email[0].isalpha()
    and email.count("@") == 1
    and email.endswith(".com")
    and " " not in email
):
    print("Email address valid")
else:
    print("Email address invalid")
