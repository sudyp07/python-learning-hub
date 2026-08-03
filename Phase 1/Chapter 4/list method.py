# It always give only one list by changing the requested change , as given by the user, not new list like below:)

list1 = [5,3,56,6,78,2,5,5,2,6,8,54,35,345,43,5,435,43,534,5,4]

list1.sort()               #sorting the value from small to big                      [2, 2, 3, 4, 5, 5, 5, 5, 5, 6, 6, 8, 35, 43, 43, 54, 56, 78, 345, 435, 534]
list1.reverse()            #reverse the value from end to start                      [4, 5, 534, 43, 435, 5, 43, 345, 35, 54, 8, 6, 2, 5, 5, 2, 78, 6, 56, 3, 5]
list1.append(5)            #it adds 5 at the end of the list                         [5, 3, 56, 6, 78, 2, 5, 5, 2, 6, 8, 54, 35, 345, 43, 5, 435, 43, 534, 5, 4, 5]
list1.insert(4, 87)  #it adds 87 num at 4th index                         [5, 3, 56, 6, 87, 78, 2, 5, 5, 2, 6, 8, 54, 35, 345, 43, 5, 435, 43, 534, 5, 4]
list1.pop(1)               #it pops out num.3 from list cause its in index 1         [5, 56, 6, 78, 2, 5, 5, 2, 6, 8, 54, 35, 345, 43, 5, 435, 43, 534, 5, 4]
print(list1.pop(2))        #it prints the value that pop i.e 56                      #56  --> cause it is located at the 2nd index number
list1.remove(534)          #it removes number 534 from the list                      [5, 3, 56, 6, 78, 2, 5, 5, 2, 6, 8, 54, 35, 345, 43, 5, 435, 43, 5, 4]
list1.clear()              #it removes list data from list []                        []
del list1[2]               #it removes 56 cause its in 2nd index                     [5, 3, 6, 78, 2, 5, 5, 2, 6, 8, 54, 35, 345, 43, 5, 435, 43, 534, 5, 4]

print(list1)
