import glob
import os
from crystal_enum import *
from qe_tools import *
from subprocess import call
import time

get_prim_structs(['V'])

struct_files = glob.glob('*.cif')
for fileindex,sfile in enumerate(struct_files):
    atoms = read(sfile)
    prefix = sfile.split('.')[0]
    qei = QEInput(atoms)
    ishex = False
    if 'hex' in prefix:
        ishex = True
    qei.generate_kpoints(density=45,ishex=ishex)
    qei.kpoints_settings(qei.kpoints,qei.kpoints_shft)
    qei.default_settings(spin_polarized=True)
    qei.system['ecutwfc']=80.0
    qei.system['ecutrho']=320.0    
    qei.electrons['scf_must_converge']= '.true.'
    dirname = 'relax_%s' % prefix
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    qei.write_input('./%s/%s.in' % (dirname, prefix))
    time.sleep(0.5)
    call('cp %s ./%s' % (sfile,dirname),shell = True)
