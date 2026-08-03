# check largest number out of 4

num1 = int(input("Enter a number 1: "))
num2 = int(input("Enter a number 2: "))
num3 = int(input("Enter a number 3: "))
num4 = int(input("Enter a number 4: "))
#
if (num1 > num2 and num1 > num3 and num1 > num4):
    print("Num 1 is greater than all")
elif (num2 > num1 and num2 > num3 and num2 > num4):
    print("Num 2 is greater than all")
elif (num3 > num1 and num3 > num4 and num3 > num4):
    print("Num 3 is greater than all")
else:
    print("Num 4 is greater than all")

# check student wether s\he is passed or failed

marks1 = int(input("Enter your marks1 :"))
marks2 = int(input("Enter your marks2 :"))
marks3 = int(input("Enter your marks3 :"))

#check for total percentage (marks out of 100)
total_percentage = (100 *(marks1 + marks2 + marks3 )) / 300
print(f"Your total percentage is:  {total_percentage:.1f}")

if(total_percentage >= 40 and marks1 >= 33 and marks2 >= 33 and marks3 >= 33):
    print("You passed the examinations")
else:
    print("You failed the examinations")


# checking spammm comment and filter that out

spam1 = "Buy now"
spam2 = "Limited time offer"
spam3 = "Congratulations! You won"
spam4 = "Claim your prize"
spam5 = "Free gift"
message = input("Enter your comment: ")

if ((spam1 in message) or (spam2 in message) or (spam3 in message) or (spam4 in message) or (spam5 in message)):
    print("Spam comment Detected !!!")
else:
    print("Fair comment Detected !!!")


# checking username char length

username = input("Enter your name: ")
if  (len(username )>= 10):
    print("Welcome " + username )
else:
    print("Username Invalid " + username )

# check name are presented in the list or not

names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Isabella", "Jack"]
name = input("Enter your name: ")
if (name in names):
    print("Welcome " + name)
else:
    print("Sorry " + name)


# calculate grades based on the marks

student_marks = int(input("Enter your score to check your grade: "))

if (student_marks >= 90):
    print("Your Grade is A++")
elif(student_marks >= 80 and student_marks < 90):
    print("Your Grade is B+")
elif(student_marks >= 70 and student_marks < 80):
    print("Your Grade is C+")
elif(student_marks >= 60 and student_marks < 70):
    print("Your Grade is D+")
elif(student_marks >= 50 and student_marks < 60):
    print("Your Grade is E")
else:
    print(student_marks)
    print("Your Grade is F, which is equivalent to Failing the Examination")


#check the word is in or not:

passage = '''
Summer is my favorite season because the days are warm and sunny. During the summer holidays, my friends and I enjoy playing cricket, swimming, and eating ice cream. Families often travel to beautiful places, while children spend more time outdoors. The bright sunshine, clear Blue skies, and colorful flowers make summer a joyful and relaxing time of the year.'''

user_in = input("message to check the word:")

if (user_in in passage.lower()):
    print(user_in + " is located Inside the Passage")
else:
    print(user_in + " is not in the Passage")




