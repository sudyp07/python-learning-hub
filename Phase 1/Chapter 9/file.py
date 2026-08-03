# Opening a file in write mode
file = open("03_write.txt", "w")  ##here write.txt is file name and 'w' means write in file
file.write("Hello, World!")  # # write the actual content that should write in the particular file
print ("File opened successfully!!")
file.close() # #close the file after work done (after writing the file)


# Opening a file in read mode
file = open("02_read.txt", "r")  # 'read.txt' is the file name and 'r' means read mode
content = file.read()  ##assigning the read function into a content variable
print(content)# reading the actual content of the particular file
print("File Examined successfully!!")
file.close()  # close the file after work done


'''
r = open for reading
w = open for writing
a = open for apending  # IT WILL ADD SOMETHING IN THE END OF ANY FILE
+ = open for updating  
`rb` will open for read in binary mode
`rt` will open for read in text mode 
'''