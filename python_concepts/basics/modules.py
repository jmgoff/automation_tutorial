# modules may be imported using import commands:
import numpy as np
# numpy libraries contain objects and data types that are convenient for math


# for example, consider this numpy array
a = np.array([1,2,3])

print(a)
print(type(a))

# certain math is easier with numpy arrays
print(a*2)

# similar operations do different things with lists
c = [1,2,3]
print (c*2) 


# Note, you may load a module without giving it an abbreviated reference
import numpy
b = numpy.array([1,2,3])
print(b)
print(type(b))
