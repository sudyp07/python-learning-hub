# banking program with python using functions

def show_balance(balance):
    print(f'Your current balance is ${balance:.2f}')

def deposit():
    amount = float(input("Enter amount to deposit: "))

    if amount <= 0:
        print("Please enter a positive amount")
        return 0
    else:
        return amount


def withdraw(balance):
    amount = float(input("Enter amount to withdraw: "))

    if amount > balance:
        print("You cannot withdraw more than you have.")
        return 0
    elif amount <= 0:
        print("Please enter a positive amount")
        return 0
    else:
        return amount

def main():
    balance = 0
    is_running = True

    while is_running:
        print("BANKING PROGRAM STARTED")
        print("1.Show Balance")
        print("2.Deposit")
        print("3.Withdraw")
        print("4.Exit")

        choice = input("Enter your choice from (1-4):  ")

        if choice == "1":
            show_balance(balance)
        elif choice == "2":
            balance += deposit()
        elif choice == "3":
            balance -= withdraw(balance)
        elif choice == "4":
            is_running = False
        else:
            print("Please enter a valid choice.")

if __name__ == "__main__":
    main()

print("Thank you for using our Banking Program")