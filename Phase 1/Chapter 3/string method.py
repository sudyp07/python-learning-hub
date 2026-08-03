name = 'sudip nepal'

print(name)                          # sudip nepal (PRINTS THE STRING EXACTLY AS IT IS)
print(name.upper())                  # SUDIP NEPAL (CONVERTS ALL LETTERS TO UPPERCASE)
print(name.lower())                  # sudip nepal (CONVERTS ALL LETTERS TO LOWERCASE)
print(name.capitalize())             # Sudip nepal (CAPITALIZES ONLY THE FIRST LETTER OF THE ENTIRE STRING)
print(name.title())                  # Sudip Nepal (CAPITALIZES THE FIRST LETTER OF EVERY WORD)
print(name.strip())                  # sudip nepal (REMOVES SPACES FROM BOTH THE BEGINNING AND THE END OF THE STRING)
print(name.split())                  # ['sudip', 'nepal'] (SPLITS THE STRING INTO A LIST USING SPACES)
print("-".join(name.split()))        # sudip-nepal (JOINS THE LIST ELEMENTS INTO A SINGLE STRING USING '-' AS A SEPARATOR)
print(name.replace("nepal", "sharma"))# sudip sharma (REPLACES THE SPECIFIED WORD OR CHARACTER WITH A NEW ONE)
print(name.find("nepal"))            # 6 (RETURNS THE INDEX OF THE FIRST OCCURRENCE OF THE GIVEN WORD, OR -1 IF NOT FOUND)
print(name.count("a"))               # 1 (COUNTS HOW MANY TIMES THE GIVEN CHARACTER OR WORD APPEARS)
print(name.startswith("sudip"))      # True (CHECKS WHETHER THE STRING STARTS WITH THE GIVEN WORD)
print(name.endswith("nepal"))        # True (CHECKS WHETHER THE STRING ENDS WITH THE GIVEN WORD)
print(name.isalpha())                # False (CHECKS WHETHER THE STRING CONTAINS ONLY LETTERS)
print(name.isdigit())                # False (CHECKS WHETHER THE STRING CONTAINS ONLY DIGITS)
print(name.isalnum())                # False (CHECKS WHETHER THE STRING CONTAINS ONLY LETTERS AND DIGITS)
print(name.islower())                # True (CHECKS WHETHER ALL LETTERS IN THE STRING ARE LOWERCASE)
print(name.isupper())                # False (CHECKS WHETHER ALL LETTERS IN THE STRING ARE UPPERCASE)
print(len(name))                     # 11 (RETURNS THE TOTAL NUMBER OF CHARACTERS IN THE STRING, INCLUDING SPACES)


# ================================================================
# IMPORTANT POINTS TO REMEMBER
# ================================================================

# ✔ Strings are ordered.
# ✔ Strings are immutable (cannot be modified after creation).
# ✔ Strings are sequences of Unicode characters.
# ✔ Strings allow duplicate characters.
# ✔ Strings support indexing and slicing.
# ✔ Strings can be created using single (' '), double (" "), or triple (''' ''' / """ """) quotes.
# ✔ Every string method returns a NEW string because strings are immutable.
# ✔ String methods do NOT change the original string unless reassigned.
# ✔ Strings support many operators (+, *, in, not in, ==, etc.).
# ✔ Strings are one of the most commonly used data types in Python.


# ✔ Strings also work with many built-in functions:

#       - len()
#       - max()
#       - min()
#       - sorted()
#       - reversed()
#       - ord()
#       - chr()
#       - ascii()
#       - hash()
#       - enumerate()
#       - any()
#       - all()