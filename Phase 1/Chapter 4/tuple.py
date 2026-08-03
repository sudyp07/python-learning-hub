#tuple are nearly same as list but tuple are immutable that means you cannot change the values inside the it (same as strings)
tuple_format = ()   #this is a empty tuple format

#important tips for tuple
tuple1 = (1)
print(type(tuple1)) #this is int, not

#if you want to make a legit tuple write a number and give a comma after that like this:
tuple2 = (1,)
print(type(tuple2)) #Now, this is tuple

profession = ("teacher", "farmer", "programmer", "doctor", "Physiotherapist")
print(profession)


# ================================================================
# IMPORTANT POINTS TO REMEMBER
# ================================================================

# ✔ Tuples are ordered.
# ✔ Tuples are immutable (cannot be modified).
# ✔ Tuples allow duplicate values.
# ✔ Tuples can store multiple data types.
# ✔ Tuples are generally faster than lists.
# ✔ A comma (,) creates a tuple—not the parentheses.
# ✔ Tuples have only TWO methods:
#       1. count()
#       2. index()