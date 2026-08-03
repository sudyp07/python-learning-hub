# Sample of Dictionary in and accessing the data in --> python
MY_NAME = {} #THIS IS BLANK DICT !!

my_dict = {
    "name": "Sudeep Nepal",
    "gender" : "Male",
    "age" : 25,
    "country" : "United States"
}

print(my_dict)          #  {'name': 'Sudeep Nepal', 'gender': 'Male', 'age': 25, 'country': 'United States'}
print(my_dict["name"])  # Sudeep Nepal
print(my_dict["age"])    # 25
print(my_dict["gender"])  # Male
print(type(my_dict))    #  <class 'dict'>

##***************************************************************##
                # IMPORTANT POINTS TO REMEMBER
# ================================================================

# ✔ Dictionaries are unordered before Python 3.7, after that its ordered
# ✔ Dictionaries are mutable (can be modified after creation).
# ✔ Dictionaries store data as key-value pairs.
# ✔ Dictionary keys must be unique (no duplicate keys allowed)...
# ✔ Dictionary values can be duplicated.
# ✔ Keys must be immutable types (e.g., str, int, float, tuple).
# ✔ Values can be of any data type.
# ✔ Dictionaries are created using curly braces {} or dict().
# ✔ Dictionaries are optimized for fast lookup using keys.
# ✔ Dictionaries can contain nested dictionaries and other collections.
# ✔ Dictionaries do NOT support indexing by position.
# ✔ Access dictionary items using their keys.
