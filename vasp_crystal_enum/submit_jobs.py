import glob
import os 
from subprocess import call

struct_files = glob.glob('*.cif')
for sid,sfile in enumerate(struct_files):
    prefix = sfile.split('.')[0]
    os.chdir('./run_%s' % prefix)
    #NOTE once you uncomment 'this line', all of the slurm
    #  files in this example will be submitted to the scheduler. 
    #  it is commented out at first so you can do a 'dry 
    #  run'.
    #call('sbatch run_%03d.s' % sid,shell = True) #NOTE 'this line'
    call('echo submitted job for %s' % prefix, shell = True)
    os.chdir('../')

