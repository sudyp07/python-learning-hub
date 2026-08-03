#Python compound interest calculator using python while loop :)

principle = 0
rate = 0
time = 0

while principle <= 0:
    principle = float(input("Enter the Principle amount: "))
    if principle <= 0:
        print("Principle can't be 0 or less than 0.")

while rate <= 0:
    rate = float(input("Enter the interest rate: "))
    if rate <= 0:
        print("Interest can't be 0 or less than 0.")

while time <= 0:
    time = int(input("Enter the  time: "))
    if time <= 0:
        print("Interest can't be 0 or less than 0.")

total = principle * (1 + rate / 100)

print(f'Balance afer {time} year/s: ${total:.2f}')


'''
THIS METHOD ALLOWS USER TO ENTER ZER0 VALUE AS WELL
#Python compound interest calculator using python while loop :)
'''
principle = 0
rate = 0
time = 0

while True:
    principle = float(input("Enter the principle amount: "))
    if principle < 0:
        print("Principle can't be less than 0.")
    else:
        break

while True:
    rate = float(input("Enter the interest rate: "))
    if rate < 0:
        print("Interest rate can't be less than 0.")
    else:
        break

while True:
    time = int(input("Enter the time: "))
    if time < 0:
        print("Time can't be less than 0.")
    else:
        break

total = principle * (1 + rate / 100) ** time

print(f'Balance afer {time} year/s: ${total:.2f}')

