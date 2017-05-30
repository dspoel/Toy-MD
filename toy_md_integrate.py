#!/usr/bin/env python3

import math

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
