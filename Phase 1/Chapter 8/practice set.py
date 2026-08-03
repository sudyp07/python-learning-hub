##checking greater number from 3 number
def high():
    num1 = int(input("Enter a number: "))
    num2 = int(input("Enter another number: "))
    num3 = int(input("Enter another number: "))

    if num1 > num2 and num1 > num3:
        print(f'The Highest number from three input is',num1)
    elif(num2 > num1 and num2 > num3):
        print(f'The Highest number from three input is',num2)
    else:
        print(f'The Highest number from three input is', num3)

high()

## celsius to farenheit
def f_to_c(f):
    return 5 * (f - 32) / 9

f = int(input("Enter a temperature in Fahrenheit: "))
print(f"The conversion of {f}°Fahrenheit to Celsius is : {(f_to_c(f)):.2f}°C")


## prevent py to print new line at the end (use end = "")
a = 34
b = 53
c = 65
d = 63

print(a)
print(b)
print(c, end = "") #these both lines print in a single line
print(d, end = "") #these both lines print in a single line


# # learning recursion properly
'''
sum(1) = 1
sum(2) = 1+2 =3
sum(3) = 1+2+3 = 6

sum(n) = 1+2+3+4+5.....n
sum(n) = sum(n-1) + n
'''

def sum(n):
    if (n == 1):  ## this  is the base condition , it stops here from running inifine like -1,-2-3
        return 1
    return sum(n - 1) + n

print(sum(4))

## star printing pattern
#
def pattern (n):
    if (n == 0):
        return
    print("*" * n)
    pattern(n-1)


n = int(input("Enter a number: "))
pattern(n)


## inches to centimeters
def inch_to_cm(inch):
    return inch * 2.54

n = int(input("Enter a number: "))
print(f'The corresponding values of {n} in cms is {inch_to_cm(n)}')



# remove a word from list and strip
def remove(list , word):
    n = []
    for item in list:
        if not(item == word):
            n.append(item.strip(word))
    return n

list = ["Haierr", "Subham", "Pieterr", "Munierr", "rr"]

print(remove(list , "rr"))  # #['Haie', 'Subham', 'Piete', 'Munie']


##write a python to print a multiplication table of a number

def multiply(n):
    for i in range(1,11):
        print(f'{n} x {i} = {i*n}')

multiply(3)

"""
3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
3 x 4 = 12
3 x 5 = 15
3 x 6 = 18
3 x 7 = 21
3 x 8 = 24
3 x 9 = 27
3 x 10 = 30
"""
