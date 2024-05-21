# accessing items in python lists
#  (and other list-like types)

a = [1,2,3]

# items in a python list are assigned base-zero indices

print(a[0])
print(a[1])
print(a[2])

# values may be accessed and modified index-wise
a[0] = 6

print (a)

# you can insert other items into a list
## append new element at the end of the list
a.append(3) 
print(a)

## add new element at a specified index:
a.insert(0,1)
print(a)
## syntax is x.insert(<index>,item)


# the index corresponding to the first appearance of an element may be found
#  with the '.index' function

print(a.index(6))

# see more at: https://docs.python.org/3/tutorial/introduction.html#lists
