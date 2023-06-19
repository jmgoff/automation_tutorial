import os
import numpy as np

def datafile_string(en,force):
    # function, using string formatting, to put energy and force values into the
    # format we saw before
    contents = """energy: %f
force: %f %f %f""" % (tuple([en]) + tuple(list(force)))
    return contents

np.random.seed(54921) # so we all get the same random values

energies = np.random.rand(10)
forces = np.random.rand(10,3)

for i in range(len(energies)):
    energy_i = energies[i]
    force_i = forces[i]
    dirname = './data/random_data_%03d' % i
    if not os.path.isdir(dirname):#if the folder doesnt exist...
        os.mkdir(dirname) #make one!
    os.chdir(dirname) #move into the folder
    with open('example.txt','w') as writeout:
        datafile_contents = datafile_string(energy_i,force_i)
        writeout.write(datafile_contents)
    os.chdir('../../') # go back to our working directory
