## passing simple arguments
def greet (name):
    print("Hello, " + name + "!")

greet("Sudeep")  ##Hello, Sudeep!

## making intermediate function (here name parameters take name like Ram and ending parameter take word like Thanks)
def goodday (name , ending):
    print("Hello, " + name + "!")

goodday("Ram" , "Thanks")    ##Hello, Ram!
goodday("Shyam" , "Takecare") ##Hello, Shyam!
goodday("Hari" , "Byee") ##Hello, Hari!


## Making return fuctions with variables
def hello(name , ending):
    print("Hello, " + name + "!" + ending)  ## Hello Ram! Thanks
    print(ending)                           ## Thanks
    return "ok"                             ## ok

a = hello("Ram" , "Thanks") # if we assign function call in the variables we should always use retun like above
print(a)


# # default parameter and arguments
def goodday(name, ending = "Thank you" ):
    print(f"Goodday, {name}", end = " ")
    print(ending)

# # here if we didnt assign a value in argument it will print the default value i.e , Thank you
goodday('Harry!!' , "Goodbye")   ## we gave its respective value so it returns  (Goodday, Harry!! # #Goodbye)
goodday("Cyrus!!")             ## we didnt assign respective value so it takes default value  (Goodday, Cyrus!! Thank you)