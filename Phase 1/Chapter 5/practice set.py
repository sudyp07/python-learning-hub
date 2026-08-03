#ENGLISH NEPALI TRANSLATON
eng_nep = {
    "Hello" : "namaste",
    "sit" : "basa",
    "eat" : "khau",
    "go" : "jau"
}

word = input("Enter a word: ") # Enter a word: sit
print(eng_nep[word]) # basa

# take input of 8 number from user and display number at once
user_input = set()
numbers = int(input("Enter a number 1: "))
user_input.add(numbers)
numbers = int(input("Enter a number 2: "))
user_input.add(numbers)
numbers = int(input("Enter a number 3: "))
user_input.add(numbers)
numbers = int(input("Enter a number 4: "))
user_input.add(numbers)
numbers = int(input("Enter a number 5: "))
user_input.add(numbers)
numbers = int(input("Enter a number 6: "))
user_input.add(numbers)
numbers = int(input("Enter a number 7: "))
user_input.add(numbers)
numbers = int(input("Enter a number 8: "))
user_input.add(numbers)
print("THE SET IS" , user_input)


# checking while we can set dual value or not
set_check = set()
set_check.add("18")
set_check.add(18)
print(set_check)

# check the length of following set

s = set()
s.add(20)
s.add(20.0)
s.add("20")
result = len(s)
print(result)  # it comes 2 cause in set 20.0 and 20 is same cause comparision operator checks values not data types either its float and integer it returns one value

# checking the type
set1 = {}
print(type(set1)) #ITS DICT


#TAKE USER DATA FROM USER AND ADD IT IN THE EMPTY DICT :)
# IN THE BELOW EXAMPLE IF YOU ENTER SAME VALUE FOR MULTIPLE KEYS ,IT WILL PRINT THE VALUE YOU ENTERED IN THE LAST :) , CAUSE WE RAN UPDATE METHOD IN DICTIONARY..
# IN THE BELOW EXAMPLE IF YOU ENTER SAME KEYS FOR MULTIPLE VALUE ,IT WILL PRINT THE VALUE YOU ENTERED IN THE LAST :) , CAUSE WE RAN UPDATE METHOD IN DICTIONARY..
userin = {}
name = input("Enter your  name: ")
lang = input("Enter your favorite language: ")
userin.update({name: lang})
name = input("Enter your  name: ")
lang = input("Enter your favorite language: ")
userin.update({name: lang})
name = input("Enter your  name: ")
lang = input("Enter your favorite language: ")
userin.update({name: lang})
name = input("Enter your  name: ")
lang = input("Enter your favorite language: ")
userin.update({name: lang})

print(userin)


#CHECK EITHER IF WE CAN CHANGE THE VALUE OF LIST INSIDE THE SET

values = {'harry',"marry","carrie" , [1,2,4,5]}
values[4][2] = 3
# no you cannont cause its immutable and unhasable


















