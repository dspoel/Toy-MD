#!/usr/bin/env python3

# read ATOM or HETATM frompdb
def read_pdb(filename):
    inputfile = open(filename, "r", encoding='utf-8')
    box    = []
    coords = []
    atomnm = []
    resnm  = []
    resnr  = []
    elem   = []
    conect = []
    try:
        for line in inputfile:
            if (line.find("ATOM") == 0 or
                line.find("HETATM") == 0):
                x = float(line[31:37])
                y = float(line[38:45])
                z = float(line[46:53])
                coords.append([x, y, z])
                atomnm.append(line[12:16])
                resnm.append(line[17:20])
                resnr.append(int(line[22:27]))
                if (len(line) >= 77):
                    elem.append(line[76:78])
                else:
                    elem.append("  ")
            elif (line.find("CRYST1") == 0):
                box.append(float(line[7:15]))
                box.append(float(line[16:24]))
                box.append(float(line[25:33]))
            elif (line.find("CONECT") == 0):
                conect.append([int(line[7:12]), int(line[13:18])])
    finally:
        inputfile.close()
    return [ box, coords, atomnm, resnm, resnr, elem, conect ]
       
def write_pdb_frame(file, step, box, coords, atomnm, resnm, resnr, elem):
    file.write("TITLE    t = %s\n" % ( step ))
    file.write("CRYST1%9.3f%9.3f%9.3f%7.2f%7.2f%7.2f P 1           1\n" %
               ( box[0], box[1], box[2], 90, 90, 90 ))
    file.write("MODEL    %5d\n" % ( step ) )
    N = len(coords)
    for i in range(N):
        file.write("ATOM   %4d %4s%4s  %4d    %8.3f%8.3f%8.3f%6.2f%6.2f          %2s\n" %
                   ( i+1, atomnm[i], resnm[i], resnr[i],
                     coords[i][0], coords[i][1], coords[i][2],
                    1.0, 0.0, elem[i] ) )
    file.write("TER\n")
    file.write("ENDMDL\n")

def test_pdb():
    [ box, coords, atomnm, resnm, resnr, elem, conect ] = read_pdb("koko.pdb")

    outputfile = open("water2.pdb", "w", encoding='utf-8')
    try:
        write_pdb_frame(outputfile, 1, box, coords, atomnm, resnm, resnr, elem)
    finally:
        outputfile.close()
        
