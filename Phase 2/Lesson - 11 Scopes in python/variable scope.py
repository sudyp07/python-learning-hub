# variable scope = where a variable is visible and accessible
# scope resolution = LEGB  local   --> enclosed    -->gobal    -->built it

# Example 1: Local Scope  [name exists only inside greet()]
def greet():
    name = "Sudip"
    print(name)

greet()  # Sudip


#Step 2: Global Scope -->  Variables outside every function are global variables.
name = "Sudip"

def greet():
    print(name)

greet()  # Sudip


#Step 3: Enclosed Scope  --> This happens with nested functions.
def outer():
    x = 10

    def inner():
        print(x)

    inner()

outer() # 10

# Step 4: Built-in Scope  --> Python already has many names.

print()
len()
sum()
max()
min()
type()

numbers = [10,20,30]

print(len(numbers))  # 3




















