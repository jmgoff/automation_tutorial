import glob
import os
from qe_tools import *
from subprocess import call


struct_files = glob.glob('*.cif')
for fileindex,sfile in enumerate(struct_files):
    prefix = sfile.split('.')[0]
    dirname = 'run_%03d' % fileindex
    qeinput = '%s.in' % prefix
    job_name = 'run_%03d' % fileindex
    outfile = '%s.out' % prefix

    slurm_file = 'submit_%03d.slurm' % (fileindex)
    os.chdir(dirname)
    shell_line = 'sbatch %s' % slurm_file
    print (shell_line)
    call(shell_line,shell=True) # comment this out to do a dry run
    os.chdir('../')

