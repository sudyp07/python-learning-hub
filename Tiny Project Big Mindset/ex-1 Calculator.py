## 1 hour correct
## calculator making using if else

operator = input("Please enter your operator(+,-,*,/,%,**): ")
first_number = float(input("Please enter your first number: "))
second_number = float(input("Please enter your second number: "))

## error handling

if operator not in ["+", "-", "*", "/", "%", "**"]:
    raise SystemExit("Sorry! Please enter a valid operator.")


## logic writing

if operator == "+":
    print(f'The addition of Two number is : {first_number + second_number:.2f}')
elif operator == "-":
    print(f'The subtraction of Two number is : {first_number - second_number:.2f}')
elif operator == "*":
    print(f'The multiplication of Two number is : {first_number * second_number:.2f}')
elif operator == "/":
    print(f'The division of Two number is : {first_number / second_number:.2f}')
elif operator == "%":
    print(f'The modulo of Two number is : {first_number % second_number:.2f}')
elif operator == "**":
    print(f'The exponentiation of Two number is : {first_number ** second_number:.2f}')
else:
    print("Sorry ! Please enter a valid operator")