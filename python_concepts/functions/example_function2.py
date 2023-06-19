import sys

# inputs from the 'args' are provided when the code is called
#  python example_function2.py <number1> <number2>
#  filling in the input with specific values:
#  python example_function 1 7

number1 = sys.argv[1]
number2 = sys.argv[2]

def add_numbers(a,b):
    result = a + b
    return result

result = add_numbers(number1,number2)
print (result)

