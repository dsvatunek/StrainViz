"""
The script will exist in a distributable file package with the following architecture:

Strain_modeler/   
|-- geometry/  
|-- dummies/
|-- output/  
|-- scripts.py
|-- README.md
1. The user will create a geometry folder, add a .xyz geometry of the optimized strained molecule, 
and as many .out gaussian output files from force calculations as necessary into the dummies folder.
2. A script will compile and average all of the .out files to create .tcl scripts in the output folder.
3. The user can then run the .tcl scripts in VMD to visualize each type of molecular strain.
"""

from scripts import *
from bond_scripts import *
import os

for file in os.listdir('geometry'):
    if file.endswith(".xyz"):
        geometry_filename = 'geometry/' + file
		
full_bond_forces = []
full_angle_forces = []
full_dihedral_forces = []
full_key = []
for file in os.listdir('dummies'):
    if file.endswith(".out"):
        a, b, c = map_forces(geometry_filename, file)
        for line in a:
            full_bond_forces.append(line)
        for line in b:
            full_angle_forces.append(line)
        for line in c:
            full_dihedral_forces.append(line)

averaged_bond_forces = combine_dummies(full_bond_forces, geometry_filename, "bond")
averaged_angle_forces = combine_dummies(full_angle_forces, geometry_filename, "angle")
averaged_dihedral_forces = combine_dummies(full_dihedral_forces, geometry_filename, "dihedral")

total_forces = averaged_bond_forces + averaged_angle_forces + averaged_dihedral_forces
combine_force_types(total_forces, geometry_filename)

print_total(total_forces, "Total strain")
print_total(averaged_bond_forces, "Bond strain")
print_total(averaged_angle_forces, "Angle strain")
print_total(averaged_dihedral_forces, "Dihedral strain")