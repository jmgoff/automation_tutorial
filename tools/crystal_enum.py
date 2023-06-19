from ase.io import read,write
import spglib as spg
from ase.lattice.cubic import *
from ase.lattice.tetragonal import *
from ase.lattice.orthorhombic import *
from ase.lattice.monoclinic import *
from ase.lattice.triclinic import *
from ase.lattice.hexagonal import *
from ase.neighborlist import *
from ase.build import bulk
from ase import Atoms,Atom


class DiamondFactory(FaceCenteredCubicFactory):
    """A factory for creating diamond lattices."""
    xtal_name = 'diamond'
    bravais_basis = [[0, 0, 0], [0.25, 0.25, 0.25]]
Diamond = DiamondFactory()

class GraphiteFactory(GraphiteFactory):
	bravais_basis=[[0, 0, 0], [0.5, 0.5, 0.5]]
Graphite = GraphiteFactory()

def optimal_bond_to_latparam(optimal_bond_length,atoms,lattice_params,tol=0.15):
	verbose = False
	#ideal reference would be fcc Cu while finding optimal starting lattice parameters for simple cubic Cu
	tst_atoms = atoms.copy()
	natural_cutoff = max([ optimal_bond_length, np.average(natural_cutoffs(atoms))])
	atinds = [atom.index for atom in atoms]
	at_dists = {i:[] for i in atinds}
	all_dists = []
	nl = primitive_neighbor_list('ijdD',pbc=tst_atoms.pbc,positions=tst_atoms.positions ,cell=tst_atoms.get_cell(),cutoff=natural_cutoff)
	for i,j in zip(nl[0],nl[-1]):
		at_dists[i].append(j)
		all_dists.append(j)
	if len(all_dists) == 0:
		current_bond_length = 1.2 * optimal_bond_length
	else:
		current_bond_length = np.average(all_dists)
	while current_bond_length > optimal_bond_length + tol:
		if current_bond_length > optimal_bond_length + tol:
			cell = tst_atoms.get_cell()
			cell_vec_sizes = [np.linalg.norm(v) for v in cell]
			mx = max(cell_vec_sizes)
			mx_ind = cell_vec_sizes.index(mx)
			isize = cell_vec_sizes[mx_ind]
			iratio = optimal_bond_length/isize
			istep = (  iratio * 0.2 ) #1/5 th of the size
			assert istep < 1., "check your step size %f" % istep
			new_cell = (1 - istep) * cell
			tst_atoms.set_cell(new_cell)
		elif current_bond_length < optimal_bond_length - tol:
			cell = tst_atoms.get_cell()
			cell_vec_sizes = [np.linalg.norm(v) for v in cell]
			mx = max(cell_vec_sizes)
			mx_ind = cell_vec_sizes.index(mx)
			isize = cell_vec_sizes[mx_ind]
			iratio = optimal_bond_length/isize
			istep = (  iratio * 0.2 ) #1/5 th of the size
			assert istep < 1., "check your step size %f" % istep
			new_cell = (1 + istep) * cell
			tst_atoms.set_cell(new_cell)
		if verbose:
			print ('istep',istep,current_bond_length, optimal_bond_length,tst_atoms.get_cell())
		nl = primitive_neighbor_list('ijdD',pbc=tst_atoms.pbc,positions=tst_atoms.positions ,cell=tst_atoms.get_cell(),cutoff=natural_cutoff)
		if len(nl[-1]) == 0:
			current_bond_length = optimal_bond_length * 1.2
		else:
			current_bond_length = np.average(nl[-1])
	
	return tst_atoms

def get_cell_type(atoms):
	cell = atoms.get_cell()
	scpos = atoms.get_scaled_positions()
	numbers = atoms.numbers
	spgcell = (cell,scpos,numbers)
	spacegroup = spg.get_spacegroup(spgcell, symprec=1e-5, angle_tolerance=-1.0, symbol_type=0)

	spacegroup_to_tuple = {
'Pm-3m (221)' : ('cubic','sc'),
'Im-3m (229)' : ('cubic','bcc'),
'Fm-3m (225)' : ('cubic','fcc'),
'R-3m (166)' : ('cubic','diamond'),
'Fd-3m (227)' : ('cubic','diamond'),
'P4/mmm (123)' : ('tetragonal','st'),
'I4/mmm (139)' : ('tetragonal','ct'),
'Pmmm (47)' : ('orthorhombic','so'),
'Cmmm (65)' : ('orthorhombic','baco'),
'Fmmm (69)' : ('orthorhombic','fco'),
'Immm (71)' : ('orthorhombic','boco'),
'P2/m (10)' : ('monoclinic','sm'),
'C2/m (12)' : ('monoclinic','bcm'),
'P-1 (2)' : ('triclinic','t'),
'P6/mmm (191)' : ('hexagonal','h'),
'P6_3/mmc (194)' : ('hexagonal','hcp'),
'P6_3/mmc (194)' : ('hexagonal','hgr')
	}
	return spacegroup_to_tuple[spacegroup]

