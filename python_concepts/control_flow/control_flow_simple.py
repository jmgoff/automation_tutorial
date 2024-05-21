# controlling flow in python

## for loops
## for <iterable>:
##     do <something>
a = [1,2,3]
for i in a:
# to do things in a for loop, the corresponding line must be indented
    print(i)


## logicals

b = [2,4,5]

if b[0] == (2*a[0]):
    print(b[0],a[0])

## while loops
## while <condition>
##     do <something>
count = 0
while count < 2:
    print(a[count])
    count += 1 # add 1 to the previous value of count

