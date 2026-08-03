## lets make ATM using python

bank_balance = 10000
user_input = int(input("Enter a number 1 for Cash Withdraw and Number 2 for Cash Deposit : "))


## error handling ##
if user_input != 1 and user_input != 2:
    print("Enter the right number to operate this ATM....")
    raise SystemExit

##headings
if user_input == 1:
    print("=================================")
    print("Welcome to Cash Withdrawl Section.")
    print("=================================")
elif user_input == 2:
    print("=================================")
    print("Welcome to Cash Deposit Section.")
    print("=================================")

## real algorithms here
## withdrawl section

if user_input == 1:
    balance = int(input("Enter the amount you want to withdraw: "))
    if  balance > bank_balance or balance < 0:
        print("You can't withdraw Negative Balance or more balance than you have.")
    else:
        withdraw_balance = bank_balance - balance
        final_balance = bank_balance - balance
        print(f"You have successfully withdrew ${balance} from your bank account.")
        print(f'Final balance is ${final_balance}.')
    pass

## deposit section

if  user_input == 2:
    deposit_balance = int(input("Enter the amount you want to deposit: "))
    print(f"You have successfully deposited ${deposit_balance} into your bank account.")
    print(f'Final balance is ${deposit_balance + bank_balance}.')

print("=======================================")
print("Thank you for using our ATM, Good bye!")
print("=======================================")