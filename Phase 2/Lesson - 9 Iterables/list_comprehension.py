"""
list comprehension is a concise way to create list in python and its compact and easier to read than tradition loops
[expression for value in iterable if condition]
"""

# first --> traditional looops

doubles = []
for x in range(1 , 11):
    doubles.append(x * 2)

print(doubles) # output is --> [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

## now using list comprehension

multiples = [x * 2 for x in range(1, 11)]
triples = [x * 3 for x in range(1, 11)]
squares = [x**2 for x in range(1, 11)]

print(multiples) # output is --> [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
print(triples)  # output is --> [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
print(squares)  ## output is --> [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]


# now working with the list of fruits

fruits = ["apple", "banana", "cherry", "grapes"]
fruits = [fruit.upper() for fruit in fruits]
fruit_chars = [fruit[0] for fruit in fruits]
print(fruits) # output is --> ['APPLE', 'BANANA', 'CHERRY', 'GRAPES']
print(fruit_chars)  # output is --> ['A', 'B', 'C', 'G']


# now working with the list of numbers

numbers = [1, -2, 3, 4, -5, 6, 7, -8, 9, 10]

positive_numbers = [num for num in numbers if num >= 0]
negative_numbers = [num for num in numbers if num < 0]
even_numbers = [num for num in numbers if num % 2 == 0]
odd_numbers = [num for num in numbers if num % 2 != 0]

print(positive_numbers) # --> positive numbers --> [1, 3, 4, 6, 7, 9, 10]
print(negative_numbers) # --> negative numbers --> [-2, -5, -8]
print(even_numbers)  # --> even numbers [-2, 4, 6, -8, 10]
print(odd_numbers)  # --> odd numbers  [1, 3, -5, 7, 9]


# list of grades

grades = [85, 43, 70, 90, 56, 61, 30]

passing_grades = [grade for grade in grades if grade >= 60]
failed_grades = [grade for grade in grades if grade <= 60]

print(passing_grades) # [85, 70, 90, 61]
print(failed_grades) # [43, 56, 30]







