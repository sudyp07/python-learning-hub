foods = []
prices = []
total = 0

while True:
    food = (input("Enter food you want to buy: "))
    if food.lower() == "q":
        break
    else:
        price = float(input("Enter price of food $: "))
        foods.append(food)
        prices.append(price)

print("-------YOUR CART----------")

for food in foods:
    print(food , end =" ")

for price in prices:
    total += price

print()
print(f'The total prices of food is {total}.')