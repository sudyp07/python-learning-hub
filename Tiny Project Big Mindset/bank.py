import random
import time
import sys

# Constants
choices = (
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
)

# User database
users = {}

# Current session variables
current_user = None
current_balance = 0

# Main program loop
while True:
    print("\n" + "=" * 40)
    print("         SUDIP BANK")
    print("=" * 40)
    print("1. Account Creation")
    print("2. Account Login")
    print("3. Exit")
    print("=" * 40)

    try:
        main_choice = int(input("Enter your choice (1-3): "))
    except ValueError:
        print("❌ Please enter a valid number!")
        continue

    # ============ ACCOUNT CREATION ============
    if main_choice == 1:
        print("\n" + "=" * 40)
        print("       ACCOUNT CREATION")
        print("=" * 40)

        full_name = input("Enter your full name: ").strip()
        if not full_name:
            print("❌ Name cannot be empty!")
            continue

        address = input("Enter your address: ").strip()
        phone_number = input("Enter your phone number: ").strip()

        # Generate username
        base = full_name[0:4].lower()
        random_part = ''.join(random.choices(choices, k=5)).lower()
        username = base + random_part

        # Set password
        password = input("Create a password (min 4 characters): ").strip()
        if len(password) < 4:
            print("❌ Password must be at least 4 characters!")
            continue

        # Store user
        users[username] = {
            'full_name': full_name,
            'address': address,
            'phone': phone_number,
            'password': password,
            'balance': 1000.0
        }

        print(f"\n✅ Account Created Successfully!")
        print(f"👤 Name: {full_name}")
        print(f"🔑 Username: {username}")
        print(f"💰 Initial Balance: $1000.00")
        print("\n📝 Please note your username for login!")
        time.sleep(2)

    # ============ ACCOUNT LOGIN ============
    elif main_choice == 2:
        print("\n" + "=" * 40)
        print("         ACCOUNT LOGIN")
        print("=" * 40)

        username_input = input("Enter your username: ").strip()
        password_input = input("Enter your password: ").strip()

        if username_input in users and users[username_input]['password'] == password_input:
            current_user = username_input
            current_balance = users[current_user]['balance']
            print(f"\n✅ Welcome back, {users[current_user]['full_name']}!")
            print("You are now logged in.")
            time.sleep(1)

            # ============ BANKING MENU (Logged In) ============
            while current_user is not None:
                print("\n" + "=" * 40)
                print("         BANKING OPERATIONS")
                print("=" * 40)
                print(f"👤 User: {users[current_user]['full_name']}")
                print("-" * 40)
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Transfer")
                print("4. Check Balance")
                print("5. Change Password")
                print("6. Logout")
                print("=" * 40)

                try:
                    bank_choice = int(input("Select an option (1-6): "))
                except ValueError:
                    print("❌ Please enter a valid number!")
                    continue

                # ---------- DEPOSIT ----------
                if bank_choice == 1:
                    print("\n" + "=" * 40)
                    print("         DEPOSIT SECTION")
                    print("=" * 40)

                    try:
                        deposit_amount = float(input("Enter amount to deposit: $"))
                        if deposit_amount <= 0:
                            print("❌ Amount must be greater than 0!")
                        else:
                            current_balance += deposit_amount
                            users[current_user]['balance'] = current_balance
                            print(f"✅ Successfully deposited ${deposit_amount:.2f}")
                            print(f"💰 New balance: ${current_balance:.2f}")
                    except ValueError:
                        print("❌ Please enter a valid number!")

                # ---------- WITHDRAW ----------
                elif bank_choice == 2:
                    print("\n" + "=" * 40)
                    print("         WITHDRAWAL SECTION")
                    print("=" * 40)

                    try:
                        withdraw_amount = float(input("Enter amount to withdraw: $"))
                        if withdraw_amount <= 0:
                            print("❌ Amount must be greater than 0!")
                        elif withdraw_amount > current_balance:
                            print(f"❌ Insufficient balance! You have ${current_balance:.2f}")
                        else:
                            current_balance -= withdraw_amount
                            users[current_user]['balance'] = current_balance
                            print(f"✅ Successfully withdrew ${withdraw_amount:.2f}")
                            print(f"💰 New balance: ${current_balance:.2f}")
                    except ValueError:
                        print("❌ Please enter a valid number!")

                # ---------- TRANSFER ----------
                elif bank_choice == 3:
                    print("\n" + "=" * 40)
                    print("         TRANSFER SECTION")
                    print("=" * 40)

                    recipient = input("Enter recipient's username: ").strip()

                    if recipient not in users:
                        print("❌ Recipient account not found!")
                    elif recipient == current_user:
                        print("❌ Cannot transfer to yourself!")
                    else:
                        try:
                            transfer_amount = float(input("Enter amount to transfer: $"))
                            if transfer_amount <= 0:
                                print("❌ Amount must be greater than 0!")
                            elif transfer_amount > current_balance:
                                print(f"❌ Insufficient balance! You have ${current_balance:.2f}")
                            else:
                                # Process transfer
                                current_balance -= transfer_amount
                                users[current_user]['balance'] = current_balance
                                users[recipient]['balance'] += transfer_amount
                                print(
                                    f"✅ Successfully transferred ${transfer_amount:.2f} to {users[recipient]['full_name']}")
                                print(f"💰 New balance: ${current_balance:.2f}")
                        except ValueError:
                            print("❌ Please enter a valid number!")

                # ---------- CHECK BALANCE ----------
                elif bank_choice == 4:
                    print("\n" + "=" * 40)
                    print("         BALANCE CHECK")
                    print("=" * 40)
                    print(f"💰 Your current balance: ${current_balance:.2f}")

                # ---------- CHANGE PASSWORD ----------
                elif bank_choice == 5:
                    print("\n" + "=" * 40)
                    print("         CHANGE PASSWORD")
                    print("=" * 40)

                    old_password = input("Enter your old password: ")

                    if users[current_user]['password'] != old_password:
                        print("❌ Incorrect old password!")
                    else:
                        new_password = input("Enter your new password (min 4 characters): ")
                        if len(new_password) < 4:
                            print("❌ Password must be at least 4 characters!")
                        else:
                            confirm_password = input("Confirm your new password: ")
                            if new_password != confirm_password:
                                print("❌ Passwords do not match!")
                            elif new_password == old_password:
                                print("❌ New password must be different from old password!")
                            else:
                                users[current_user]['password'] = new_password
                                print("✅ Password changed successfully!")

                # ---------- LOGOUT ----------
                elif bank_choice == 6:
                    print("\n" + "=" * 40)
                    print("         LOGGING OUT")
                    print("=" * 40)

                    confirm = input("Are you sure you want to logout? (y/n): ").lower()
                    if confirm == 'y':
                        print(f"👋 Goodbye, {users[current_user]['full_name']}!")
                        current_user = None
                        current_balance = 0
                        time.sleep(1)
                        break
                    else:
                        print("Logout cancelled.")

                else:
                    print("❌ Invalid choice! Please select 1-6.")

                time.sleep(0.5)

        else:
            print("\n❌ Invalid username or password!")
            time.sleep(1)

    # ============ EXIT ============
    elif main_choice == 3:
        print("\n👋 Thank you for using SUDIP BANK!")
        print("Goodbye!")
        break

    else:
        print("❌ Invalid choice! Please select 1-3.")