# For all examples:

It is highly recommended to run this in a virtual environment.
(Though it is not completely necessary.)

You can do so after you have installed anaconda:

conda create -n autotutorial python=3.10

conda activate autotutorial


After an environment is chosen (base or the one above),
you must set some tutorial paths and variables.


export TUTORIAL_PATH=/path/to/automation

- linux:

export PYTHONPATH=$PYTHONPATH:$TUTORIAL_PATH/tools

- max/ios:

export PYTHONPATH="${PYTHONPATH}:$TUTORIAL_PATH/tools"



# For VASP examples:
install required packages:

pip install ase
pip install pymatgen

You will need to set your pymatgen vasp pseudopotential
directory. You may do so by makeing a file in your home's
config folder.
Check first to make sure you have a config folder:

ls ~/.config

If nothing shows up, then run

mkdir ~/.config

Once this folder is made, you may open up a pmgrc.yaml file
there:

vi ~/.config/.pmgrc.yaml

enter this into the first line, replacing /path/to/ with 
your own path to our automation tutorial folder. Do NOT
enter the variable for the tutorial path here.

PMG_VASP_PSP_DIR: /path/to/automation/POT_PAW_PBE_52

IMPORTANT NOTE: you will have to ask james for this folder
because he cannot post it on github! Shoot him an 
email in advance if at all possible to request.

# for QE examples
Install QE v. 7.0 or later. See james for help if stuck!
You only need to do these steps if you have QE installed
and/or want to run QE DFT calculations.

First, add quantum espresso executables to your path

- linux

export PATH=$PATH:/path/to/qe-7.1/bin

- mac/ios

export PATH="${PATH}:/path/to/qe-7.1/bin"

Second, set the variable: $ESPRESSO_PSEUDO

- linux

export ESPRESSO_PSEUDO=$TUTORIAL_PATH/qe_pseudos

- mac/ios

export ESPRESSO_PSEUDO="$TUTORIAL_PATH/qe_pseudos"

# For FitSNAP examples
! IF FitSNAP is not already installed, get an installation
This requires the use of conda for these examples.

Step 0: Install anaconda if you have not already.

Step 1: install dependencies (lammps first)

conda install lammps

pip install numpy scipy scikit-learn virtualenv psutil pandas tabulate mpi4py Cython

Step 2: download FitSNAP somewhere convenient

git clone https://github.com/FitSNAP/FitSNAP.git

Step 3: Set the required environmental variables

FITSNAP_DIR=\path\to\FitSNAP

export PYTHONPATH=$FITSNAP_DIR:$LAMMPS_DIR/python:$PYTHONPATH
