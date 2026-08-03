#print the mulitplication table of a given number using for loop
user_input = int(input("Enter a number: "))

for i in range(1,11):
    print(f"{user_input} * {i} = {user_input*i}")
    i += 1

#greet person stored in name list
l = ['harry','carrie','sachin', 'rahul',"sarbada", 'sudeep']

for i in l:
        if (i.startswith('s'.lower())):
            print(f"Namaste {i.capitalize()}")

#print the mulitplication table of a given number using for loop
i = 0
num2 = int(input("Enter a number: "))

while (i < 11):
    print(f"{num2} * {i} = {i*num2}")
    i += 1


# check whether the number is prime or not
number = int(input("Enter a number: "))

if number < 2:
    print("Number is not prime")
else:
    for i in range(2, number):
        if number % i == 0:
            print("Number is not prime")
            break
    else:
        print("Number is prime")


# while loop to sum number

num = int(input("Enter a number: "))
i = 1
sum = 0

while(i <= num):
    sum = sum + i
    i = i + 1
print(sum)


# # write the factorial of 5
# # 5! = 1*2*3*4*5

Number = int(input("Enter a number: "))
product = 1

for i in range (1 , Number+1):
    product  = product * i
print(f"The factorial of {Number} is: {product}.")


## make star tree using loop
n = int(input("Enter height: "))

for i in range(1, n + 1):
    spaces = " " * (n - i)
    stars = "*" * (2 * i - 1)
    print(spaces + stars)

# multiplications table of any number in reversed way
num = int(input("Enter a number: "))

for i in range(1, 11):
    print(f"{num} x { 11 - i} = {num*(11 -i)}") # it will print any table in proper format in reversed way













