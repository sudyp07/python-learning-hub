#SETS
# Sets are unordered, so the output order may be different each time.
# Set methods usually modify the ORIGINAL set because sets are mutable.
#you can store any data like string integer boolean and float

#mistakes while making an empty set :
sudeep = {}
print(type(sudeep)) # <class 'dict'> dont use sett = {} casue its empty dict not set ....

sett = set() #This is used to make a empty set , dont use sett = {} casue its empty dict ....
print(type(sett)) # <class 'set'>

#one legal set
it_companies = {"google", "yahoo", "apple", "yahoo", "google"}
print(it_companies) # {'google', 'yahoo', 'apple'} , its because set doesnt allowed duplicate values.
print(type(it_companies)) #<class 'set'>


