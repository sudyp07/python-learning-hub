name = "Sudeep" # This is a single quoted simple string
surname = 'Nepal'# This is a double quoted  simple string
full_name = """My name is Sudeep Nepal"""# This is also Triple quoted simple string
print(len(name)) #6  #It is because there are 6 letters in my name,as it gives the length of the value of my name !!

# In programming index counts will always starts from zero (0) for example when: (positive & negative indexing)
# district = "Humla"
# here, H-0 , u-1 , m-2 , l-3 , a-4 --> Length =5 (It counts  from 0)   --> This is positive indexing !!
#like-> -5  , -4  , -3  , -2 , - 1  (It counts  from -1)  --> This is  negative indexing !!
#Also space is counted as string inside quoted text !

# TypeError: 'str' object does not support item assignment
# var="HELLO PYTHON"
# var[7]="y" #You cannot change the value of strings like this , it gives error.

# Extract the value by using  negative indexing
var1 = "HELLO PYTHON"
print(var1[-1])   # N
print(var1[-5])   # Y
print(var1[-12])  # H

#Python defines ":" as string slicing operator.
#It prints from index 3 till 8 but (excluding 8) , if you want to print till exact 8 you have enter 9 to get value of index 8.

var2="HELLO PYTHON"
print ("var2:",var2)                   #var: HELLO PYTHON
print ("var2[3:8]:", var2[3:8])        #var[3:8]: LO PY

#MASTERING NEGATIVE SLICING --> (Usually not needed in python , instead it can be asked in the interview)
mom = "Devi"
print(mom[-3 : -1]) #->ev
print(mom[1 : 3])   #->ev #changed to correspondance positive indices

#Know about the length and advanced slicing method
my_name = "Sudip"
print(my_name[:4])  #Sudi #This is same as  (my_name[0:4])
print(my_name[1:])  #udip #This is same as  (my_name[1:5])  --> It counts length of the value after colon : and prints all
print(my_name[1:5]) #udip (same as above)


#Slicing with the skip value
word = 'amazing'
print(word[1:6:2]) #mzn
# lets learn this properly now
# It gives (mzn) as result cause :

# start = 1 → Start at index 1 ('m').
# stop = 6 → Stop before index 6. So index 6 ('g') is not included.
# step = 2 → Move 2 positions each time.

word2 = "Expenditure"
print(word2[1:5:2]) #xe
# lets learn this properly now
# It gives (xe) as result cause :

# start = 1 → Start at index 1 ('x').                                ✅ start is included.
# stop = 5 → Stop before index 5. So index 5 ('d') is not included.  ❌ stop is excluded.
# step = 2 → Move 2 positions each time.                             ➡️ step tells Python how many positions to move (jump) each time.











