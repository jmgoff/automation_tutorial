import sys

# inputs from the 'args' are imported as strings by default
number1 = sys.argv[1]
number2 = sys.argv[2]

# converting the strings to floats before using them as input
number1 = float(number1)
number2 = float(number2)

def add_numbers(a,b):
    a = float(a)
    b = float(b)
    result = a + b
    return result

result = add_numbers(number1,number2)
print (result)

