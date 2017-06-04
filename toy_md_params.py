#!/usr/bin/env python3

def check_parameters(md_params, filename):
    necessary = [ "number-of-steps", "time-step", "temperature", "output-frequency", "tau-T" ]
    nfound = 0
    for n in necessary:
        if (not n in md_params):
            print("No parameter %s in %s" % ( n, filename ) )
        else:
            nfound += 1
    if (nfound != len(necessary)):
        print("Not all parameters were found in %s, quitting" % ( filename ) )
        exit(0)
        
def read_parameters(filename, check = True):
    infile = open(filename, "r", encoding='utf-8')
    md_params = {}
    for line in infile:
        # Skip comments starting with '#'
        comment = line.find('#')
        params = line[:comment].split()
        if (len(params) > 1):
            md_params[params[0]] = params[1]

    if (check):
        check_parameters(md_params, filename)
    return md_params
