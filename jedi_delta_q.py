import os
import numpy as np
import jedi_functions
from jedi_kill_atoms import ls_NrAtoms, x0_coords, xF_coords, delta_x_list
from jedi_directory import ba_state, bl_state, da_state
from jedi import directory

"""

It calculates the redundant internal coordinates from the B-Matrix and 
the deviation in the cartesian coordinates within in the deformation (delta q).

"""

print("Starting delta_q.py to calculate q0, qF and delta_q.")

# Read the transposed B-Matrix and generate its transposed
B_transp = np.loadtxt('b_transp.txt')
B = np.loadtxt('b_mat.txt')

class atom(object):
	# parsing the arguments (index: as specified in bl, ba and da; state: "relax" or "force")
	def __init__(self, index, state):
		self.state = state

		if self.state == "relax":
			self.x = x0_coords[(index - 1), 0]
		elif self.state == "force":
			self.x = xF_coords[(index - 1), 0]

		if self.state == "relax":
			self.y = x0_coords[(index - 1), 1]
		elif self.state == "force":
			self.y = xF_coords[(index - 1), 1]

		if self.state == "relax":
			self.z = x0_coords[(index - 1), 2]
		elif self.state == "force":
			self.z = xF_coords[(index - 1), 2]

    # distance between two atoms
	def distance(self, other):
		return np.sqrt( ( self.x - other.x )**2 + ( self.y - other.y )**2 + ( self.z - other.z )**2 )

	# vector between two atoms
	def vector(self, other):
		vec = [0, 0, 0]
		vec[0] = other.x - self.x
		vec[1] = other.y - self.y
		vec[2] = other.z - self.z
		return vec

q0 = []
qF = []

# Bond lengths
if bl_state == True: 
    __dirpath__ = os.path.realpath(os.path.join(os.getcwd(), directory))
    os.chdir(__dirpath__)

if os.path.isfile('bl.txt') or os.path.isfile('bl_manip.txt') == True:
    from jedi_kill_atoms import bl
    for i in bl:

        if len(ls_NrAtoms) > 0:
            for killed_atom in ls_NrAtoms:
                i_0 = jedi_functions.kill_atoms(killed_atom, int(i[0]))
                i_1 = jedi_functions.kill_atoms(killed_atom, int(i[1]))
                i = i_0, i_1

        atom_1_relax = atom( int(i[0]), "relax" )
        atom_2_relax = atom( int(i[1]), "relax" )
        q0.append(atom_1_relax.distance(atom_2_relax))

        atom_1_force = atom( int(i[0]), "force" )
        atom_2_force = atom( int(i[1]), "force" )
        qF.append(atom_1_force.distance(atom_2_force))

if bl_state == True:
    __origpath__ = os.path.dirname(os.getcwd())
    os.chdir(__origpath__)

# Bond angles
if ba_state == True: 
    __dirpath__ = os.path.realpath(os.path.join(os.getcwd(), directory))
    os.chdir(__dirpath__)

if os.path.isfile('ba.txt') or os.path.isfile('ba_manip.txt') == True:

    from jedi_kill_atoms import ba

    for i in ba:

        if len(ls_NrAtoms) > 0:
            for killed_atom in ls_NrAtoms:
                i_0 = jedi_functions.kill_atoms(killed_atom, int(i[0]))
                i_1 = jedi_functions.kill_atoms(killed_atom, int(i[1]))
                i_2 = jedi_functions.kill_atoms(killed_atom, int(i[2]))
                i = i_0, i_1, i_2

        atom_1_relax = atom( int(i[0]), "relax" )
        atom_2_relax = atom( int(i[1]), "relax" )
        atom_3_relax = atom( int(i[2]), "relax" )
        u0 = atom_2_relax.vector(atom_1_relax)
        v0 = atom_2_relax.vector(atom_3_relax)
        q0.append(np.arccos( np.dot( u0, v0 ) / ( np.linalg.norm(u0) * np.linalg.norm(v0) ) ))

        atom_1_force = atom( int(i[0]), "force" )
        atom_2_force = atom( int(i[1]), "force" )
        atom_3_force = atom( int(i[2]), "force" )
        uF = atom_2_force.vector(atom_1_force)
        vF = atom_2_force.vector(atom_3_force)
        qF.append(np.arccos( np.dot( uF, vF ) / ( np.linalg.norm(uF) * np.linalg.norm(vF) ) ))

if ba_state == True:
    __origpath__ = os.path.dirname(os.getcwd())
    os.chdir(__origpath__)

# Dihedral angles
counter = 0

if da_state == True: 
    __dirpath__ = os.path.realpath(os.path.join(os.getcwd(), directory))
    os.chdir(__dirpath__)

