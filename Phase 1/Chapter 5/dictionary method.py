# DICTIONARY METHODS
# It always changes the ORIGINAL dictionary (mutable).
# Most dictionary methods modify the same dictionary instead of creating a new one.

marks = {
    "user1": 34,
    "user2": 45,
    "user3": 55,
    "user4": 65
}

marks.clear()                        # Removes all key-value pairs                               {}
marks.copy()                         # Creates and returns a shallow copy                        {'user1': 34, 'user2': 45, 'user3': 55, 'user4': 65}
dict.fromkeys(["A","B"], 100)# Creates a new dictionary with given keys              {'A': 100, 'B': 100}
marks.get("user2")                   # Returns the value of 'user2'                              45
marks.get("user5")                   # Returns None if key doesn't exist                         None
marks.get("user5", 0)     # Returns default value if key doesn't exist                0
marks.items()                        # Returns all key-value pairs                               dict_items([('user1',34),('user2',45),('user3',55),('user4',65)])
marks.keys()                         # Returns all keys                                          dict_keys(['user1','user2','user3','user4'])
marks.pop("user2")                   # Removes 'user2' and returns its value                     45             # Dictionary becomes:    # {'user1':34,'user3':55,'user4':65}
marks.popitem()                      # Removes and returns the last inserted item                ('user4', 65)  # Dictionary becomes: # {'user1':34,'user2':45,'user3':55}
marks.setdefault("user5", 80)        # Adds key if it doesn't exist                              {'user1':34,'user2':45,'user3':55,'user4':65,'user5':80}
marks.setdefault("user1", 100)       # Does nothing because key exists                           Returns 34
marks.update({"user2":99})           # Updates existing key                                      {'user1':34,'user2':99,'user3':55,'user4':65}
marks.update({"user5":88})           # Adds new key if it doesn't exist                          {'user1':34,'user2':45,'user3':55,'user4':65,'user5':88}
marks.values()                       # Returns all values                                        dict_values([34,45,55,65])

print(marks.items())