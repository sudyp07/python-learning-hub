"""
Class = Blueprint
Object = Real item
Attribute = Information
Method = Action
self = Current object
__init__ = Object setup method
"""

class Student:
    def __init__(self, name, age, course):
        self.name = name
        self.age = age
        self.course = course


student_one = Student("Ethan Miller", 19, "Computer Science")

print(student_one.name)
print(student_one.age)
print(student_one.course)

"""
Ethan Miller
19
Computer Science
"""
