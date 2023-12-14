from config_tool import *
rytoev = 13.6057039763
rypau3_to_gpa = 29421.02648438959 / 2
autoAA = 0.529177249
giga = 1.e9
from ase.io import iread,write
ryperau_to_evperAA = rytoev*autoAA
ev_2_gpa = 160.21766208
evstress_to_Pa=ev_2_gpa*giga
Pastress_to_bar = 1/(100000)

def flines_to_forces(lines):
    forces = []
    for line in lines:
        l = line.split()
        f = [float(l[-3])*ryperau_to_evperAA,float(l[-2])*ryperau_to_evperAA,float(l[-1])*ryperau_to_evperAA]
        forces.append(f)
    return forces

def slines_to_stresses(lines):
    stresses = []
    for line in lines:
        l = line.split()
        s = [float(l[0])*1,float(l[1])*1,float(l[2])*1]
        stresses.append(s)
    return stresses

def parse_stresses(outfile,infile,trajectory_index=None):
    try:
        base_atoms = read(outfile)
    except TypeError:
        base_atoms = read(infile,format='espresso-in')
    #NOTE this assumes that no extra force contributions are made (e.g through external packages like environ)
    with open(outfile,'r') as readin:
        lines = readin.readlines()
        #flines = [line for line in lines if 'force' in line and 'cont' not in line and 'conv' not in line and 'corr' not in line and 'CPU' not in line and 'crit' not in line and 'Dyn' not in line]
        flineinds = [lineid for lineid,line in enumerate(lines) if 'total   stress' in line]
        fsteps = {flineind:lines[flineind +1: flineind+1+3] for flineind in flineinds }
        sperstep = {flineind:slines_to_stresses(fsteps[flineind]) for flineind in flineinds}
    if trajectory_index != None:
        stresses = sperstep[flineinds[trajectory_index]]
        return stresses
    else:
        return list(sperstep.values())

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
stresses_traj = parse_stresses(myoutfile,myinfile)
energy_traj = parse_energies(myoutfile)


try:
    atoms_traj = [ati for ati in iread(myoutfile,format='espresso-out') ]
    print (len(atoms_traj))
except TypeError:
    atoms = read(myinfile,format='espresso-in')

for traj_ind, energy in enumerate(energy_traj):
    stresses = stresses_traj[traj_ind]
    atoms = atoms_traj[traj_ind]
    cell = atoms.get_cell() #[(1,0,0),(0,1,0)...]

    forces = forces_traj[traj_ind]
    print ('NOTE', forces, ' if all of your forces are zero, you may need to turn off symmetry! (set nosym = .true. in your quantum espresso input) unless you only have one atom')
    input_stresses = np.array(stresses)*rypau3_to_gpa*giga*Pastress_to_bar
    input_stresses = input_stresses.tolist()
    datadct = {'Forces':forces,
    'Energy':energy,
    'Stress':input_stresses,
    }
    
    fsats = fsnap_atoms()
    fsats.set_ASE(atoms,**datadct)
    fsats.write_JSON(ex_json_prefix + '_%d' % traj_ind,write_header=False)
    if traj_ind == len(energy_traj) -1:
        write('%s.cif' % ex_json_prefix,atoms)
