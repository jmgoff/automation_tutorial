#!/bin/bash

# greps the first cell vector from each single-atom eos poscar
grep -A1 -n '1\.0' ./*/POSCAR | grep '  '
