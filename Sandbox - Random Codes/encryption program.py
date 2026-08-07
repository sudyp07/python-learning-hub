import random
import string

chars = " " + string.ascii_letters + string.digits + string.punctuation
chars = list(chars)
key = chars.copy()
random.shuffle(key)


# lets do encryption

plain_text = input("Please enter a text to encrypt: ")
cipher_text = ""

for letter in plain_text:
    index = chars.index(letter)
    cipher_text += key[index]

print(f'Original text: {plain_text}')
print(f'Cipher text: {cipher_text}')

# lets do decryption

cipher_text = input("Please enter a text to encrypt: ")
plain_text = ""

for letter in cipher_text:
    index = key.index(letter)
    plain_text += chars[index]

print(f'Encrypted text: {cipher_text}')
print(f'Original text: {plain_text}')

# output
'''
Please enter a text to encrypt: I love you
Original text: I love you
Cipher text: 'PvakYP8a,
Please enter a text to encrypt:  'PvakYP8a,
Encrypted text:  'PvakYP8a,
Original text: I love you
'''