from example_class import Number_Pair

a = 1
b = 7

numspair = Number_Pair(a,b)

#---------------------------------------------
# use another method (function) from the class
#---------------------------------------------

numspair.subtract()
print ('subtracted: a-b', numspair.subtracted)

# try the other order
numspair.subtract(order='b-a')
print ('subtracted: b-a', numspair.subtracted)

# print all of the attributes 
print (vars(numspair))



