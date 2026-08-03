class employee:
    language = 'python'
    salary = 10000

    def __init__(self, name, salary, language):  ## dunder method, which is automatically called !!
        self.name = name
        self.salary = salary
        self.language = language
        print('Creating Object .....')

    def getInfo(self):
        print(f'The language is {self.language} and salary is ${self.salary}')


sudip = employee("SUDEEP_BOSS","1221212", "JAVA") ## WE ASSIGN IT TO THE DUNDER OPTION ABOVE
print( sudip.name, sudip.language ,sudip.salary )
