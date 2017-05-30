#!/usr/bin/env python3

def read_force_field(filename):
    infile = open(filename, "r", encoding='utf-8')
    bond_length       = {}
    bond_force_const  = {}
    sigma             = {}
    epsilon           = {}
    mass              = {}
    charge            = {}
    for line in infile:
        # Skip comments starting with '#'
        comment = line.find('#')
        params = line[:comment].split()
        key = params[0].strip()
        Nparam = len(params)
        if (key.find("sigma") == 0 and Nparam == 3):
            sigma[params[1].strip()] = float(params[2].strip())
        elif (key.find("epsilon") == 0 and Nparam == 3):
            epsilon[params[1].strip()] = float(params[2].strip())
        elif (key.find("bond") == 0 and Nparam == 5):
            bond  = params[1] + "-" + params[2]
            bond2 = params[2] + "-" + params[1]
            bond_length[bond]       = float(params[3])
            bond_length[bond2]      = float(params[3])
            bond_force_const[bond]  = float(params[4])
            bond_force_const[bond2] = float(params[4])
        elif (key.find("mass") == 0 and Nparam == 3):
            mass[params[1].strip()] = float(params[2].strip())
        elif (key.find("charge") == 0 and Nparam == 3):
            charge[params[1].strip()] = float(params[2].strip())
        else:
            print("Unknown keyword '%s' in %s" % ( key, filename ) )
    ff                      = {}
    ff["bond_length"]       = bond_length
    ff["bond_force_const"]  = bond_force_const
    ff["sigma"]             = sigma
    ff["epsilon"]           = epsilon
    ff["charge"]            = charge
    ff["mass"]              = mass
    return ff
