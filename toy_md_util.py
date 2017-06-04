#!/usr/bin/env python3

def sorted_pair(a, b):
    if (b < a):
        tmp = b
        b   = a
        a   = tmp
    return [ a, b]

def make_angles(conect):
    newconn = []
    N = len(conect)
    print("There are %d bonds" % ( N ))
    for i in range(N):
        conect[i] = sorted_pair(conect[i][0], conect[i][1])

    for i in range(N):
        c = conect[i]
        i1 = i+1
        for j in range(i1, N):
            d = conect[j]
            if (c[0] == d[0] and not c[1] == d[1]):
                newconn.append(sorted_pair(c[1], d[1]))
            elif (c[1] == d[0] and not c[0] == d[1]):
                newconn.append(sorted_pair(c[0], d[1]))
            elif (c[0] == d[1] and not c[1] == d[0]):
                newconn.append(sorted_pair(c[1], d[0]))
            elif (c[1] == d[1] and not c[0] == d[0]):
                newconn.append(sorted_pair(c[0], d[0]))
    print("There are %d angles" % ( len(newconn) ))
    for n in newconn:
        conect.append(n)
    sorted_con = sorted(conect)
    print("There are %d conect" % ( len(sorted_con) ) )
    return sorted_con
    
def make_exclusions(N, conect):
    exclude = []
    for i in range(N):
        exclude.append([])
    nexcl = 0
    for c in conect:
        a1 = c[0]
        a2 = c[1]
        exclude[a1].append(a2)
        exclude[a2].append(a1)
        nexcl += 1
    print("There are %d exclusions" % (nexcl) )
    return exclude

def get_masses(elem, mass):
    masses = []
    N = len(elem)
    for i in range(N):
        if (elem[i] in mass):
            masses.append(mass[elem[i]])
        else:
            print("No mass for elem '%s'" % ( elem[i] ) )
    return masses

def get_temperature(natoms, ekin):
    # Use Ekin = (3/2) natoms kB T
    # T = (2 Ekin) / (3 kB natoms)
    kB = 0.00831415
    return (2 * ekin)/(3 * natoms * kB)
