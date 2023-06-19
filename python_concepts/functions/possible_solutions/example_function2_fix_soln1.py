import sys

# inputs from the 'args' are imported as strings by default
number1 = sys.argv[1]
number2 = sys.argv[2]

def add_numbers(a,b):
    # if inputs are given as strings, convert them to floats first
    if type(a) == str:
	a = float(a)
    if type(b) == str:
	b = float(b)
    result = a + b
    return result

result = add_numbers(number1,number2)
print (result)

