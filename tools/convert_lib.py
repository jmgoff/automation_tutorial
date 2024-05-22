from config_tool import *
rytoev = 13.6057039763
rypau3_to_gpa = 29421.02648438959 / 2
autoAA = 0.529177249
giga = 1.e9
from ase.io import iread,write
#Ry/au * (au/AA) * (eV/Ry) = (eV/AA)
#Ry/au^2  * (au/AA) *(au/AA) * (eV/Ry) = eV/AA
ryperau_to_evperAA = rytoev*autoAA
ev_2_gpa = 160.21766208
evstress_to_Pa=ev_2_gpa*giga
Pastress_to_bar = 1/(100000)

def get_natoms(lines):
    data_lines = [line for line in lines if 'number of atoms' in line]
    data_line = data_lines[0]
    return int(data_line.split()[-1])

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

def parse_stresses(outfile,infile=None,trajectory_index=None):
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

def parse_forces(outfile,infile=None,trajectory_index=None):
    try:
        base_atoms = read(outfile)
    except TypeError:
        if infile != None:
            base_atoms = read(infile,format='espresso-in')
        else:
            base_atoms = None
    #NOTE this assumes that no extra force contributions are made (e.g through external packages like environ)
    with open(outfile,'r') as readin:
        lines = readin.readlines()
        if infile != None:
            natoms = len(base_atoms)
        elif infile == None:
            natoms = get_natoms(lines)
        flineinds = [lineid for lineid,line in enumerate(lines) if 'Forces acting on atoms' in line]
        fsteps = {flineind:lines[flineind +2: flineind+2 + natoms] for flineind in flineinds }
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

def process_QE(myoutfile, ex_json_prefix,energy_references=None, myinfile=None, parse_QE_forces=True, parse_QE_stresses = True):
    """
    myoutfile: (string) # output file name  from quantum espresso
    myinfile: (string) # input file name  from quantum espresso
    ex_json_prefix: (string) # prefix for json file 
    energy_references: (dict) # dictionary of reference energies (in eV/atom) for each element in your structure
    parse_QE_forces: (logical) # flag to parse hellmann-feynman forces from QE output
    parse_QE_stresses: (logical) # flag to parse stresses from QE output
    """
    #Build list of forces, stresses, and energies for each trajectory (minimization) step

    atoms_traj = []
    try:
        atoms_traj = [ati for ati in iread(myoutfile,format='espresso-out') ]
        atoms = atoms_traj[0]
    except (TypeError,AssertionError):
        if myinfile != None:
            atoms = read(myinfile,format='espresso-in')
            if len(atoms_traj) == 0:
                atoms_traj.append(atoms)
        else:
            try:
                atoms = iread(myoutfile,format='espresso-out')[0]
            except TypeError:
                raise AttributeError('Your atom trajectory from file %s has no atoms and no supplementary input file has been supplied. \\Either supply the QE input file to define the initial structure [this will be needed for SCF calculations] \\or ensure that your vc-relax/relax calculation completes at least one full ion iteration' % myoutfile)

    atsyms = list(atoms.symbols)
    utypes = list(set(atsyms))
    type_counts = {utype:atsyms.count(utype) for utype in utypes}
    if energy_references == None:
        print ('WARNING no reference energies supplied - you the energy of your \\ fitsnap structure will be calculated with the following reference energies subtracted %s' % ( ' '.join([' %s=0.0']*len(utypes)) % tuple(utypes) ))
        energy_references = {utype:0.0 for utype in utypes}
    elif energy_references != None:
        supplied_types = list(energy_references.keys())
        flag1 = tuple(sorted(utypes)) == tuple(sorted(supplied_types))
        flag2 = all([utypei in supplied_types for utypei in utypes])
        assert flag1 or flag2, "your reference energies must be supplied for all atoms in your QE calculation"
        

    energy_traj = parse_energies(myoutfile)
    traj_len = len(energy_traj)
    if parse_QE_forces:
        forces_traj = parse_forces(myoutfile,myinfile)
    elif not parse_QE_forces:
        forces_traj = [list(np.zeros((len(atoms_traj[0]),3)))]* traj_len
    if parse_QE_stresses:
        stresses_traj = parse_stresses(myoutfile,myinfile)
    elif not parse_QE_stresses:
        stresses_traj = [list(np.zeros((3,3)))]*traj_len

    if len(energy_traj) == (len(atoms_traj)-1):
        atoms_traj = atoms_traj[:-1]

    assert len(energy_traj) == len(atoms_traj), "energy trajectory with %d entries and atoms with %d entries" % (len(energy_traj),len(atoms_traj))
    for traj_ind, energy in enumerate(energy_traj):
        stresses = stresses_traj[traj_ind]
        atoms = atoms_traj[traj_ind]
        cell = atoms.get_cell() #[(1,0,0),(0,1,0)...]

        if len(atoms) == 1:
            forces = [[0.0,0.0,0.0]]
        else:
            try:
                forces = forces_traj[traj_ind]
            except IndexError:
                forces = [[0.0,0.0,0.0]]*len(atoms)
        zero_force_flags = [all([fi == 0.0 for fi in forci]) for forci in forces]
        if all(zero_force_flags) and len(forces) > 1:
            print ('NOTE', forces, ' if all of your forces are zero (and it is not a single-atom structure), you may need to turn off symmetry! (set nosym = .true. in your quantum espresso input)')
        eref = np.sum([type_counts[utypei]* energy_references[utypei] for utypei in utypes])
        #type_counts = {utype:atoms.symbols.copy().count(utype) for utype in utypes}
        input_stresses = np.array(stresses)*rypau3_to_gpa*giga*Pastress_to_bar
        input_stresses = input_stresses.tolist()
        datadct = {'Forces':forces,
        'Energy':energy-eref,
        'Stress':input_stresses,
        }
        
        fsats = fsnap_atoms()
        fsats.set_ASE(atoms,**datadct)
        fsats.write_JSON(ex_json_prefix + '_%d' % traj_ind,write_header=False)
        # uncomment to write cif file for visualization in VESTA or other.
        #if traj_ind == len(energy_traj) -1:
        #    write('%s.cif' % ex_json_prefix,atoms)
