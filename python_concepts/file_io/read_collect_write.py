import numpy as np

# path to file
f = './data/example.txt'
# use the open function in read 'r' mode
with open(f, 'r') as readin:
    # read in line per line
    lines = readin.readlines()

for line in lines:
    l = line.split() #convert string to list of strings splitted where there are spaces
    if 'energy' in line:
        energy = float(l[-1]) 
        with open('energy_only.txt', 'w') as writeout:
            writeout.write('%1.2f' % energy)

    if 'force' in line:
        frc_vec = [float(k) for k in l[1:]]
        frc_vec = np.array(frc_vec)        
        np.save('force.npy',frc_vec)

