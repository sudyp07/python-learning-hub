#good afternoon user program
user_input = input("Please enter your name: ")
print("GOOD AFTERNOON " +  user_input.upper() )

# fill tempelate program
letter = """
        Dear <|name|>
        You are seleted for upcoming episode.
        <|date|>
        """

letter_new = letter.replace("<|name|>" , "Sudeephero").replace("<|date|>" , "25 February 2030")
print(letter_new)

#DETECT DOUBLE SPACE IN STRINGS:
sentence = "my full name is Sudeep  Nepal"
print(sentence.find("  "))

#REPLACE DOUBLE SPACE INTO SINGLE SPACE
sentence1 = "my full name is Harish  Kumar"
print(sentence1.replace("  ", " "))


#format letter using escape sequence
sentence2 = "DEAR HARRY,\n THIS PYTHON COURSE IS NICE, \t \"THANKS.\""
print(sentence2)




