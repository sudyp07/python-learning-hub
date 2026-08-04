def hello(greeting, title, first, last):
    print(f" {greeting} {title} {first} {last}.")

# here order doesnt matter you can add value before or after if you declare it properly like this :
hello(greeting="Hey",last="Voll", first="Georgia" , title= "Ms")

# passed the arguments normally without mentioning the title or name or greetings..
hello("Hello", "Mr" , "Travis", 'Head')
hello("Hello", "Mr" , "Pat", 'Cummins')
hello("Hello", "Mr" , "Nathan", 'Lyon')
hello("Hello", "Mr" , "Mitch", 'Starc')

"""
 Hey Ms Georgia Voll.
 Hello Mr Travis Head.
 Hello Mr Pat Cummins.
 Hello Mr Nathan Lyon.
 Hello Mr Mitch Starc.
 """

for x in range(1 , 13):
    print(x, end = " ")  # this end keyword is also a keyword arguments
# 1 2 3 4 5 6 7 8 9 10 11 12
print()

def get_phone(country, area, first, last):
    return f"{country}-{area}-{first}-{last}"
phone_number = get_phone(country= 977, area="9841" , first="234", last="5678"  )
print(phone_number)  # 977-9841-234-5678