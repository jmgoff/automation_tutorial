from subprocess import call

def parse_results():
    call("""grep "'*ALL', 'Unweighted', 'Training', 'Energy'" ./*/*.md | awk '{print $(NF-3)}' > energy_rmse.txt """,shell=True)
    call("""grep "'*ALL', 'Unweighted', 'Training', 'Force'" ./*/*.md | awk '{print $(NF-3)}' > force_rmse.txt """,shell=True)
    return None
parse_results()

energies = []
with open('energy_rmse.txt','r') as readenergy:
    enlines = readenergy.readlines()
    for line in enlines:
        l = line.split()
        energies.append(float(l[0]))

forces = []
with open('force_rmse.txt','r') as readforce:
    frclines = readforce.readlines()
    for line in frclines:
        l = line.split()
        forces.append(float(l[0]))

for ien, enerr in enumerate(energies):
    frcerr = forces[ien]
    print ('sample_%03d'%ien, enerr + frcerr)
