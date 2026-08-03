# indexing  = accessing elements of a sequence using [] (indexing operator)
# [start : end: step]

credit_card_number = "5414-3753-6572-1098"

print(credit_card_number[0])    # 5
print(credit_card_number[:4])   # 5414
print(credit_card_number[5:9])  # 3753
print(credit_card_number[5:])   # 3753-6572-1098
print(credit_card_number[-1])   # 8
print(credit_card_number[::2])  # 51-7367-08 # it jumps 2 steps from first to last

## simple excercise to get the last 4 digit of the credit card number:
print(credit_card_number[15:]) #1098

# using negative indexing
print(credit_card_number[-4:]) #1098