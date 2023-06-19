from config_tool import *
rytoev = 13.6057039763
autoAA = 0.529177249
from ase.io import iread,write
#Ry/au * (au/AA) * (eV/Ry) = (eV/AA)
ryperau_to_evperAA = rytoev*autoAA

def flines_to_forces(lines):
    forces = []
    for line in lines:
        l = line.split()
        f = [float(l[-3])*ryperau_to_evperAA,float(l[-2])*ryperau_to_evperAA,float(l[-1])*ryperau_to_evperAA]
        forces.append(f)
    return forces

def parse_forces(outfile,infile,trajectory_index=None):
    try:
        base_atoms = read(outfile)
    except TypeError:
        base_atoms = read(infile,format='espresso-in')
    #NOTE this assumes that no extra force contributions are made (e.g through external packages like environ)
    with open(outfile,'r') as readin:
        lines = readin.readlines()
        #flines = [line for line in lines if 'force' in line and 'cont' not in line and 'conv' not in line and 'corr' not in line and 'CPU' not in line and 'crit' not in line and 'Dyn' not in line]
        flineinds = [lineid for lineid,line in enumerate(lines) if 'Forces acting on atoms' in line]
        fsteps = {flineind:lines[flineind +2: flineind+2 +len(base_atoms)] for flineind in flineinds }
        fperstep = {flineind:flines_to_forces(fsteps[flineind]) for flineind in flineinds}
        print(fperstep)

    if trajectory_index != None:
        forces = fperstep[flineinds[trajectory_index]]
        return forces
    else:
        return list(fperstep.values())

def parse_energies(outfile,trajectory_index=None):
    with open(outfile,'r') as readin:
        lines = readin.readlines()
        enlines = [line for line in lines if '!' in line]
        ens = [float(enline.split()[-2])*rytoev for enline in enlines]
    if trajectory_index != None:
        return ens[trajectory_index]
    else:
        return ens

myoutfile = 'Ni_cubic_fcc_atoms.out' # output from quantum espresso
myinfile = 'Ni_cubic_fcc_atoms.in' # input for quantum espresso
ex_json_prefix = 'Ni_cubic_fcc_atoms_rlx' # prefix for json file 
forces_traj = parse_forces(myoutfile,myinfile)
energy_traj = parse_energies(myoutfile)

#print ('NOTE', energy_traj[0],' is not referenced!, consider subtracting a reference state energy from each value (e.g. the energy of an isolated atom)')
#reffed_energy = energy[0] - (len(atoms) * eref) # for example if eref is the energy of an isolated atom
print ('NOTE', forces_traj[0], ' if all of your forces are zero, you may need to turn off symmetry! (set nosym = .true. in your quantum espresso input)')

try:
    atoms_traj = [ati for ati in iread(myoutfile,format='espresso-out') ]
    print (len(atoms_traj))
except TypeError:
    atoms = read(myinfile,format='espresso-in')

for traj_ind, energy in enumerate(energy_traj):
    forces = forces_traj[traj_ind]
    atoms = atoms_traj[traj_ind] 
    datadct = {'Forces':forces,
    'Energy':energy
    }
    
    fsats = fsnap_atoms()
    fsats.set_ASE(atoms,**datadct)
    fsats.write_JSON(ex_json_prefix + '_%d' % traj_ind,write_header=False)
    if traj_ind == len(energy_traj) -1:
        write('%s.cif' % ex_json_prefix,atoms)
