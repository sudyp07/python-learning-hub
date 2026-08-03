class employee:
    language = "Python" ## THIS IS A CLASS ATTRIBUTE
    salary = 10000 ## THIS IS A CLASS ATTRIBUTE


sudeep = employee()
sudeep.name = 'sudeep' ## THIS IS AN OBJECT ATTRIBUTE
print( sudeep.name ,sudeep.language,sudeep.salary )

saif = employee()
saif.name = "Saif Ali Khan"
print( saif.name ,saif.language,saif.salary )


## here name is an object attribute and
# salary and language are class attribute as they belongs directly to the class


##class is universal but instance differs from each user respectivelyyy.. -->