def get_primitive_cell(atoms):
	cell = atoms.get_cell()
	scpos = atoms.get_scaled_positions()
	numbers = atoms.numbers
	spgcell = (cell,scpos,numbers)
	symmetry = spg.get_symmetry(spgcell, symprec=1e-5)
	lattice, scaled_positions, numbers = spg.standardize_cell(spgcell, to_primitive=True, no_idealize=False, symprec=1e-5)
	new_prim = Atoms(numbers)
	new_prim.set_cell(lattice)
	new_prim.set_scaled_positions(scaled_positions)
	new_prim.set_pbc(True)
	return new_prim

allowed_lattice_params = {
('cubic','sc'):[('a',)],
 ('cubic','bcc'):[('a',)],
 ('cubic','fcc'):[('a',)],
 ('cubic','diamond'):[('a',)],
 ('tetragonal','st'):[('a','c/a')],
 ('tetragonal','ct'):[('a','c/a')],
 ('orthorhombic','so'):[('a','b/a','c/a')],
 ('orthorhombic','baco'):[('a','b/a','c/a')],
 ('orthorhombic','fco'):[('a','b/a','c/a')],
 ('orthorhombic','boco'):[('a','b/a','c/a')],
 ('monoclinic','sm'):[('a', 'b/a', 'c/a', 'alpha')],
 ('monoclinic','bcm'):[('a', 'b/a', 'c/a', 'alpha')],
 ('triclinic','t'):[('a', 'b/a', 'c/a', 'alpha', 'beta', 'gamma')],
 ('hexagonal','h'):[('a','c/a')],
 ('hexagonal','hcp'):[('a','c/a')],
 ('hexagonal','hgr'):[('a','c/a')]
}

lattice_params_schema = {
 ('cubic','sc'):2.0,#{'a':2.0},
 ('cubic','bcc'):4.0,#{'a':4.0},
 ('cubic','fcc'):4.0,#{'a':4.0},
 ('cubic','diamond'):4.0,#{'a':4.0},
 ('tetragonal','st'):{'a':4.0,'c/a':4/3},
 ('tetragonal','ct'):{'a':3.0,'c/a':4/3},
 ('orthorhombic','so'):{'a':2.0, 'b/a':1.2, 'c/a':1.3},
 ('orthorhombic','baco'):{'a':4.0, 'b/a':1.2, 'c/a':1.3},
 ('orthorhombic','fco'):{'a':4.0, 'b/a':1.2, 'c/a':1.3},
 ('orthorhombic','boco'):{'a':4.0, 'b/a':1.2, 'c/a':1.3},
 ('monoclinic','sm'):{'a':4.0, 'b/a':1.2, 'c/a':1.3, 'alpha':70 },
 ('monoclinic','bcm'):{'a':4.0, 'b/a':1.2, 'c/a':1.3, 'alpha':70 },
 ('triclinic','t'):{'a':4.0, 'b/a':1.2, 'c/a':1.3, 'alpha':70., 'beta':40., 'gamma':100. },
 ('hexagonal','h'):{'a':2.0,'c/a':1.5},
 ('hexagonal','hcp'):{'a':2.0,'c/a':0.75},
 ('hexagonal','hgr'): {'a':2.0,'c/a':1.5},
}


