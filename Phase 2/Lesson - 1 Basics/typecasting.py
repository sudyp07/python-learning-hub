# Type casting (also called type conversion) means changing the data type of a value or variable into another data type.


# example -->

name = "Sudeep"
age = 23
gpa = 3.8
is_student = True

gpa = int(gpa)
print(gpa)  # 3

age = float(age)
print(age) # 23.0

age = str(age)
print(age , type(age))  # 23.0 # <class 'str'>

name = bool(name)
print(name)  # True