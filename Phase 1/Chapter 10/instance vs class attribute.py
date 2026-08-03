class employee:
    language = 'python'  ## this is a class attribute
    salary = 10000

sudip = employee()
sudip.language = 'JavaScript'  #This is an instance attribute
print( sudip.language ,sudip.salary )

## here if you give just class attribute for the function it will print  the class attribute
## but if you give instance attribute for the function it will prin the instance attribute
## it always takes instance value as a default value it both value assigns .....