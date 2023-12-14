from config_tool import *
rytoev = 13.6057039763
autoAA = 0.529177249

#Ry/au * (au/AA) * (eV/Ry) = (eV/AA)
ryperau_to_evperAA = rytoev*autoAA

def flines_to_forces(lines):
    forces = []
    for line in lines:
        l = line.split()
        f = [float(l[-3])*ryperau_to_evperAA,float(l[-2])*ryperau_to_evperAA,float(l[-1])*ryperau_to_evperAA]
        forces.append(f)
    return forces

def parse_forces(outfile,infile,trajectory_index=-1):
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

    forces = fperstep[flineinds[trajectory_index]]
    return forces

def parse_energies(outfile,trajectory_index=-1):
    with open(outfile,'r') as readin:
        lines = readin.readlines()
        enlines = [line for line in lines if '!' in line]
        ens = [float(enline.split()[-2])*rytoev for enline in enlines]
    return ens[trajectory_index]

myoutfile = 'elasticFCC3.out' # output from quantum espresso
myinfile = 'elasticFCC3.in' # input for quantum espresso
ex_json_prefix = 'test_4' # prefix for json file 
forces = parse_forces(myoutfile,myinfile)
energy = parse_energies(myoutfile)

print ('NOTE', energy,' is not referenced!, consider subtracting a reference state energy from each value (e.g. the energy of an isolated atom)')
#reffed_energy = energy[0] - (len(atoms) * eref) # for example if eref is the energy of an isolated atom
print ('NOTE', forces, ' if all of your forces are zero, you may need to turn off symmetry! (set nosym = .true. in your quantum espresso input)')
datadct = {'Forces':forces,
'Energy':energy
}

try:
    atoms = read(myoutfile)
except TypeError:
    atoms = read(myinfile,format='espresso-in')
fsats = fsnap_atoms()
fsats.set_ASE(atoms,**datadct)
fsats.write_JSON(ex_json_prefix,write_header=False)
