#!/usr/bin/env python3

import sys, argparse
from toy_md_params import *
from toy_md_files  import *
from toy_md_forces import *

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--coordinates", dest="coordinates", help="Coordinate pdb file for reading",   type=str,    default="")
    parser.add_argument("-o", "--trajectory",  dest="trajectory",  help="Output pdb file for writing",  type=str,    default="")
    parser.add_argument("-p", "--parameters",  dest="parameters",  help="Parameter file for reading",   type=str,    default="params.txt")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args  = parseArguments()

    if (len(args.parameters) > 0):
        md_params = read_parameters(args.parameters, True)

    if (len(args.coordinates) > 0):
        [ box, coords, atomnm, resnm, resnr, elem, conect ] = read_pdb(args.coordinates)
        velocities = []
        for step in range(int(md_params["number-of-steps"])):
            [ energy, forces ] = calculate_forces(box, coords, elem, conect)
            integrate(box, coords, velocities, forces, md_params["time-step"])
            scale_temperature(velocities, md_params["temperature"])
            if (step % md_params["output-frequency"] == 0):
                wri
    else:
        print("No coordinate file")
        
