# Our training data and methods

## Contents

### Code and pseudopotentials

<b>tools</b>: `automation/tools` Scripts, functions, and methods for setting up 
and running QE DFT calculations for interatomic potentials. Tools are also
provided that convert QE outputs into data structures required by FitSNAP

The scripts and tools in `automation` generate QE input files based on
certain defaults and environment variables. (defaults have been tested).
Firstly, itis assumed that the PseudoDojo pseudopotential library is used. 
This library needs to be uncompressed from `automation/qe_pseudos.zip` 
and an environment variable needs to be set to:
`export ESPRESSO_PSEUDO=/path/to/automation/qe_pseudos`
for QE to run the scripts within.

To use the tools, just add the folder to your pythonpath

`export PYTHONPATH=$PYTHONPATH:/path/to/automation/tools`

### Structures

<b>Single element structures</b> structures for the single element components
can be found in `simple_single_element`. 

<b>Other alloy structures</b> more alloy structures may be found in
`composition_sampling_bcc`. These are small and should run quickly. They
are made using symmetry arguments

# TO ADD and train on in the next iteration of the potential

<b>High temperature trajectory from AIMD or with single SCF DFT ran on high temp 
trajectory from a classical potential</b>

<b>Genetic algorithm structures with ditstorted lattice positions</b>

<b>Defect structures</b>

... and others recommened/required following first tests.
