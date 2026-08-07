# Python Slot Machine

import random


def spin_row():
    symbols = ["🍒", "🍉", "🍋", "🔔", "⭐"]
    return [random.choice(symbols) for _ in range(3)]


def print_row(row):
    print("*************")
    print(" | ".join(row))
    print("*************")


def get_payout(row, bet):
    if row[0] == row[1] == row[2]:
        if row[0] == "🍒":
            return bet * 3
        elif row[0] == "🍉":
            return bet * 4
        elif row[0] == "🍋":
            return bet * 2
        elif row[0] == "⭐":
            return bet * 20
        elif row[0] == "🔔":
            return bet * 10

    return 0


def main():
    balance = 100

    print("**************************************")
    print("** Welcome to the Python Slot Machine **")
    print("******** SYMBOLS: 🍒 🍉 🍋 🔔 ⭐ ********")
    print("**************************************")

    while balance > 0:
        print(f"\nCurrent Balance: ${balance}")

        bet = input("Enter your bet amount: ")

        if not bet.isdigit():
            print("Please enter a positive number.")
            continue

        bet = int(bet)

        if bet <= 0:
            print("Bet must be greater than zero.")
            continue

        if bet > balance:
            print("Insufficient funds.")
            continue

        balance -= bet

        print("\nSpinning...\n")
        row = spin_row()
        print_row(row)

        payout = get_payout(row, bet)

        if payout > 0:
            print(f"🎉 YOU WON ${payout}!")
        else:
            print("😢 YOU LOST THIS ROUND.")

        balance += payout

        if balance <= 0:
            print("You're out of money!")
            break

        play_again = input("\nWould you like to play again? (y/n): ").upper()

        if play_again != "Y":
            break

    print("\n**********************************************")
    print(f"Game Over! Your final balance is ${balance}.")
    print("**********************************************")


if __name__ == "__main__":
    main()