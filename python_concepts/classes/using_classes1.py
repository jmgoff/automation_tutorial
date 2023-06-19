from example_class import Number_Pair

a = 1
b = 7

numspair = Number_Pair(a,b)

# print the attribute that corresponds to the addition of a and b
print(numspair.added)

# print all of the attributes 
print (vars(numspair))

# use another method 

numspair.subtract()

#print the result

print(numspair.subtracted)





