f = open("05_poem.txt", "r")
content = f.read()
if "Twinkle" in content:
    print("Twinkle is presented in the poem.")
else:
    print("Twinkle is not presented in the poem.")

f.close()

### Twinkle is presented in the poem.

