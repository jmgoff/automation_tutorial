# Composition subspace sampling

This directory contains subdirectories of alloy crystal structures that
are useful for fitting alloy potentials. The composition axes in the alloy
are completely sampled in VERY small unit cells (this means the composition
axes are sampled coarsely but compositions 0-1.0 are sampled for each element
combination. This is done systematically according to the procedure for 
generating derivative superstructures,
https://doi.org/10.1016/j.commatsci.2017.04.015 , using the ICET code. 
This generates <i>all</i> alloy unit cells that are unique up to space group
operations of the parent lattice.
 
<i>The chemical subspaces are sampled here in the BCC crystal structure only. 
We can quickly generate them for others when ready.</i>

# Specifics on the different sets of structures within

## Structures close to the quaternary alloy lattice constant (~2.9)

<b>AB_binary_DSS_# </b>: AB is the alloy pair within a 4 element system, 
the \# corresponds to the maximum supercell size (as a factor of the primitive 
cell) that has been enumerated. These structures should be run with
`calculation="relax"`.

<b>ABC_ternary_DSS_# </b>: ABC is the alloy triplet within a 4 element system, 
the \# corresponds to the maximum supercell size (as a factor of the primitive
cell) that has been enumerated. These structures should be run with
`calculation="relax"`.

Both of the above sets of structures may be generated with the binary_enum.py
and ternary_enum.py scripts, respectively. The lattice constant and the
parent lattice structure may be edited in these.

## compressed & expanded alloy structures 

<b>cmpex_AB_DSS_# </b>: AB is the alloy pair within a 4 element system
the \# corresponds to the maximum supercell size (as a factor of the primitive
cell) that has been enumerated. These structures should be run with
`calculation="scf"` - similar to equation of state calculations. 

These and other compressed/expanded structures may be generated with the
compress_expand.py script.
