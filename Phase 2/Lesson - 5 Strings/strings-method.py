name = input("Enter your full name: ") #Sudip Nepal
phone_number = input("Enter your phone number: ")

print(len(name)) #11 # It will give you the length of the value assigned in input
print(name.find(" ")) #5 cause spaces comes in 5 index
print(name.find("Nepal")) # 6 cause it comes in the index 6 of my full name
print(name.rfind("q"))  # -1 cause it retuns negative if it didn't find any q or alphabets assigned in quoatation marks
print(name.capitalize()) # Sudip nepal
print(name.upper()) # SUDIP NEPAL
print(name.lower())  # sudip nepal
print(name.title()) # Sudip Nepal
print(name.isdigit()) # False cause its alphabets
print(name.isalnum())  # False cause there are no numbers I just asssign my own name here
print(name.isalpha()) # False cause i have given a space between name and surname
print(name.islower())  # check either the given variable is in lower case or not , if yes true either false
print(name.isupper())  # check either the given variable is in upper case or not , if yes true either false
print(phone_number.count("-")) #01-25-585456-41 # 3  --> cause there are 3 hyphens here in this number
print(phone_number.replace("-", " "))  #01 25 585456 41  # --> replace hyphens with the space

# Important : There are more functions regarding string in python to access that:
 # --> print(help(str))