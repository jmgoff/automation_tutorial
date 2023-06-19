from pymatgen.core import Structure
from pymatgen.io.vasp.sets import MPStaticSet, MPRelaxSet, MPNonSCFSet
#from pymatgen.io.vasp.inputs import Kpoints
from pymatgen.io.vasp.inputs import *
from pymatgen.io.ase import *
from crystal_enum import *
import glob

# -------------------------------------------------------------
# build or read in an atomic structure
# -------------------------------------------------------------
structs = get_prim_structs(['Zr']) # function outputs cif files
struct_files = glob.glob('*.cif')
print (struct_files)
s1 = struct_files[0]
file_prefix = s1.split('.')[0]
structure = Structure.from_file(s1)

atoms = AseAtomsAdaptor.get_atoms(structure)
#s = AseAtomsAdaptor.get_structure(atoms)

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
#relax_input_set.modify_incar(incar_settings)
relax_input_set.user_incar_settings = incar_settings

#kpoints_settings = {
#    "kpoints": 1000
#}
#input_set.modify_kpoints(kpoints_settings)
#relax_input_set.Kpoints = Kpoints.automatic_density_by_vol(structure,kppvol=kdens,force_gamma=False)
relax_input_set.user_kpoints_settings = ks

#relax_input_set = MPRelaxSet(structure)
relax_input_set.write_input("run_%s" % file_prefix)

