# these are more than enough escape sequence

sentence = "Sudeep is a good \n boy but he is poor." #(sentence after (\n) prints in a new line)
sentence2 = "Kumar is a bad boy but he is very\t rich." #(sentence after (\t) prints with a tab space like     gap after very and before rich !!)
sentence3 = 'Harish belongs from a good & reputed \'family\''  #(\'family\' We can get family still inside the double quote c)
sentence4= "This is a backslash: \\"  # (\\)THIS PRINTS A SINGLE BACKSLASH (\)



print(sentence)     #Sudeep is a good
                    #boy but he is poor.
print(sentence2) #   Kumar is a bad boy but he is very	 rich.
print(sentence3) #  Harish belongs from a good & reputed 'family'
print(sentence4) #  This is a backslash: \