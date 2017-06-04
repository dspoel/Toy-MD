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

def dot_product(x, y):
    xy = 0;
    N  = len(x)
    for i in range(N):
        xy += x[i]*y[i]
    return xy

def inner_product(x):
    return dot_product(x, x)

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

def nonbonded_forces(box, coords, elem, exclude, force, sigma, epsilon, charge):
    energy = 0
    N = len(coords)
    # Physical constant 1/4 pi epsilon_0 in the right MD units
    facel = 138.1
    cutoff_squared = (0.9*min(0.5*box[0], 0.5*min(box[1], box[2])))**2
#    print("cutoff %.2f" % ( math.sqrt(cutoff_squared) ) )
    for i in range(N):
        i1 = i+1
        for j in range(i1, N):
            if (not j in exclude[i]):
                dx   = distance_pbc(box, coords[i], coords[j])
                dx2  = inner_product(dx)
                dx_1 = 1.0/math.sqrt(dx2)
                if (dx2 < cutoff_squared):
                   # print("pair %d %d distance %.3f" % ( i, j, math.sqrt(dx2) ) )
                    Ecoul = charge[elem[i]]*charge[elem[j]]*facel*dx_1
                    Fcoul = -Ecoul*dx_1
                    epsilon_ij = math.sqrt(epsilon[elem[i]]*epsilon[elem[j]])
                    if (epsilon_ij > 0):
                        sigma_ij   = 0.5*(sigma[elem[i]]+sigma[elem[j]])
                        sr         = sigma_ij*dx_1
                        sr6        = sr**6
                        Evdw       = 4*epsilon_ij*(sr6**2 - sr6)
                        Fvdw       = 4*epsilon_ij*((sr6*sr)**2 - sr6*sr**2)
                    else:
                        Evdw       = 0
                        Fvdw       = 0
                    energy    += (Ecoul + Evdw)
                    for m in range(3):
                        dfm = (Fcoul+Fvdw)*dx[m]
                        force[i][m] += dfm
                        force[j][m] -= dfm  
    return [ energy, force ]

def calculate_forces(box, coords, elem, conect, exclude, ff):
    N = len(coords)
    force = []
    for i in range(N):
        force.append([0.0, 0.0, 0.0])
    [ Vbond, force ]    = bonded_forces(box, coords, elem, conect, force,
                                        ff["bond_length"], ff["bond_force_const"])
    [ Vnonbond, force ] = nonbonded_forces(box, coords, elem, exclude, force,
                                           ff["sigma"], ff["epsilon"], ff["charge"])
    
    return [ Vbond+Vnonbond, force ]
