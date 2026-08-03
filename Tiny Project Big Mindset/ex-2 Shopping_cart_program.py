#shopping cart programs -->

item = input('What item do you like to purchase?: ').lower()
price = float(input('What is the price for the item?: '))
quantity = int(input('How many quantity would you like?: '))
total_price = price * quantity

#lets make it more better by adding some variables:
print(f"You purchased {quantity} x {item}/s.")
print(f'Your total is : ${total_price:.2f}')
print(f'The total price of {item} is ${total_price:.2f}.')

"""
You purchased 3 x shirt/s.
Your total is : $30.99
The total price of shirt is $30.99.
"""