if os.path.isfile('da.txt') or os.path.isfile('da_manip.txt') == True:

    from jedi_kill_atoms import da

    for i in da:

        if len(ls_NrAtoms) > 0:
            for killed_atom in ls_NrAtoms:
                i_0 = jedi_functions.kill_atoms(killed_atom, int(i[0]))
                i_1 = jedi_functions.kill_atoms(killed_atom, int(i[1]))
                i_2 = jedi_functions.kill_atoms(killed_atom, int(i[2]))
                i_3 = jedi_functions.kill_atoms(killed_atom, int(i[3]))
                i = i_0, i_1, i_2, i_3

        atom_1_relax = atom( int(i[0]), "relax" )
        atom_2_relax = atom( int(i[1]), "relax" )
        atom_3_relax = atom( int(i[2]), "relax" )
        atom_4_relax = atom( int(i[3]), "relax" )
        u0 = atom_2_relax.vector(atom_1_relax)
        u0_normed = u0 / np.linalg.norm(u0)
        v0 = atom_3_relax.vector(atom_4_relax)
        v0_normed = v0 / np.linalg.norm(v0)
        w0 = atom_2_relax.vector(atom_3_relax)
        w0_normed = w0 / np.linalg.norm(w0)

        # numerical errors kill arccos if something like "1.0000000000024" is encountered. Be sure to avoid this.
        value = np.dot( np.cross( u0_normed, w0_normed ), np.cross( v0_normed, w0_normed ) ) / ( np.sqrt(1-(np.dot( u0_normed, w0_normed )**2)) * np.sqrt(1-(np.dot( v0_normed, w0_normed )**2)) )
        if ( value > 1.0 ) and ( value < 1.1 ):
            value = 1
        elif ( value < -1.0 ) and ( value > -1.1 ):
            value = -1

        q0_preliminary = np.arccos( value )

        atom_1_force = atom( int(i[0]), "force" )
        atom_2_force = atom( int(i[1]), "force" )
        atom_3_force = atom( int(i[2]), "force" )
        atom_4_force = atom( int(i[3]), "force" )
        uF = atom_2_force.vector(atom_1_force)
        uF_normed = uF / np.linalg.norm(uF)
        vF = atom_3_force.vector(atom_4_force)
        vF_normed = vF / np.linalg.norm(vF)
        wF = atom_2_force.vector(atom_3_force)
        wF_normed = wF / np.linalg.norm(wF)

        # see above
        value = np.dot( np.cross( uF_normed, wF_normed ), np.cross( vF_normed, wF_normed ) ) / ( np.sqrt(1-(np.dot( uF_normed, wF_normed )**2)) * np.sqrt(1-(np.dot( vF_normed, wF_normed )**2)) )
        if ( value > 1.0 ) and ( value < 1.1 ):
            value = 1
        elif ( value < -1.0 ) and ( value > -1.1 ):
            value = -1

        qF_preliminary = np.arccos( value )

# There is a problem in the definition of the dihedral angle: Only the cosine is uniquely defined,
# not the angle itself, since the cosine is antisymmetric to 0. In the definition by Helgaker,
# a dihedral is positive if one of the outer vectors has to be turned in a clockwise manner to coincide
# with the other outer vector and negative if it has to be turned anticlockwise. We can calculate the
# cosine perfectly, but we cannot say from the cosine value if the dihedral is positive or negative.
# The product B*delta_x, however, gives us a crude estimation for the dihedral angle, and in any case,
# the algebraic sign is correct. For this reason, we have to check the sign of the
# product B*delta_x and adjust the sign of the dihedral angle if necessary.
# In the (hopefully rare) cases in which dihedrals flip around +- 180 degrees, this procedure also
# gives the best estimate, since it adjusts the signs of q0 and qF in such a way that q0 is now on the
# "side" of qF, and since it is a good approximation that dihedrals are symmetric to 180 degrees,
# this procedure yields a good guess for the displacement of the dihedral. Otherwise, the displacement
# in the dihedral angle would be too large and the harmonic approximation would break down.

        check_dihedral = np.dot(B, delta_x_list)

        q0_final = q0_preliminary
        qF_final = qF_preliminary

        ba = np.array(ba, dtype = object)
        bl = np.array(bl, dtype = object)
        da = np.array(da, dtype = object)
        

        if ( check_dihedral[bl.shape[0]+ba.shape[0]+counter] < 0 ) and ( ( qF_preliminary - q0_preliminary ) > 0 ):
            q0_final = -q0_preliminary
            qF_final = -qF_preliminary
        elif ( check_dihedral[bl.shape[0]+ba.shape[0]+counter] > 0 ) and ( ( qF_preliminary - q0_preliminary ) < 0 ):
            q0_final = -q0_preliminary
            qF_final = -qF_preliminary

        q0.append(q0_final)
        qF.append(qF_final)

        counter += 1

if da_state == True:
    __origpath__ = os.path.dirname(os.getcwd())
    os.chdir(__origpath__)

# Generate delta_q
delta_q = np.subtract(qF, q0)

with open("delta_q.txt", "w+") as out_file:
    np.savetxt(out_file, delta_q, fmt='% f', delimiter='\t')
    out_file.close()
