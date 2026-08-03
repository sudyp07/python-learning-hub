age = int(input("Enter your age: "))


if age  == 18:
    print("You do have right age to vote")


if (age >= 18):
    print("You are old enough to vote")
elif (age == 0):
    print("You are entering an invalid age")
elif (age < 0):
    print("You are not born yet")
else:
    print("You are not  eligibe to vote yet")

# pass method in conditional expression :)

name =  "Sudeep"
if name == "Sudeep":
    pass   # (if we dont want to show and run it,we can simply bypass it using pass)
else:
    "We cant show you the user detail because of the policy.."