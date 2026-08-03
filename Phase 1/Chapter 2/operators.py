# ARITHMETIC OPERATORS (plus, minus, multiply, divide, modulus and exponential are arithmetic operators..)

a = 54
b = 56
c = a + b
print(c)
# Here 54 and 56 are operand ( + plus sign is Assignment operators) and Output 110 is Result

# ********************************************************************************************************

# ASSIGNMENT OPERATORS ( = , += , -= are known as Assignment Operators)
num1 = 96
# print(num1) #(here = sign assign the num1 value to 96, so it is  a Assignment operator)
num2 = 61
# num2 += 5 # (Increment the value by 5 in the num2 variable)
num2 -= 5 #(Decrement the value by 5 in the num2 variable)
# print(num2)

# ********************************************************************************************************

# COMPARISION OPERATORS  # It either shows the values in either true or false
isActiveUser = True
# print(isActiveUser)
isOffline = False
# print(isOffline)

# for better knowledge about comparision operators
checknum = 5 > 52
print(checknum)
checknum1 = 5 < 52
# print(checknum1)

checkNumber = 45 >= 45
print(checkNumber)
checkNumber2 = 45 <= 54
# print(checkNumber2)

isTrue =  5 != 7
# print(isTrue) # it returns true cause 5 is not equals to 7)
# here ( ! = is not known as not equals to)

# ********************************************************************************************************

# LOGICAL OPERATORS (BASICALLY AND  ,  OR / NOT aree Logical operators)

# and returns True only when both conditions are true; if either is false, it returns False.
# or returns True when at least one condition is true; it only returns False when both are false.
# not simply reverses the boolean value — it turns True into False and False into True.


age = 25
has_license = True

print(age >= 18 and has_license)                              # True (both conditions true)
print(age < 18 or has_license)                                # True (second condition true)
print(not has_license)                                        # False (reverses True to False)
print(not (age > 30))                                         # True (reverses False to True)
print((age >= 18 and has_license) or not (age < 21))          # True (combination)



