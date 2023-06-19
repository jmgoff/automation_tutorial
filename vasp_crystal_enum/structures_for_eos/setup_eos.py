from pymatgen.core import Structure
from pymatgen.io.vasp.sets import MPStaticSet, MPRelaxSet, MPNonSCFSet
from pymatgen.io.vasp.inputs import *
from pymatgen.io.ase import *
from crystal_enum import *
from subprocess import call
import glob

def setup_calc_for_struct(structfile):
    s1 = structfile
    file_prefix = s1.split('.')[0]
    structure = Structure.from_file(s1)

    atoms = AseAtomsAdaptor.get_atoms(structure)

    # -------------------------------------------------------------
    # initialize pymatgen vasp input object using materials project
    # defaults
    # -------------------------------------------------------------

    relax_input_set = MPRelaxSet(structure)

    # -------------------------------------------------------------
    # try to detect lattice symmetry to help with Kpoint setup
    # -------------------------------------------------------------

    lat_type_ishex = False
    lat_type,hall_num = get_cell_type(atoms)
    if hall_num == 0:
        print('failed to detect current lattice symmetry, trying to find parent lattice symmetry')
        tmp_ats = atoms.copy()
        syms = [atoms[0].symbol] * len(atoms)
        tmp_ats.set_symbols(syms)
        lat_type,hall_num = get_cell_type(tmp_ats)

    # -------------------------------------------------------------
    # set up kpoints with uniform kpoint density in recip. space
    #  or use one of the other schemes available in pymatgen
    # -------------------------------------------------------------

    kdens = 20
    gflag = False
    if hall_num in range(183,195):
        ks = Kpoints.automatic_density_by_vol(structure,kppvol=kdens,force_gamma=True)
    elif hall_num not in range(183,195) and hall_num != 0:
        #apply regular monkhorst for non-hexagonal cells
        ks = Kpoints.automatic_density_by_vol(structure,kppvol=kdens,force_gamma=False)
        gflag = True
    else:
        print ('WARNING: your spacegroup cannot be detected - if you know you are using a hexagonal cell, your kmesh may not be gamma centered')

    # -------------------------------------------------------------
    # modify default materials project vasp input settings with,
    # dictionary update
    # -------------------------------------------------------------

    incar_settings = {
        "ISMEAR": 1,
        "SIGMA": 0.1
    }

    relax_input_set.user_incar_settings = incar_settings

    # -------------------------------------------------------------
    # modify default kpoints to our better ones
    # -------------------------------------------------------------

    relax_input_set.user_kpoints_settings = ks

    # -------------------------------------------------------------
    # write the inputs
    # -------------------------------------------------------------

    relax_input_set.write_input("run_%s" % file_prefix)



# -------------------------------------------------------------
# build or read in an atomic structure
# -------------------------------------------------------------
structs = get_prim_structs(['Zr']) # function outputs cif files


# -------------------------------------------------------------
# gather up the structure files and build inputs for them
# -------------------------------------------------------------
struct_files = glob.glob('*.cif')
for sfile in struct_files:
    if 'bcc' in sfile: #only look at bcc for this example
        atoms = read(sfile) # read in structure
        prefix = sfile.split('.')[0] # get name of file 
        a = np.linalg.norm(atoms.get_cell()[0]) # relaxed lattice parameter
        compress_expand(atoms, a, prefix = prefix, axes = [0,1,2], stepsize=0.03, nsteps = 3 )
        #glob up compressed and expanded files
        eos_files = glob.glob('*eos*cif')
        for eos_file in eos_files:
            eos_prefix = eos_file.split('.')[0]
            setup_calc_for_struct(eos_file)
            call('mv %s ./run_%s' % (eos_file,eos_prefix),shell = True)
        
