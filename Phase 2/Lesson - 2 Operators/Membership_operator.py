# it is used to test whether the value or variable is found in a sequence (string, list, tuple,set or dictionary)
# 1. --> in
# 2. --> not in

# strings first

word = 'MICROSOFT'
letter = input("Enter a letter in the secret word: ")

if letter in word:
    print(f'There is a {letter} in the secret word')
else:
    print(f'There is no {letter} in the secret word')

## ALSO YOU CAN WRITE LIKE IT (if you gave not in --> in the if statement you must flip the printing sentence.
if letter not in word:
    print(f'There is no {letter} in the secret word')
else:
    print(f'There is a {letter} in the secret word')


# ## list ,tuple and sets is same as it

students = {'Travis', 'Sandy', 'Pat', "Brook"}

stundets = input("Enter a student name: ")

if stundets in students:
    print(f'There is a  student named : {stundets} in the student name')
else:
    print(f'There is no student named : {stundets} in the student name')


#FOR DICTIONARY

grades = {'SANDY':"A+"
    , "PATRICK": "A"
    ,"SPONGEGBOB": "B"
    , "TRAVIS" : "C"}


student_info = input("Enter student name: ")

if student_info in grades:
    print(f"{student_info}'s grade is {grades[student_info]}")
else:
    print(f"{student_info}'s info was not found")



# Email validator example

email = "Sudyphero@fakemail.com"

if "@" in email and "." in email:
    print(f"{email} is a valid email address")
else:
    print(f"{email} is not a valid email address")



