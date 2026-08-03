import time

my_time = int(input("Enter the time in seconds: "))

for x in range(0, my_time):
    seconds = x % 60
    print(f"00:00:{seconds}")
    time.sleep(1)

print("TIME'S UP !!")  # it will print this like the second we gave and it will time up the stopwatch)



# In reversed an in advanced way:

my_time = int(input("Enter the time in seconds: "))

for x in range(my_time ,0, -1):
    seconds = x % 60
    minutes = int(x / 60) % 60
    hours = int(x / 3600)
    print(f"{hours:02}:{minutes:02}:{seconds:02}")
    time.sleep(1)

print("TIME'S UP !!")   # it will print the time in hour, minutes and second  in reveresed way properly !!

