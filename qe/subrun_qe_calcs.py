import glob
import os
from subprocess import call

struct_files = glob.glob('*.cif')
for fileindex,sfile in enumerate(struct_files):
    print ('running',sfile)
    prefix = sfile.split('.')[0]
    dirname = 'run_%03d' % fileindex
    os.chdir(dirname)
    call('mpirun -np 24 pw.x -in %s.in &> %s.out ' % (prefix,prefix),shell = True)
    os.chdir('../')
