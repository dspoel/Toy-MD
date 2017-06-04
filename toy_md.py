#!/usr/bin/env python3

import sys, argparse
from toy_md_integrate   import *
from toy_md_params      import *
from toy_md_force_field import *
from toy_md_files       import *
from toy_md_forces      import *
from toy_md_util        import *

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--coordinates", dest="coordinates", help="Coordinate pdb file for reading",   type=str,    default=None)
    parser.add_argument("-o", "--trajectory",  dest="trajectory",  help="Output pdb file for writing",  type=str,    default="traj.pdb")
    parser.add_argument("-p", "--parameters",  dest="parameters",  help="Parameter file for reading",   type=str,    default=None)
    parser.add_argument("-ff", "--forcefield",  dest="forcefield",  help="Parameter file for reading",   type=str,    default=None)
    args = parser.parse_args()
    if (not args.coordinates):
        printf("Sorry but I need a coordinate file")
        exit(0)
    if (not args.parameters):
        printf("Sorry but I need a parameter file")
        exit(0)
    if (not args.forcefield):
        printf("Sorry but I need a forcefield file")
        exit(0)
        
    return args

# Here starts the fun stuff
if __name__ == '__main__':
    # Check command line arguments
    args  = parseArguments()

    # Read run parameters
    md_params = read_parameters(args.parameters, True)

    # Read input coordinates, atom name etc.
    [ box, coords, atomnm, resnm, resnr, elem, conect ] = read_pdb(args.coordinates)
    # Add angles
    conect = make_angles(conect)

    # Generate intramolecular exclusions
    exclude = make_exclusions(len(coords), conect)
        
    # Make a velocities array
    velocities = []
    for i in range(len(coords)):
        velocities.append([0.0, 0.0, 0.0])

    # Get the force field
    ff = read_force_field(args.forcefield)

    # Get shortcut for the masses
    masses = get_masses(elem, ff["mass"])

    # Open the trajectory file
    outputfile = open(args.trajectory, "w", encoding='utf-8')
    for step in range(int(md_params["number-of-steps"])):
        # Compute the forces
        [ epotential, forces ] = calculate_forces(box, coords, elem, conect, exclude, ff )
        
        # Step the coordinates
        [ ekinetic, coords, velocities ] = integrate(box, coords, velocities, forces,
                                                         masses, float(md_params["time-step"]))
            
        # Put the coordinates back in the box
        put_in_box(box, resnr, coords)

        # Compute temperature
        T = get_temperature(len(coords), ekinetic)
        
        # Print some stuff
        print("Step: %5d Epot  %10.3f  Ekin  %10.3f   Etot %10.3f  T %7.2f" %
              ( step, epotential, ekinetic, epotential+ekinetic, T) )
        if (step % int(md_params["output-frequency"]) == 0):
            write_pdb_frame(outputfile, step, box, coords, atomnm, resnm, resnr, elem)

    # Done with the loop over steps, now close the file
    outputfile.close()
        
