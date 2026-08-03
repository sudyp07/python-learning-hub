# making rectangle by taking user input and symbols

rows = int(input("Enter number of rows: "))
columns = int(input("Enter number of columns: "))
symbols = input("Enter any types of symbols you want: ")


for x in range(rows):
    for i in range (columns):
        print(symbols , end = " ")
    print()


## Output :
'''

Enter number of rows: 7
Enter number of columns: 10
Enter any types of symbols you want: 😜

😜 😜 😜 😜 😜 😜 😜 😜 😜 😜 
😜 😜 😜 😜 😜 😜 😜 😜 😜 😜 
😜 😜 😜 😜 😜 😜 😜 😜 😜 😜 
😜 😜 😜 😜 😜 😜 😜 😜 😜 😜 
😜 😜 😜 😜 😜 😜 😜 😜 😜 😜 
😜 😜 😜 😜 😜 😜 😜 😜 😜 😜 
😜 😜 😜 😜 😜 😜 😜 😜 😜 😜 

'''