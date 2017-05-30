#!/usr/bin/env python3

import math

def put_in_box(box, resnr, coords):
    N      = len(coords)
    cgcm   = []
    old    = -1
    invres = []
    for i in range(N):
        if (resnr[i] != old):
            cgcm.append([ 0.0, 0.0, 0.0 ])
            invres.append([])
            old = resnr[i]
        for m in range(3):
            cgcm[len(cgcm)-1][m] += coords[i][m]
        invres[len(invres)-1].append(i)
    N = len(cgcm)
    for i in range(N):
        for m in range(3):
            cgcm[i][m] /= len(invres[i])
    for i in range(N):
        for m in range(3):
            if (cgcm[i][m] > box[m]):
                for k in invres[i]:
                    coords[k][m] -= box[m]
            if (cgcm[i][m] <= 0):
                for k in invres[i]:
                    coords[k][m] += box[m]
    
def integrate(box, coords, velocities, forces, masses, time_step):
    N    = len(coords)
    ekin = 0
    for i in range(N):
        vel2 = 0
        for m in range(3):
            velocities[i][m] += forces[i][m]*time_step/masses[i]
            coords[i][m]     += velocities[i][m]*time_step
            vel2             += velocities[i][m]**2
        ekin += 0.5*masses[i] * vel2
    
    return [ ekin, coords, velocities ]
