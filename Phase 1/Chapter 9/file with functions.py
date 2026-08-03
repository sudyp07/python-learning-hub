f = open('01_file.txt', 'r')  ## taking file from same dir where this python file is located in reading mode.
lines = f.readlines()# reading each and every line by line
print(lines) ##prining each lines
print(type(lines)) ##printing the type of lines, it will return in list
f.close() #important :IMPORTANT :always close the file after the work is done, its a good practice altough it will not give error in absence as well.

##OUTPUT:

# ['I am Sudeep Nepal.\n', 'I am from Bhaktapur.\n', 'I live with my parents.\n',
# 'I used to code when I got free from my college.\n', 'My favorite food is momo and chowmein.']
# <class 'list'>

# printing the text line by line using proper readline module....

f = open('01_file.txt', 'r')

line1 = f.readline()
print(line1 ,type(line1))

line2 = f.readline()
print(line2 ,type(line2))

line3 = f.readline()
print(line3 ,type(line3))

line4 = f.readline()
print(line4 ,type(line4))

line5 = f.readline()
print(line5 ,type(line5))

line6 = f.readline()
print( line6,type(line6))

"""
I am Sudeep Nepal.
 <class 'str'>
I am from Bhaktapur.
 <class 'str'>
I live with my parents.
 <class 'str'>
I used to code when I got free from my college.
 <class 'str'>
My favorite food is momo and chowmein. <class 'str'>
 <class 'str'>
"""

 #### you can do this simply by running while loop
f = open('01_file.txt', 'r')  ## taking file from same dir where this python file is located in reading mode.
line = f.readline()  ## reading each and every line by line
while(line != ""): ## while line is not equals to empty strings till the end.
    print(line) ## keep printing line till its not finished printing
    line = f.readline()  ## it will prevent while loop from running continiously

f.close()  ##IMPORTANT :always close the file after the work is done, its a good practice altough it will not give error in absence as well.

### it still prints like this :
"""
I am Sudeep Nepal.

I am from Bhaktapur.

I live with my parents.

I used to code when I got free from my college.

My favorite food is momo and chowmein.
"""