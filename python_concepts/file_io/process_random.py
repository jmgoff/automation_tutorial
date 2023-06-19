import os
import glob
import numpy as np

def process_file(f):
    with open(f, 'r') as readin:
        # read in line per line
        lines = readin.readlines()
    for line in lines:
        l = line.split()
        if 'energy' in line:
            energy = float(l[-1])
        if 'force' in line:
            frc_vec = [float(k) for k in l[1:]]
            frc_vec = np.array(frc_vec)
    return energy,frc_vec

data_folders = glob.glob('./data/random_data*')
print(data_folders)
data_folders = sorted(data_folders)

energies = []
forces = []
for fold in data_folders:
    os.chdir(fold)
    # what directory are we in after this operation?
    # check with this command:
    this_dir = os.getcwd()
    #example files in this folder:
    files_in_this_folder = [f for f in os.listdir(this_dir) if 'example' in f]
    for file in files_in_this_folder:
        energy,force = process_file(file)
        print (this_dir, energy, force)
        energies.append(energy)
        forces.append(force)
    os.chdir('../../') # go back to our working directory

print ('parsed energy list:', energies)

