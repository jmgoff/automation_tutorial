# strings may be modified & formatted in useful ways

## adding variable integer values to a string
values = [1,2,3,4]
for i in values:
    # %d for integers
    string = 'value: %d' % i
    print(string)

## adding variable floats to a string
values = [float(k) for k in values]
for i in values:
    # %f for floats
    string = 'value: %f' % i
    print(string)

values = ['a','b','c']
for i in values:
    # %s for floats
    string = 'value: %s' % i
    print(string)

values = [100,200,300,400]
## specify digits
for i in values:
    # %0<n>d -> n leading zeros for integer
    print("%05d" % i)

## How do you think we add in digits for floats???
## Answer below:

## f string formatting is also useful
value = 5
c = f"specified value: {value}"
print(c)
