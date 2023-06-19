from ase import Atom
from ase.build import bulk
from ase.io import read,write
from icet import ClusterSpace
from icet.tools.structure_generation import (generate_sqs,
                                             generate_sqs_from_supercells,
                                             generate_sqs_by_enumeration,
                                             generate_target_structure)

from icet.input_output.logging_tools import set_log_config
set_log_config(level='INFO')

base_species = ["Mo", "Nb", "Ta", "Ti", "W"]
primitive_structure = bulk('W',cubic=False)
cs = ClusterSpace(primitive_structure, [6., 4.0], base_species)
print (cs)
def gen_sqs(ind,target_concentrations,cs=cs):
	primitive_structure = bulk('W',cubic=False)
	cubic_structure = bulk('W',cubic=True)
	base_species = ["Mo", "Nb", "Ta", "Ti", "W"]
	#HEAVY tungsten
	max_len = 64
	#conc_rest = {elm: 1/len(base_species) for elm in base_species}
	#target_concentrations = conc_rest.copy()
	print(target_concentrations)
	#sqs = generate_sqs(cluster_space=cs,
	sqs = generate_sqs_from_supercells(cluster_space=cs,
			   #max_size=10,
			  # n_steps=max_len * 500,
                           n_steps = 10000,
			   supercells= [primitive_structure*(3,3,3)],# cubic_structure*(2,2,2)],
			   target_concentrations=target_concentrations)
	write('sqs_%d.vasp' % ind,sqs)
	write('sqs_%d.cif' %ind,sqs)
	print('Cluster vector of generated structure:', cs.get_cluster_vector(sqs))
	del cs

target_concentrations_many = {
1: {'Mo': 5/27, 'Nb': 5/27, 'Ta': 5/27, 'Ti': 5/27, 'W': 7/27} ,
2: {'Mo': 4/27, 'Nb': 4/27, 'Ta': 4/27, 'Ti': 4/27, 'W': 11/27} ,
3: {'Mo': 4/27, 'Nb': 4/27, 'Ta': 4/27, 'Ti': 6/27, 'W': 9/27} ,
4: {'Mo': 4/27, 'Nb': 4/27, 'Ta': 6/27, 'Ti': 4/27, 'W': 9/27} ,
5: {'Mo': 4/27, 'Nb': 6/27, 'Ta': 4/27, 'Ti': 4/27, 'W': 9/27} ,
6: {'Mo': 6/27, 'Nb': 4/27, 'Ta': 4/27, 'Ti': 4/27, 'W': 9/27} ,
7: {'Mo': 2/27, 'Nb': 2/27, 'Ta': 2/27, 'Ti': 2/27, 'W': 19/27} ,
8: {'Mo': 2/27, 'Nb': 2/27, 'Ta': 2/27, 'Ti': 4/27, 'W': 17/27} ,
9: {'Mo': 2/27, 'Nb': 2/27, 'Ta': 4/27, 'Ti': 2/27, 'W': 17/27} ,
10: {'Mo': 2/27, 'Nb': 4/27, 'Ta': 2/27, 'Ti': 2/27, 'W': 17/27} ,
11: {'Mo': 4/27, 'Nb': 2/27, 'Ta': 2/27, 'Ti': 2/27, 'W': 17/27} ,
}

for tind,tconc in target_concentrations_many.items():
	gen_sqs(tind,tconc)	
