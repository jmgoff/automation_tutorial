from example_class import Number_Pair

a = 1
b = 7

numspair = Number_Pair(a,b)

#---------------------------------------------
# use a method that needs some more work
#---------------------------------------------

numspair.multiply(a,b)
print ('multiplied', numspair.multiplied, '\n\n\n')

# try to change the input

anew = 2
bnew = 5
numspair.multiply(anew,bnew)


