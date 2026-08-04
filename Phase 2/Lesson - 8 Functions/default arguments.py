def net_price (list_price, discount = 0 , tax = 0.05):
    return list_price * ( 1 - discount) * ( 1 + tax)

print(net_price(500))  ## 525.0 cause we got zero discount as default and 0.05 % of tax in the product of 500 rupees.
print(net_price(1000 , 0.1)) # 945.0 cause we got 0.1 discount in the product of 1000 rupees and tax of 0.05 %.


 # simple excercise

import  time

def count( end , start = 5 ): ## place parameters at second with value to work default value functions works properly.
    for x in range(start,end+1):
         print(x)
         time.sleep(1)
    print("Finished !!")

count(0,10) ## here we gave a non default arguments to parameters.
count(12) ## here we pass a end but not start cause we passed the default parameters of start value to 5)