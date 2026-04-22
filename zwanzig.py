#!/usr/bin/env python3

import numpy, os, plotxvg

TEMPERATURE = 298.15   # Kelvin
BOLTZ       = 0.008314 # kJ/mol Kelvin

def gen_delta_ener(nener:int, amplitude: float):
    # Generate velocities for NATOM particles, store the square velocities
    allener = []
    for i in range(nener):
        allener.append(amplitude*numpy.random.normal())

    return allener

if __name__ == "__main__":
    amplitude = 10.0 # kJ/mol
    beta      = 1.0/(BOLTZ*TEMPERATURE)
    print(f"Energy distribution witdh {amplitude} beta {beta}")
    for nener in [ 10, 100, 1000, 10000, 100000, 1000000 ]:
        deltaF = []
        deltaE = []
        ntrial = 5
        for i in range(ntrial):
            usum = 0
            esum = 0
            for ener in gen_delta_ener(nener, amplitude):
                usum += numpy.exp(-ener*beta)
                esum += ener
            deltaF.append(-BOLTZ*TEMPERATURE*numpy.log(usum/nener))
            deltaE.append(esum/nener)
        # Compute average and std. dev.
        dFsum = 0
        dFsum2 = 0
        for df in deltaF:
            dFsum += df
            dFsum2 += df**2
        dFaver = dFsum/ntrial
        dFstd  = numpy.sqrt(dFsum2/ntrial - dFaver**2)
        # Prepare nice output
        outstring = ("nener %7d deltaF:" % nener )
        for df in deltaF:
            outstring += (" %7.2f" % df)
        # Compute average energy
        dEsum = 0
        for de in deltaE:
            dEsum += de
        dEaver = dEsum/ntrial
        # Compute entropy
        deltaS = (dEaver - dFaver)
        print("%s aver %7.2f stddev %7.2f <E> %7.2f <TS> %7.2f kJ/mol" % ( outstring, dFaver, dFstd, dEaver, deltaS ) )
        
