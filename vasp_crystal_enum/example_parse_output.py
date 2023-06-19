from pymatgen.io.vasp.outputs import Vasprun, Oszicar
import glob

directories = glob.glob('run_*')
for directory in directories:
    os.chdir(directory)

    #let pmg load the output
    vasprun = Vasprun('vasprun.xml')
    # for a smaller object/quick look at the run
    # osz = Oszicar('OSZICAR')
    
    traj = vasprun.get_trajectory()
    # you should see forces and stuff for your
    #  md or relaxation steps!
    print (vars(traj))
