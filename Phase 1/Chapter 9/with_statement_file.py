f = open("01_file.txt")
print(f.read())
f.close()


## The same can be written using with statement like this:

with open("01_file.txt", "r") as f:
    print(f.read())

## you dont have to close the file like above cause it will automatically do so !!!
# BOTH CODE OUTPUT IS ::

'''
I am Sudeep Nepal.
I am from Bhaktapur.
I live with my parents.
I used to code when I got free from my college.
My favorite food is momo and chowmein.
'''