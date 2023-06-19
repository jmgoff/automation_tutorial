from example_class import Number_Pair


a_lst = [1,2,3,5,7]
b_lst = [2,2,1,2,5]

for a,b in zip(a_lst,b_lst): # zip is a way to iterate over the two lists above
    nmpr = Number_Pair(a,b)
    if a > b:
        subtraction_order = 'a-b'
    else:
        subtraction_order = 'b-a'
    nmpr.subtract(subtraction_order)
    nmpr.multiply(a,b)
    print (a,b,'addition:', nmpr.added, 'subtracted:', nmpr.subtracted, 'multiplied:', nmpr.multiplied)
