import glob
import os
from qe_tools import *
from subprocess import call

def write_slurm(qeinput,job_name,outfile,node_num=22):
    slurm_str = """#!/bin/bash
#SBATCH --nodes=1
#SBATCH -w, --nodelist=node[%d]
#SBATCH --overcommit
#SBATCH --ntasks-per-node=24
#SBATCH --time=24:00:00
#SBATCH --job-name=%s
#SBATCH --output=%s
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

mpirun pw.x < %s""" % (node_num, job_name, outfile, qeinput )
#                        int     str       str      str
    return slurm_str

struct_files = glob.glob('*.cif')
for fileindex,sfile in enumerate(struct_files):
    prefix = sfile.split('.')[0]
    dirname = 'run_%03d' % fileindex
    qeinput = '%s.in' % prefix
    job_name = 'run_%03d' % fileindex
    outfile = '%s.out' % prefix

    slurm_str = write_slurm(qeinput,job_name,outfile,node_num=22)
    slurm_file = './%s/submit_%03d.slurm' % (dirname,fileindex)
    with open(slurm_file,'w') as swrite_file:
        swrite_file.write(slurm_str)
    #print (slurm_str)
