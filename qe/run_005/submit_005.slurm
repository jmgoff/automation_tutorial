#!/bin/bash
#SBATCH --nodes=1
#SBATCH -w, --nodelist=node[22]
#SBATCH --overcommit
#SBATCH --ntasks-per-node=24
#SBATCH --time=24:00:00
#SBATCH --job-name=run_005
#SBATCH --output=Ni_cubic_bcc_atoms.out
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

mpirun pw.x < Ni_cubic_bcc_atoms.in