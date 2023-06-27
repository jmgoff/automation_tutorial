from pymatgen.io.vasp.outputs import Vasprun, Oszicar
import glob

directories = glob.glob('run_*')
for directory in directories:
    os.chdir(directory)

    #let pmg load the output
    vasprun = Vasprun('vasprun.xml')
    band_gap = vasprun.get_band_structure().get_band_gap()
    # for a smaller object/quick look at the run
    # osz = Oszicar('OSZICAR')
    
    traj = vasprun.get_trajectory()
    # you should see forces and stuff for your
    #  md or relaxation steps!
    print (vars(traj))
    # you have access to other properties too such as band gap
    band_gap = vasprun.get_band_structure().get_band_gap()
