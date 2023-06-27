import sys
from ase import Atoms,Atom
from ase.io import read,write
from pymatgen.core import Structure
from pymatgen.io.vasp.inputs import Kpoints
from pymatgen.io.ase import *
from ase.data import atomic_numbers, atomic_names, atomic_masses, covalent_radii
import glob

# -------------------------------------------------------------
# build or read in an atomic structure
# -------------------------------------------------------------

ang_to_bohr = 1.8897259886

class QEInput:
    def __init__(self,structure):
        self.atoms = structure
        self.natoms = len(self.atoms)
        self.ntypes = len(set(self.atoms.symbols))
        self.control = {}
        self.system = {}
        self.ions = {}
        self.electrons = {}
        self.cell = {}        
        self.kpoints = {}
        self.pseudo_family = 'pseudo_dojo'
        self.spin_per_type = None
        self.default_settings(spin_polarized=True)
        self.conv_to_bohr = True
        self.set_cell_params()
        self.set_atomic_species()
        
    def generate_kpoints(self,density,ishex=False):
        structure = AseAtomsAdaptor.get_structure(self.atoms)
        if ishex:
            ks = Kpoints.automatic_density_by_vol(structure,kppvol=density,force_gamma=True)
            kpts = ks.kpts[0]
            #without shifting, we must set even kpoint meshes to odd so that 1 will be on gamma
            iseven = [ i %2 == 0 for i in kpts]
            for ikpt,kpt in enumerate(kpts):
                if iseven[ikpt]:
                    kpts[ikpt] += 1
                else:
                    continue
        else:
            ks = Kpoints.automatic_density_by_vol(structure,kppvol=density,force_gamma=False)
            kpts = ks.kpts[0]
        self.kpoints = kpts
        self.kpoints_shft = ks.kpts_shift
        self.set_atomic_positions()


    def set_spin_per_type(self,tind,spin=2.5):
        if self.spin_per_type == None:
            self.spin_per_type = {}
        self.spin_per_type[tind] = spin

    def set_cell_params(self):
        #CELL_PARAMETERS { alat | bohr | angstrom } 
        cell_vecs = self.atoms.get_cell().copy()
        cell_vecs = np.array(cell_vecs)
        if self.conv_to_bohr:
            cell_vecs *= ang_to_bohr
        self.cell_vecs = cell_vecs

    def set_atomic_species(self):
        specs = {}
        these_syms = list(set(self.atoms.symbols))
        for sym in these_syms:
            atomic_numberi = atomic_numbers[sym]
            massi = atomic_masses[atomic_numberi]
            spec = '  %s  %4.12f  %s\n' % (sym,massi,'%s.upf' %sym)
            specs[sym] = spec
        self.species = specs

    def set_atomic_positions(self,units ='crystal',freeze_atom_inds = []):
        #ATOMIC_POSITIONS { alat | bohr | angstrom | crystal | crystal_sg } 
        if units == 'crystal':
            input_pos = self.atoms.get_scaled_positions()
        elif units  == 'angstrom':
            input_pos = self.atoms.positions
        elif units  == 'bohr':
            input_pos = self.atoms.positions * ang_to_bohr
        else:
            raise ValueError("you cannot use crystal_sg or alat units yet")

        pos_strs = ['ATOMIC_POSITIONS %s\n' % units ]
        for i in range(self.natoms):
            posi = input_pos[i]
            sym = self.atoms.symbols[i]
            freeze_arr = [1,1,1]
            if i in freeze_atom_inds:
                freeze_arr = [0,0,0]
            qe_pos_str = "  %s    %4.12f   %4.12f   %4.12f  %d   %d   %d \n" % ( (sym,) + tuple(list(posi)) + tuple(freeze_arr))
            pos_strs.append(qe_pos_str)
        self.position_strs = pos_strs
        

    def default_settings(self,spin_polarized=True,randomize_spins = False,random_seed = 589123):
        self.control = {
        'calculation':'vc-relax',
        'etot_conv_thr':1.e-5,
        'forc_conv_thr':1.e-4,
        'tprnfor':'.true.',
        'outdir':'./out',
        'tstress':'.true.'
        }
        self.system = {'ecutwfc':60.0,
        'ecutrho' : 480.0,
        'ibrav' : 0,
        'nosym' : '.true.',
        'nat': self.natoms,
        'ntyp':self.ntypes,
        'nspin': 1,
        'occupations' : 'smearing',
        'smearing': 'mv',
        'degauss' : 0.01,
        }
        #sets up ferromagnetic ordering by default
        if randomize_spins:
            np.random.seed(random_seed)
            spin_samples = np.random.uniform(-1,1,self.ntypes)*2.5
        if spin_polarized:
            self.system['nspin'] = 2
            if self.spin_per_type == None:
                for typ in range(self.ntypes):
                    typind = typ + 1
                    if randomize_spins:
                        self.set_spin_per_type(typind,spin=spin_samples[typ])
                    else:
                        self.set_spin_per_type(typind,spin=2.5)

            for typ in range(self.ntypes):
                typind = typ + 1
                self.system['starting_magnetization(%d)' % typind] = self.spin_per_type[typind] 

        self.electrons = {
        'mixing_mode': 'TF',
        'conv_thr':1.E-6,
        }

        self.ions = {
        'ion_dynamics':'bfgs',
        'upscale': 1000,
        }

        self.cell = {
        'cell_dofree': 'all',
        'cell_dynamics': 'bfgs',
        }
    

    def kpoints_settings(self,kpoints, offset = (0,0,0), method='automatic'):
        #K_POINTS { tpiba | automatic | crystal | gamma | tpiba_b | crystal_b | tpiba_c | crystal_c } 
        if type(kpoints) == list or type(kpoints) == np.ndarray:
            kpoints = tuple(list(kpoints))
            kpoint_str = 'K_POINTS %s \n' % method
            kpoint_str += '  %d  %d  %d    %d  %d  %d\n' % (kpoints + tuple(offset))
        self.kpoint_input = kpoint_str


    def write_input(self,fname):
        strinp ="&CONTROL\n"
        for controlflag, controlval in self.control.items():
            if type(controlval) == str:
                if 'true' in controlval or 'false' in controlval:
                    stri = '  %s  =  %s, \n' % (controlflag, controlval)
                else:
                    stri = '  %s  =  "%s", \n' % (controlflag, controlval)
            elif type(controlval) == int:
                stri = '  %s  =  %d, \n' % (controlflag, controlval)
            elif type(controlval) == float:
                stri = '  %s  =  %4.12E, \n' % (controlflag, controlval)
                stri = stri.replace('E','D')
            else:
                stri = '  %s  =  %s, \n' % (controlflag, controlval) # try to treat anything else as a string
            strinp += stri
        strinp += '/\n'
        strinp += '\n&SYSTEM\n'
        for systemflag,systemval in self.system.items():
            if type(systemval) == str:
                if 'true' in systemval or 'false' in systemval:
                    stri = '  %s  =  %s, \n' % (systemflag, systemval)
                else:
                    stri = '  %s  =  "%s", \n' % (systemflag, systemval)
            elif type(systemval) == int:
                stri = '  %s  =  %d, \n' % (systemflag, systemval)
            elif type(systemval) == float:
                stri = '  %s  =  %4.12E, \n' % (systemflag, systemval)
                stri = stri.replace('E','D')
            else:
                stri = '  %s  =  %s, \n' % (systemflag, systemval) # try to treat anything else as a string
            strinp += stri

        strinp += '/\n'
        strinp += '\n&ELECTRONS\n'
        for electronsflag,electronsval in self.electrons.items():
            if type(electronsval) == str:
                if 'true' in electronsval or 'false' in electronsval:
                    stri = '  %s  =  %s, \n' % (electronsflag, electronsval)
                else:
                    stri = '  %s  =  "%s", \n' % (electronsflag, electronsval)
            elif type(electronsval) == int:
                stri = '  %s  =  %d, \n' % (electronsflag, electronsval)
            elif type(electronsval) == float:
                stri = '  %s  =  %4.12E, \n' % (electronsflag, electronsval)
                stri = stri.replace('E','D')
            else:
                stri = '  %s  =  %s, \n' % (electronsflag, electronsval) # try to treat anything else as a string
            strinp += stri

        strinp += '/\n'
        strinp += '\n&IONS\n'
        for ionsflag,ionsval in self.ions.items():
            if type(ionsval) == str:
                if 'true' in ionsval or 'false' in ionsval:
                    stri = '  %s  =  %s, \n' % (ionsflag, ionsval)
                else:
                    stri = '  %s  =  "%s", \n' % (ionsflag, ionsval)
            elif type(ionsval) == int:
                stri = '  %s  =  %d, \n' % (ionsflag, ionsval)
            elif type(ionsval) == float:
                stri = '  %s  =  %4.12E, \n' % (ionsflag, ionsval)
                stri = stri.replace('E','D')
            else:
                stri = '  %s  =  %s, \n' % (ionsflag, ionsval) # try to treat anything else as a string
            strinp += stri

        strinp += '/\n'
        strinp += '\n&CELL\n'
        for cellflag,cellval in self.cell.items():
            if type(cellval) == str:
                if 'true' in cellval and 'false' in cellval:
                    stri = '  %s  =  %s, \n' % (cellflag, cellval)
                else:
                    stri = '  %s  =  "%s", \n' % (cellflag, cellval)
            elif type(cellval) == int:
                stri = '  %s  =  %d, \n' % (cellflag, cellval)
            elif type(cellval) == float:
                stri = '  %s  =  %4.12E, \n' % (cellflag, cellval)
                stri = stri.replace('E','D')
            else:
                stri = '  %s  =  %s, \n' % (cellflag, cellval) # try to treat anything else as a string
            strinp += stri

        strinp += '/\n'
        strinp += '\nATOMIC_SPECIES\n'
        for spec, specstr in self.species.items():
            strinp += specstr

        strinp += '\n'
        for posstr in self.position_strs:
            strinp += posstr
        strinp += '\n'

        if self.conv_to_bohr:
            strinp += '\nCELL_PARAMETERS bohr\n'
        else:
            strinp += '\nCELL_PARAMETERS angstrom\n'

        for cellvec in self.cell_vecs:
            stri =  '  %4.12f  %4.12f  %4.12f\n' % tuple(list(cellvec))
            strinp += stri

        strinp += '\n'
        strinp += self.kpoint_input        

        with open(fname,'w') as writeout:
            writeout.write(strinp)
        #print (strinp)

# example usage:
#atoms = read('Zr_cubic_fcc_atoms.cif')
#qei = QEInput(atoms)
#qei.generate_kpoints(density=15)
#qei.kpoints_settings(qei.kpoints,qei.kpoints_shft)
#qei.default_settings(spin_polarized=True)
#qei.write_input('tmp.in')
