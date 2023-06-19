import os
from subprocess import call

num_samples = 25

for isamp in range(num_samples):
    dirname = 'sample_%03d' % isamp
    print ('running fit in %s' % dirname)
    os.chdir(dirname)
    call('mpirun -n 2 python3 -m fitsnap3 Ta-example.in &> outfit.txt',shell = True)
    os.chdir('../')
