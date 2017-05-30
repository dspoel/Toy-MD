#!/usr/bin/env python3

import math

def distance_pbc(box, x1, x2):
    dx = []
    for m in range(3):
        dx.append(x1[m] - x2[m])
        while (dx[m] > box[m]/2):
            dx[m] -= box[m]
        while (dx[m] <= -box[m]/2):
            dx[m] += box[m]
    return dx

def inner_product(x):
    x2 = 0;
    for xx in x:
        x2 += xx*xx
    return x2

def bonded_forces(box, coords, elem, conect, force, bond_length, force_const ):
    energy = 0
    for c in conect:
        dx   = distance_pbc(box, coords[c[0]], coords[c[1]])
        dx2  = inner_product(dx)
        dx1  = math.sqrt(dx2)
        bond = elem[c[0]] + "-" + elem[c[1]]
        if (not bond in bond_length or not bond in force_const):
            print("Unknown bond %s. Quitting." % ( bond ) )
            exit(1)
        ddx       = dx1-bond_length[bond]
        ener      = 0.5*force_const[bond]*ddx**2
        energy   += ener
        temporary = -force_const[bond]*ddx/dx1
        for m in range(3):
            force[c[0]][m] += temporary*dx[m]
            force[c[1]][m] -= temporary*dx[m]
    return [ energy, force ]

def nonbonded_forces(box, coords, elem, conect, force, sigma, epsilon, charge):
    energy = 0
    return [ energy, force ]
 
def calculate_forces(box, coords, elem, conect, ff):
    N = len(coords)
    force = []
    for i in range(N):
        force.append([0.0, 0.0, 0.0])
    [ Vbond, force ]    = bonded_forces(box, coords, elem, conect, force,
                                        ff["bond_length"], ff["force_const"])
    [ Vnonbond, force ] = nonbonded_forces(box, coords, elem, conect, force,
                                           ff["sigma"], ff["epsilon"], ff["charge"])
    
    return [ Vbond+Vnonbond, force ]
