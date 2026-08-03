## BASIC CONTINUE LOOP , it will print from 1 to 10 except 7

for i in range(1,11):
    if i == 7:
        continue
    else:
        print(i)


## BASIC BREAK LOOP, it will break the loop there when the number meets

for i in range(1,11):
    if i == 5:
        break
    else:
        print(i)


## BASIC PASS LOOP, it will Print the number continiously from 1 to 10 without any error without deducting number in loops.

for i in range(1,11):
    if i == 5:
        pass
    else:
        print(i)
