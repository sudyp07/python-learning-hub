#take 7 fruits from user and store in the list..-->
fruits = []

fruits_user = input('Enter a fruit name: ')
fruits.append(fruits_user)
fruits_user1 = input('Enter a fruit name: ')
fruits.append(fruits_user1)
fruits_user2 = input('Enter a fruit name: ')
fruits.append(fruits_user2)
fruits_user3 = input('Enter a fruit name: ')
fruits.append(fruits_user3)
fruits_user4 = input('Enter a fruit name: ')
fruits.append(fruits_user4)
fruits_user5 = input('Enter a fruit name: ')
fruits.append(fruits_user5)
fruits_user6 = input('Enter a fruit name: ')
fruits.append(fruits_user6)
print(fruits)


#marks of the students in sorted form by taking input from user :
marks = []

student1 = int(input("Enter your marks here: "))
marks.append(student1)
student2 = int(input("Enter your marks here: "))
marks.append(student2)
student3 = int(input("Enter your marks here: "))
marks.append(student3)
student4 = int(input("Enter your marks here: "))
marks.append(student4)
student5 = int(input("Enter your marks here: "))
marks.append(student5)
student6 = int(input("Enter your marks here: "))
marks.append(student6)
student7 = int(input("Enter your marks here: "))
marks.append(student7)
marks.sort()
print(marks)


#check the type that cannot be changed in python
tuple_1 = (43,32,43,235,6,345)
tuple_1[2] = 32
print(tuple_1) # so it doesn't allow any new assignment becasue it is a immutable

#take 4 input and sum them all
tuple_sum = (55, 59, 35, 45)
print(sum(tuple_sum))

#counts how many times there are zero in a tuple:
tuple_zero = (0,1,0,5,4,5,4,5,5,1,0,44,0,4,4440,42,41,4,0,4,21,1,0,4,4,2,0,0,0,0)
tuple_count = tuple_zero.count(0)
print(tuple_count)