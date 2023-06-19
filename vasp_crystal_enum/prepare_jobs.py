import glob
import os 

def make_slurm(jobid):
    vstr = """#!/bin/bash
#SBATCH --job-name=run_%03d
#SBATCH --account=<your_account_name>
#SBATCH --partition=short,batch
#SBATCH --time=4:00:00
#SBATCH --nodes=1
#SBATCH --output=outrun.out

### end of slurm stuff

#load the required modules for vasp

module load  ...

#add the vasp executable to your path
# maybe in your bashrc?

source ~/.bashrc

#run vasp

mpirun -n 16 vasp_std 
""" % jobid
    return vstr


struct_files = glob.glob('*.cif')
for sid,sfile in enumerate(struct_files):
    prefix = sfile.split('.')[0]
    os.chdir('./run_%s' % prefix)
    vstr = make_slurm(sid)
    with open('run_%03d.s' % sid,'w') as writeslurm:
        writeslurm.write(vstr)
    os.chdir('../')

