def happy_birthday():
    print('Happy Birthday')

happy_birthday() # Happy Birthday

## wishing married life
def happy_marriage(bride , groom):  ## parameters
    print('Happy marriage')
    print('God bless you both !')
    print(f"Happy Married Life {bride} and {groom}. ")

happy_marriage("Alex"  , "Nira") ## passing arguments to parameters

"""
Happy marriage
God bless you both !
Happy Married Life Alex and Nira. 
"""

## basic but important (position of arguments matters here
def greet (name , age):
    print(f"Hello {name}, You are {age} years old.")

greet("Nira", 74)   # Hello Nira, You are 74 years old.
greet("Alex", 36)   # Hello Alex, You are 36 years old.
greet("Mira" ,25)   # Hello Mira, You are 25 years old.


## display invoice
def invoice(username, amount, due_date):
    print(f"Hello {username}")
    print(f"You have {amount} dollars left.")
    print(f"You have {due_date} dollars left.")

invoice("Jake Lee", 50, "2027/01/25")
invoice("SpiderMan", 50, "2020/01/24")

"""
Hello Jake Lee
You have 50 dollars left.
You have 2027/01/25 dollars left.
Hello SpiderMan
You have 50 dollars left.
You have 2020/01/24 dollars left.
"""

## return statement used ot end a function and send a result back to the caller

def add(x, y):
    z = x + y
    return z
def subtract(x, y):
    z = x - y
    return z
def multiply(x, y):
    z = x * y
    return z
def divide(x, y):
    z = x / y
    return z

print(add( 65,76))
print(subtract(65,76))
print(multiply(65,76))
print(divide(65,76))

"""
141
-11
4940
0.8552631578947368
"""


## create a full name
def create_fullname(first, last):
    first  = first.capitalize()
    last = last.capitalize()
    return first + " " + last

fullname = create_fullname("sudeep", "nepal")
print(fullname)  # Sudeep Nepal






