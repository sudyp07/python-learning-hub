# Logical Expressions in Python

# not --> Reverses the Boolean value
is_raining = True

if not is_raining:
    print("It's not raining!!")
else:
    print("It's raining!!")   # Output: It's raining!!

# and --> Returns True only if both conditions are True
is_user = True
is_admin = True

if is_user and is_admin:
    print("It's admin!!")     # Output: It's admin!!
else:
    print("It's not admin!!")

# or --> Returns True if at least one condition is True.
# It returns False only when both conditions are False.
is_male = True
is_female = False

if is_male or is_female:
    print("Person exists.")   # Output: Person exists.
else:
    print("No person found.")