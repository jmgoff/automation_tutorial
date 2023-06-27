import glob
import os
from qe_tools import *
from subprocess import call

def build_slurm():
    sstr = """#!/bin/bash
# set the number of nodes
#SBATCH --nodes=1

# Set the specific number of nodes
#SBATCH -w, --nodelist=node[22]

# set the number of tasks (processes) per node.
#SBATCH --overcommit
#SBATCH --ntasks-per-node=24

# set max wallclock time
#SBATCH --time=1:00:00

# set name of job
#SBATCH --job-name=qeNiSIM

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL
# send mail to this address

# Screen output
#SBATCH --output=screen_output
###SBATCH -p week-long-cpu
#SBATCH --partition=day-long-cpu

source ~/.bashrc

module load intel/2018.2.199
module load openmpi/intel/2018.2.199/4.0.0

export PATH=$PATH:/mnt/nfs/wenwu/kyrel/qeInstall/qe-7.2/bin
export PYTHONPATH=$PYTHONPATH:/mnt/nfs/wenwu/Hadia/automation_tutorial-main/tools/
export TUTORIAL_PATH=/mnt/nfs/wenwu/Hadia/automation_tutorial-main
export ESPRESSO_PSEUDO=$TUTORIAL_PATH/qe_pseudos

echo "$PWD"

mpirun pw.x < %s.in > %s.out 
"""


struct_files = glob.glob('*.cif')
for fileindex,sfile in enumerate(struct_files):
    atoms = read(sfile)
    prefix = sfile.split('.')[0]
    if len(atoms) ==1:
        scell = (1,1,2)
    else:
        scell = (1,1,1)
    qei = QEInput(atoms*scell)
    ishex = False
    if 'hex' in prefix:
        ishex = True
    qei.generate_kpoints(density=45,ishex=ishex)
    qei.kpoints_settings(qei.kpoints,qei.kpoints_shft)
    qei.default_settings(spin_polarized=True)
    #qei.system['nosym']= '.false.' # turn symmetry back on to speed up! (you just wont print forces)
    dirname = 'run_%03d' % fileindex
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    qei.write_input('./%s/%s.in' % (dirname, prefix))
    call('cp %s ./%s' % (sfile,dirname),shell = True)
