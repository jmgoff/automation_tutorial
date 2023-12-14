# single element structures

The folders within give single-element crystal structures
for the 4 element system in the 14 bravais lattices. These
include the lowest energy structures for the respective elements.
In each folder, functions are called to generate these systematically
based on experimental bond lengths for different elements. 

The scripts within also demonstrate how the 'automation/tools' library
may be used to automatically convert 'cif', 'POSCAR', and many other
structures into QE inputs, based on our default DFT settings. For these
to work, automation/tools needs to be added to your PYTHONPATH environment
variable. These tools automatically adjust KPOINTS to maintain consistency
between different structures/ supercell sizes.

export PYTHONPATH=$PYTHONPATH:/path/to/automation/tools

If desired, one may choose to only run the 2-3 lowest energy structures.
These should be run with `calculation="vc-relax"` in QE.
