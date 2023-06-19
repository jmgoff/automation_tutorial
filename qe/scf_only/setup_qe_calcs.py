import glob
import os
from crystal_enum import *
from qe_tools import *
from subprocess import call

get_prim_structs(['Ni'])


struct_files = glob.glob('*.cif')
for fileindex,sfile in enumerate(struct_files):
    atoms = read(sfile)
    prefix = sfile.split('.')[0]
    qei = QEInput(atoms)
    ishex = False
    if 'hex' in prefix:
        ishex = True
    qei.generate_kpoints(density=11,ishex=ishex)
    qei.kpoints_settings(qei.kpoints,qei.kpoints_shft)
    qei.default_settings(spin_polarized=True)

    qei.control['calculation'] = 'scf' # change from default cell relaxation to single scf (energy calculation)
    qei.electrons['conv_thr'] = 1.E-9 # conv_thr scales with # of electrons. must be more stringent for small systems!

    dirname = 'run_%03d' % fileindex
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    qei.write_input('./%s/%s.in' % (dirname, prefix))
    call('cp %s ./%s' % (sfile,dirname),shell = True)
