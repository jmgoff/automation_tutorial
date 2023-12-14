from ase.io import read,write
from ase import Atom,Atoms
from ase.build import bulk, fcc111, add_adsorbate
from ase.db import connect
from icet.tools import enumerate_structures
import numpy as np

class System_Enum:
    def __init__(self,base_species):
        self.a = None
        self.blocks = []
        self.crystal_structures = []
        self.lattice_bases = []
        self.stored_lattice = {'a':{}}
        self.base_species = base_species
        return None


    def set_crystal_structures(self,structs = ['bcc']):
        self.crystal_structures = structs

    def set_lattice_constant(self,a):
        if type(a) == float:
            self.a = [a]*len(self.crystal_structures)
        elif type(a) == list:
            self.a = a
        else:
            raise TypeError("cannot use type other than float or list for lattice constant(s)")

        return None

    def set_substitutional_blocks(self,blocks=None):
        assert len(self.crystal_structures) >= 1, "set crystal structures before defining substitutional blocks - default is 'fcc' "
        if blocks == None:
            blocks = [ [self.base_species] ] * len(self.crystal_structures)
        else:
            blocks = blocks
        self.blocks = blocks

    def enumerate_structures(self, min_int_mult, max_int_mult):
        all_structs = []
        assert self.a != None, "set_lattice_constant first, then do enumeration"
        assert self.blocks != None, "set_substitutuional_blocks first, then do structure enumeration"
        for icrystal,crystal in enumerate(self.crystal_structures):
            primitive = bulk(self.base_species[0] , crystal , a=self.a[icrystal] , cubic=False)
            print ('generating structures for crystal: %s' % crystal)
            enumerated = enumerate_structures(primitive, range(min_int_mult, max_int_mult), self.blocks[icrystal])
            sublist = [ i for i in enumerated ]
            self.stored_lattice['a'][crystal] = self.a[icrystal]
            all_structs.append(sublist)
        se.all_structs = all_structs
        return all_structs


    def compress_expand(self,axes = [0,1,2],stepsize=0.01, nsteps = 2 ):
        chem_lst = ['%s']*len(self.base_species)
        chem_str = '-'.join(b for b in chem_lst) % tuple(self.base_species)
        compressed_expanded = {icrystal: {istrct: [] for istrct in range(len(self.all_structs[icrystal])) } for icrystal in range(len(self.crystal_structures)) }
        for icrystal,crystal in enumerate(self.crystal_structures):
            unique_labelings=self.all_structs[icrystal]
            this_a = self.stored_lattice['a'][crystal]
            this_stepsize = stepsize*this_a
            steps_up = np.linspace(this_a, this_a + (this_stepsize*nsteps), nsteps )
            steps_above = steps_up[1:]
            steps_down = np.linspace(this_a - (this_stepsize*nsteps), this_a, nsteps + 1 )
            steps_below = steps_down[:-1]
            all_steps = np.append(steps_below,steps_above)
            for istrct,strct in enumerate(unique_labelings):
                cell = strct.get_cell()
                scaled_pos = strct.get_scaled_positions()
                for istep in all_steps:
                    new_atoms = Atoms(strct.symbols)
                    new_cell = cell.copy()
                    for axis in axes:
                        new_cell[axis] +=  cell[axis] - istep
                    new_atoms.set_cell(new_cell)
                    new_atoms.set_scaled_positions(scaled_pos)
                    new_atoms.set_pbc(True)
                    compressed_expanded[icrystal][istrct].append(new_atoms)
                    #write('ats_%s_%s_%1.3f_%d.cif' % (chem_str,crystal,istep,istrct)  , new_atoms)
                    write('ats_%s_%s_%1.3f_%d.cif' % (chem_str,crystal,istep,istrct)  , new_atoms)

import os
from subprocess import call
import itertools
#base_species = ['Cr','Fe','Si','V']
#base_species_pairs = [['Cr', 'Fe'],
#['Cr', 'Si'],
#['Cr', 'V'],
#['Fe', 'Si'],
#['Fe', 'V'],
#['Si', 'V']
#]
base_species_pairs = [list(p) for p in itertools.combinations(['Cr','Fe','Si','V'],2)]
cellmaxmult = 4
for base_species in base_species_pairs:
    if not os.path.isdir('cmpex_%s%s_DSS_%d' % (tuple(base_species) + tuple([cellmaxmult]) ) ):
        os.mkdir('cmpex_%s%s_DSS_%d' % (tuple(base_species) + tuple([cellmaxmult]) ))
    os.chdir('cmpex_%s%s_DSS_%d' % (tuple(base_species) + tuple([cellmaxmult]) ))
    se = System_Enum(base_species)
    crystal_structures = ['bcc']
    se.set_crystal_structures(crystal_structures)
    se.set_lattice_constant([2.97])
    se.set_substitutional_blocks([base_species,base_species])
    astrcts = se.enumerate_structures(1,cellmaxmult+1)

    for icrystal,crystal in enumerate(crystal_structures):
        strcts = astrcts[icrystal]
        for istrct , strct in enumerate(strcts):
            chem_lst = ['%s']*len(base_species)
            chem_str = '-'.join(b for b in chem_lst) % tuple(base_species)
            write('ats_%s_%s_%d.cif' % (chem_str,crystal,istrct)  , strct)
            
    se.compress_expand(axes = [0,1,2],stepsize=0.03, nsteps = 2 )
    os.chdir('..')
