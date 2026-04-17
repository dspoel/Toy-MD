#!/usr/bin/env python

import math, plotxvg, numpy

NRANDOM = 6
NATOM   = 1000
TEMP    = 120  # Kelvin, in the liquid range for Argon
MASS    = 39 # Dalton for Argon
BOLTZ   = 0.008314 # kJ/mol K

def theory(v:float)->float:
    # From https://en.wikipedia.org/wiki/Maxwell%E2%80%93Boltzmann_distribution
    kBT = BOLTZ*TEMP
    x2  = MASS*v*v
    return (MASS/(2*math.pi*kBT))**(1.5) * 4 * v*v* math.pi * math.exp(-x2/(2*kBT))

def gen_v(amplitude):
    # Generate velocities for NATOM particles, store the square velocities
    allv = []
    vmax = 0
    for i in range(NATOM):
        # v squared
        v2 = 0
        # Loop over x,y,z
        for m in range(3):
            v2 += (amplitude*numpy.random.normal())**2
        v = math.sqrt(v2)
        allv.append(v)
        # Store the largest v squared
        if v > vmax:
            vmax = v
    return allv, vmax

if __name__ == "__main__":
    # Amplitude corresponding to temperature, using 1/2 mv^2 = 1/2 kB T
    amplitude  = math.sqrt(BOLTZ*TEMP/MASS)
    allv, vmax = gen_v(amplitude)

    # Generate a velocity distribution
    NDIST    = 50
    dist     = [0]*(NDIST+20)
    binwidth = vmax/NDIST
    # Fill the histogram
    for vv in allv:
        # Increase histogram bin and normalize by binwidth
        dist[int(vv/binwidth)] += 1.0*binwidth
    # Normalize the histogram
    dtot = 0
    for i in range(len(dist)):
        factor = 1
        if i == 0 or i == len(dist)-1:
            factor = 0.5
        dtot += factor*binwidth*dist[i]
    print("Sum over distribution %g" % dtot)
    for i in range(len(dist)):
        dist[i] = dist[i]/dtot

    # Now generate the plot
    vplot = "velocity-distribution.xvg"
    with open(vplot, "w") as out:
        out.write("@ title \"Velocity distribution\"\n")
        out.write("@ xaxis label \"Velocity (nm/ps)\"\n")
        out.write("@ yaxis label \"(arbitary units)\"\n")
        out.write("@ s0 legend \"Theoretical\"\n")
        out.write("@ s1 legend \"Generated\"\n")
        # Keep track of the integral of the distribution to check normalization
        dist_tot   = 0
        theory_tot = 0
        for i in range(len(dist)):
            v      = i*binwidth
            theo   = theory(v)
            ekin   = MASS*v*v
            factor = 1
            if i == 0 or i == len(dist)-1:
                factor = 0.5
            dist_tot   += factor*ekin*dist[i]*binwidth
            theory_tot += factor*ekin*theo*binwidth
            out.write("%10g  %10g  %10g\n" % (v, theo, dist[i]) )
        print("Integral over generated Ekin distribution %g (T=%g) theoretical %g (T=%g)" %
              ( dist_tot, dist_tot/(3*BOLTZ), theory_tot, theory_tot/(3*BOLTZ) ))
    plotxvg.plot([vplot], linestyle=["solid", "None"], mk=["None", "."])
