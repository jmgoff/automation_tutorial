import os
from hyperparam_tools import *

#---------------------------------------------------------------
# example for Latin Hypercube Sampling of some SNAP hyperparams
#---------------------------------------------------------------


#define a function that will help us set up input
# files with different settings
#NOTE improvement with FitSNAP library mode!

def fit_schema(twojmax,rcutfac,alpha):
    st = """[BISPECTRUM]
numTypes = 1
twojmax = %d
rcutfac = %1.5f
rfac0 = 0.99363
rmin0 = 0.0
wj = 1.0
radelem = 0.5
type = Ta
wselfallflag = 0
chemflag = 0
bzeroflag = 0
quadraticflag = 0

[CALCULATOR]
calculator = LAMMPSSNAP
energy = 1
force = 1
stress = 0

[ESHIFT]
Ta = 0.0

[SOLVER]
solver = RIDGE
compute_testerrs = 1
detailed_errors = 1

[RIDGE]
alpha=%2.6E

[SCRAPER]
scraper = JSON

[PATH]
dataPath = ../JSON


[OUTFILE]
metrics = Ta_metrics.md
potential = Ta_pot

[REFERENCE]
units = metal
atom_style = atomic
pair_style = hybrid/overlay zero 10.0 zbl 4.0 4.8
pair_coeff1 = * * zero
pair_coeff2 = * * zbl 73 73

[GROUPS]
# name size eweight fweight vweight
group_sections = name training_size testing_size eweight fweight vweight
group_types = str float float float float float
smartweights = 0
random_sampling = 0
Displaced_A15     =    1.0   0.0   37.912100   8.040892    1.E-8
Displaced_BCC     =    1.0   0.0   97.121915   6.859884    1.E-8
Displaced_FCC     =    1.0   0.0   80.597946   4.986826    1.E-8
Elastic_BCC     =    1.0   0.0   77.126500   58.771619    1.E-8
Elastic_FCC     =    1.0   0.0   76.801221   54.421385    1.E-8
GSF_110     =    1.0   0.0   49.983228   7.842181    1.E-8
GSF_112     =    1.0   0.0   42.249381   8.578090    1.E-8
Liquid     =    1.0   0.0   35.912991   7.147558    1.E-8
Surface     =    1.0   0.0   0.087594   0.046303    1.E-8
Volume_A15     =    1.0   0.0   65.767512   476.199243    1.E-8
Volume_BCC     =    1.0   0.0   63.919740   5.451515    1.E-8
Volume_FCC     =    1.0   0.0   59.903324   28.038123    1.E-8

[EXTRAS]
dump_descriptors = 0
dump_truth = 0
dump_weights = 0
dump_dataframe = 0

[MEMORY]
override = 0""" % (twojmax,rcutfac,alpha)
    return st


# summary of what LHS does: (to be used over random sampling)
#  1) Divide each parameter range into equally spaced intervals, i 
#  2) Sample one point from each interval, n_samples times, such that no two points share the same row or column (n_samples,i)


# define parameter ranges for a Latin Hypercube Sampling
variable_ranges_dict = {
        'twojmax':[5,8],
        'rcutfac':[3.0,6.0],
        'logalpha':[-7,-1]
        }
variable_types_dict = {'twojmax':int,
        'rcutfac':float,
        'logalpha':int
        }

#---------------------------------------------------------------
# Now build the latin hypercube samples using these variable ranges

# general usage: latin_hypercube_sample(variable_ranges_dict, \
#                                       variable_types_dict, num_samples,seed=48291)
# variable_ranges_dict (dict): gives the allowed values for each variable to be sampled
# variable_types_dict (dict):  gives the variable type for each variable to be sampled
#  (note that it also accepts strings)
# num_samples (int) : number of samples from the hypercube
# seed (int) : seed for random column selection (for reproducability)

num_samples = 25
lhsamples = latin_hypercube_sample(variable_ranges_dict, variable_types_dict, num_samples)
print(lhsamples)
np.save('lh_samples.npy',np.array(lhsamples))
#---------------------------------------------------------------


#---------------------------------------------------------------
# loop over lh samples and write a FitSNAP input for each
#---------------------------------------------------------------

for isamp,lh_sample in enumerate(lhsamples):
    twojmax,rcutfac,logalpha = tuple(lh_sample)
    alpha = 10**logalpha
    inpfile_str = fit_schema(twojmax,rcutfac,alpha)
    dirname = 'sample_%03d' % isamp
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    os.chdir(dirname)
    with open('Ta-example.in','w') as writeout:
        writeout.write(inpfile_str)
    os.chdir('../')
