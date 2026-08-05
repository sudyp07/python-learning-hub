# an alternative to using many 'elif' statements
# executes some code if  a value matches a 'case'
# benefits --> cleaner and syantax is more readable

# simple match case or switch statement exmaple (you can return boolean value too)

def week_of_day (day):
    match day:
        case 1:
            return "Monday"
        case 2:
            return "Tuesday"
        case 3:
            return "Wednesday"
        case 4:
            return "Thursday"
        case 5:
            return "Friday"
        case 6:
            return "Saturday"
        case 7:
            return "Sunday"
        case _:
            return "Invalid Day"

print(week_of_day(1))        # --> Monday
print(week_of_day(2))        # --> Tuesday
print(week_of_day("Tomato")) # --> Invalid Day


# (you can return boolean value too) example:

def is_nepali_citizen(citizen):
    match citizen:
        case 'Born in Nepal':
            return True
        case _:
            return False

print(is_nepali_citizen("Born in Nepal")) # --> True
print(is_nepali_citizen("Tomato")) # --> False


# you can use or operator like this here (|)

def is_weekend(day):
    match day:
        case 'saturday' | 'sunday':
            return True
        case 'monday' | 'tuesday' | 'wednesday' | 'thursday' | 'friday':
            return False
        case _:
            return False

print(is_weekend("saturday"))     # --> True
print(is_weekend("tuesday"))      # --> False
print(is_weekend("Tomato"))       # --> False




