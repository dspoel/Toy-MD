#!/usr/bin/env python3

import sys, argparse
from toy_md_integrate   import *
from toy_md_params      import *
from toy_md_force_field import *
from toy_md_files       import *
from toy_md_forces      import *

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--coordinates", dest="coordinates", help="Coordinate pdb file for reading",   type=str,    default="")
    parser.add_argument("-o", "--trajectory",  dest="trajectory",  help="Output pdb file for writing",  type=str,    default="")
    parser.add_argument("-p", "--parameters",  dest="parameters",  help="Parameter file for reading",   type=str,    default="params.txt")
    parser.add_argument("-ff", "--forcefield",  dest="force_field",  help="Parameter file for reading",   type=str,    default="force_field.txt")
    args = parser.parse_args()
    return args

def get_masses(elem, mass):
    masses = []
    N = len(elem)
    for i in range(N):
        if (elem[i] in mass):
            masses.append(mass[elem[i]])
        else:
            print("No mass for elem '%s'" % ( elem[i] ) )
    return masses

# Here starts the fun stuff
if __name__ == '__main__':
    args  = parseArguments()

    if (len(args.parameters) > 0):
        md_params = read_parameters(args.parameters, True)

    if (len(args.coordinates) > 0):
        [ box, coords, atomnm, resnm, resnr, elem, conect ] = read_pdb(args.coordinates)
        # Make a velocities array
        velocities = []
        for i in range(len(coords)):
            velocities.append([0.0, 0.0, 0.0])
        # Get the force field
        ff = read_force_field(args.force_field)
        # Get shortcut for the masses
        masses = get_masses(elem, ff["mass"])
        # Open the trajectory file
        outputfile = open(args.trajectory, "w", encoding='utf-8')
        for step in range(int(md_params["number-of-steps"])):
            [ epotential, forces ] = calculate_forces(box, coords, elem, conect, ff )
            [ ekinetic, coords, velocities ] = integrate(box, coords, velocities, forces,
                                                         masses, float(md_params["time-step"]))
            print("Epot  %10.3f  Ekin  %10.3f   Etot %10.3f" %
              ( epotential, ekinetic, epotential+ekinetic) )
            if (step % int(md_params["output-frequency"]) == 0):
                write_pdb_frame(outputfile, step, box, coords, atomnm, resnm, resnr, elem)
        outputfile.close()
    else:
        print("No coordinate file")
        
