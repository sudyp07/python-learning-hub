class Student:
    def __init__(self, name, age, course):
        self.name = name
        self.age = age
        self.course = course

    def introduce(self):
        print(f"Hello, my name is {self.name}.")
        print(f"I am {self.age} years old.")
        print(f"I am studying {self.course}.")


student_one = Student("Ethan Miller", 19, "Computer Science")
student_two = Student("Olivia Johnson", 21, "Cybersecurity")

student_one.introduce()

print()

student_two.introduce()

"""
Hello, my name is Ethan Miller.
I am 19 years old.
I am studying Computer Science.

Hello, my name is Olivia Johnson.
I am 21 years old.
I am studying Cybersecurity.

"""