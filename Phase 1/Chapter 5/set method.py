# SET METHODS
set1 = {5, 3, 56, 6, 78, 2, 8, 54, 35, 345, 43, 435, 534, 4}

set1.add(100)                           # Adds 100 to the set                                {2, 3, 4, 5, 6, ..., 534, 100}
(set1.update([200, 300]))               # Adds multiple values                               {2, 3, 4, 5, ..., 100, 200, 300}
set1.remove(56)                         # Removes 56 (Error if not found)                    {2, 3, 4, 5, 6, ..., 534}
set1.discard(500)                       # Removes 500 if present (No Error if missing)       No Error
print(set1.pop())                       # Removes & returns a random element                 e.g. 35
set1.clear()                            # Removes all elements                               set()
set2 = set1.copy()                      # Creates and returns a shallow copy                 Copy of set1
print(len(set1))                        #Counts the length of values inside set              14

#accessing the data from sets :)

result = set1.update([200, 300])
print(set1)                             #always print sets like it only you can access result


# SET OPERATIONS

A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
A.union(B)                              # Combines both sets                                 {1, 2, 3, 4, 5, 6}
A.intersection(B)                       # Common elements                                    {3, 4}
A.difference(B)                         # Elements in A but not in B                         {1, 2}
A.symmetric_difference(B)               # Elements in either set, not both                   {1, 2, 5, 6}
A.intersection_update(B)                # Keeps only common elements                         {3, 4}
A.difference_update(B)                  # Removes common elements                            {1, 2}
A.symmetric_difference_update(B)        # Updates to symmetric difference                    {1, 2, 5, 6}
A.isdisjoint(B)                         # True if no common elements                         False
A.issubset(B)                           # True if A is a subset of B                         False
A.issuperset(B)                         # True if A is a superset of B                       False