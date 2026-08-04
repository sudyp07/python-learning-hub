"""
*args = allows you to pass multiple non keyword arguments
**kwargs = allows you to pass multiple keyword-arguments
  * = unpacking operators
 it is also known as arbitary arguments
"""

# args  --> also known as arguments

def add(*args):
    total = 0
    for arg in args:
        total += arg
    return total

print(add(34,76, 64))  #174
print(add(234,746, 644,6))  #1630

# next example

def display_name (*args):  # YOU CAN RENAME ARGS LIKE (*names)
    for arg in args:       # you can do  like this : for name in names
        print(arg , end = " ")  # print(name , end = " ")

# LIKE THIS YOU CAN PASS MULTIPLE ARGUMENTS HERE IN THE ARGS

display_name("Spongebob" ,"mitchell", "Squarepants\n" )
display_name("Dr." "Spongebob" ,"mitchell", "Squarepants\n")
display_name("Dr." "Spongebob" ,"mitchell", "Squarepants" "II\n")

"""
Spongebob mitchell Squarepants
Dr.Spongebob mitchell Squarepants
Dr.Spongebob mitchell SquarepantsII
"""

"""*******"""
"""KWARGS"""
"""*******"""
# basically kwargs also known as the dict of the python like format

def print_address (**kwargs):
    for key , value in kwargs.items(): # you can just get value or keys from here, like for key in kwargs.keys():
        print( f'{key} : {value}')   # print(key)

print_address(street = "534 Fake Street",
              city = "Detroit" ,
              state = "Michigan",
              zip_code = "94107")

"""
street : 534 Fake Street
city : Detroit
state : Michigan
zip_code : 94107
"""


## excercise kwargs and args in a single excercise

def shipping_label(*args,**kwargs):
    for arg in args:
        print(arg , end = " ")
    print()
    print(f"{kwargs.get("street")} {kwargs.get("apt")}")
    print(f"{kwargs.get("city")} {kwargs.get("state")} {kwargs.get("zip_code")} {kwargs.get("PB-no.")}")


shipping_label('Dr.', "Sudip" ,'Nepal' , "Jr",
               apt = "232 random apt",
               street = "534 Fake Street",
               city = "Detroit",
               state = "Michigan",
               zip_code = "94107")


"""
Dr. Sudip Nepal Jr 
534 Fake Street 232 random apt
Detroit Michigan 94107 None
"""


"""here we get None at last in PB-no.
 becasue there is no such data with it above
 but if you want to check it and dont want to return None you can use if-else staement like this:
 if "PB-no." in kwargs:
    print(f"{kwargs.get("city")} {kwargs.get("state")} {kwargs.get("zip_code")} {kwargs.get("PB-no.")}")
else:
print(f"{kwargs.get("city")} {kwargs.get("state")} {kwargs.get("zip_code")}")
 """






