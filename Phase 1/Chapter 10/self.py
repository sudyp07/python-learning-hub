class employee:
    language = 'python'  ## this is a class attribute
    salary = 10000

    def getInfo(self):
        print(f'The language is {self.language} and salary is ${self.salary}')



sudip = employee()
sudip.language = 'JavaScript'  #This is an instance attribute
print( sudip.language ,sudip.salary )

# sudip.getInfo()  ## it will give error
employee.getInfo(sudip) ## --> this is right


## output ::
"""
JavaScript 10000
The language is JavaScript and salary is $10000
"""

## we have to give self  in everywhere we make a function