def lattice_func(pltup):
	valid_tups = [ ('cubic','sc'),
 ('cubic','bcc'),
 ('cubic','fcc'),
 ('cubic','diamond'),
 ('tetragonal','st'),
 ('tetragonal','ct'),
 ('orthorhombic','so'),
 ('orthorhombic','baco'),
 ('orthorhombic','fco'),
 ('orthorhombic','boco'),
 ('monoclinic','sm'),
 ('monoclinic','bcm'),
 ('triclinic','t'),
 ('hexagonal','h'),
 ('hexagonal','hcp'),
 ('hexagonal','hgr')]
	all_tup_str = ' '.join( '("%s" , "%s")'%B for B in valid_tups)
	assert pltup in valid_tups, "(%s,%s) is not a valid structure tuple, please enter one of the following: %s" % (pltup + (all_tup_str,))
	# cubic structures
	if pltup == ('cubic','sc'):
		return SimpleCubic
	elif pltup == ('cubic','bcc'):
		return BodyCenteredCubic
	elif pltup == ('cubic','fcc'):
		return FaceCenteredCubic
	elif pltup == ('cubic','diamond'):
		return Diamond
	# tetragonal structures
	elif pltup == ('tetragonal','st'):
		return SimpleTetragonal
	elif pltup == ('tetragonal','ct'):
		return CenteredTetragonal
	# orthorhombic structures
	elif pltup == ('orthorhombic','so'):
		return SimpleOrthorhombic
	elif pltup == ('orthorhombic','baco'):
		return BaseCenteredOrthorhombic
	elif pltup == ('orthorhombic','fco'):
		return FaceCenteredOrthorhombic
	elif pltup == ('orthorhombic','boco'):
		return BodyCenteredOrthorhombic
	# monoclinic structures
	elif pltup == ('monoclinic','sm'):
		return SimpleMonoclinic
	elif pltup == ('monoclinic','bcm'):
		return BaseCenteredMonoclinic
	# triclinic structure
	elif pltup == ('triclinic','t'):
		return Triclinic
	# hexagonal structures
	elif pltup == ('hexagonal','h'):
		return Hexagonal
	elif pltup == ('hexagonal','hcp'):
		return HexagonalClosedPacked
	elif pltup == ('hexagonal','hgr'):
		return Graphite



valid_tups = [ ('cubic','sc'),
 ('cubic','bcc'),
 ('cubic','fcc'),
 ('cubic','diamond'),
 ('tetragonal','st'),
 ('tetragonal','ct'),
 ('orthorhombic','so'),
 ('orthorhombic','baco'),
 ('orthorhombic','fco'),
 ('orthorhombic','boco'),
 ('monoclinic','sm'),
 ('monoclinic','bcm'),
 ('triclinic','t'),
 ('hexagonal','h'),
 ('hexagonal','hcp')
]


elem_list = [
'C','Si',
'Fe','Co','Ni','Cu','Zn',
'Zr','Nb','Mo',
'Ru','Pd','Ag' ,
'Hf','Ta','W',
'Ir','Pt','Au',
]

def get_prim_structs(elem_list):
    for elem in elem_list:
	    atis = bulk(elem)
	    suggested_bond_len = 2*np.average(natural_cutoffs(atis))
	    print (elem,get_cell_type(atis),suggested_bond_len)
	    for tup in valid_tups:
		    this_func = lattice_func(tup)
		    atoms =this_func(size=(1,1,1), symbol=elem, pbc=(1,1,1), latticeconstant=lattice_params_schema[tup])
		    prim_atoms = get_primitive_cell(atoms)
		    starting_atoms = optimal_bond_to_latparam(optimal_bond_length=suggested_bond_len,atoms=prim_atoms,lattice_params=None,tol=0.05)
		    write('%s_%s_%s_atoms.cif' % (elem, tup[0],tup[1]),starting_atoms)

def compress_expand(strct, a, prefix=None, axes = [0,1,2],stepsize=0.03, nsteps = 2 ):
    this_a = a # lattice constant
    compressed_expanded = {}
    steps_up = np.linspace(this_a, this_a + (stepsize*nsteps), nsteps )
    steps_above = steps_up[1:]
    steps_down = np.linspace(this_a - (stepsize*nsteps), this_a, nsteps + 1 )
    steps_below = steps_down[:-1]
    all_steps = np.append(steps_below,steps_above)

    cell = strct.get_cell()
    scaled_pos = strct.get_scaled_positions()
    for stepind,istep in enumerate(all_steps):
        new_atoms = Atoms(strct.symbols)
        new_cell = cell.copy()
        for axis in axes:
            new_cell[axis] +=  cell[axis] - istep
        new_atoms.set_cell(new_cell)
        new_atoms.set_scaled_positions(scaled_pos)
        new_atoms.set_pbc(True)
        #compressed_expanded[icrystal][istrct].append(new_atoms)
        if prefix == None:
            prefix_out = 'eos_%d' % stepind
        else:
            prefix_out = prefix + '_eos_%d' % stepind
        write('%s.cif' % prefix_out  , new_atoms)

