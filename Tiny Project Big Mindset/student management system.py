## student management portal

print("*****************************************")
print("Welcome to the student management system")
print("*****************************************")
print (
    '''
1. Add Student
2. View Students
3. Search Student
4. Delete Student
5. Update Student Marks
6. Exit '''
)
serial_number = int(input("Enter a serial number: "))
student = []

## student adding
if serial_number == 1:
    user_input = input("Enter a name of a student: ").lower()
    student.append(user_input)

