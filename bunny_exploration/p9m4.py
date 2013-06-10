"""
Holds functions for running Prover9 and Mace4 with some input.
"""
import subprocess
import os

from fca import Implication

import bunny_exploration as be

def mace4(imp_ls, destination, wait_time=1):
    """
    Runs Mace4 with implications as theorems to reject.
    Result is written in many files!
    
    @param destination: where output file of mace4 go
    @param wait_time: time constraint for mace4
    @return: number of found counter-examples
    """
    sos = 'formulas(sos).\n'
    goals = 'formulas(goals).\n'
    eol = 'end_of_list.\n\n'
    N = 0
    
    imp_num = 0
    unit_imps = 0
    for imp in imp_ls:
        imp_num += 1
        count = 0
        for j in (imp.conclusion - imp.premise):
            count += 1
            unit_imps += 1
            file_name = (destination +
                          r'/impl{}_{}.in'.format(imp_num, count))
            with open(file_name, 'w') as file:
                file.write(sos)
                for k in imp.premise:
                    file.write('\t' + str(k) + '.\n')
                file.write(eol)
    
                file.write(goals)
                file.write('\t' + str(j) + '.\n')
                file.write(eol)
                file.close()
    
                output = (destination +
                          r'/impl{}_{}_mace4.out'.format(imp_num, count))
                if subprocess.call('mace4 -t {} -N 100 -f '.format(wait_time)
                                   + file_name + ' > ' +
                                   output, shell=True) != 0:
                    os.remove(output)
                else: N += 1
            file.close()
            os.remove(file_name)
    return N

def prover9(imp_ls, destination, wait_time=2):
    """
    Runs Prover9 with implications as theorems to reject.
    Result is written in many files!
    
    @param destination: where output file of mace4 go
    @param wait_time: time constraint for mace4
    @return: list of proven atomic imps, list of not proven atomic imps
    """
    sos = 'formulas(sos).\n'
    goals = 'formulas(goals).\n'
    eol = 'end_of_list.\n\n'
    Proved = []
    NotProved = []
    
    imp_num = 0
    unit_imps = 0
    for imp in imp_ls:
        imp_num += 1
        count = 0
        for j in (imp.conclusion - imp.premise):
            count += 1
            unit_imps += 1
            InFileName = (destination +
                          r'/impl{}_{}.in'.format(imp_num, count))
            InputFile = open(InFileName, 'w')
            InputFile.write(sos)
            for k in imp.premise:
                InputFile.write('\t' + str(k) + '.\n')
            InputFile.write(eol)

            InputFile.write(goals)
            InputFile.write('\t' + str(j) + '.\n')
            InputFile.write(eol)
            InputFile.close()

            ProvOutput = (destination +
                          r'/impl{}_{}.prover9.out'.format(imp_num, count))
            if subprocess.call('prover9 -t {} -f '.format(wait_time) +
                               InFileName + ' > ' +
                               ProvOutput, shell=True) != 0:
                os.remove(ProvOutput)
                NotProved.append(Implication(imp.premise, set((j,))))
            else:
                Proved.append(Implication(imp.premise, set((j,))))
            InputFile.close()
            os.remove(InFileName)
    return Proved, NotProved


def read_model(path):
    """
    Extracting models from *.mace4.out files
    
    @return: bunny object
    """
    with open(path) as MF:
        FileText = MF.readlines()
    MF.close()
    # Finding Model
    LengthFile = len(FileText)
    for i in range(LengthFile):
        if (FileText[i].find( r'MODEL' ) != -1): break
    ModelStrInd = i
    # Reading domain
    for i in range(ModelStrInd+1, LengthFile):
        if (FileText[i].find( r'interpretation' ) != -1): break
    DomStrInd = i
    for i in FileText[DomStrInd]:
        if i.isdigit():
            Dom = int(i)
            break
    # Reading multiplication table
    found = False
    for i in range(ModelStrInd+1, LengthFile):
        if (FileText[i].find( r'function(*(_,_)' ) != -1):
            found = True
            break
    B = dict([(i, j), 0]
             for i in range(Dom)
             for j in range(Dom))
    NumB = 0
    if found:
        FunStrInd = i
        wstr = ''
        for i in range(Dom):
            wstr += FileText[FunStrInd+i+1]
        count = 0
        for i in wstr:
            if i.isdigit():
                B[count/Dom, count%Dom] = int(i)
                count += 1
        # Calculating Numj
        for i in range(Dom):
            for j in range(Dom):
                NumB += B[i, j] * Dom**(i + j*Dom)
    # Reading unary table
    found = False
    for i in range(ModelStrInd+1, LengthFile):
        if (FileText[i].find( r'function(-(_)' ) != -1):
            found = True
            break
    U = dict([i, 0] for i in range(Dom))
    NumU = 0
    if found:
        InvStrInd = i
        wstr = FileText[InvStrInd]
        count = 0
        for i in wstr:
            if i.isdigit():
                U[count] = int(i)
                count += 1
        # Calculating NumU
        for i in range(Dom):
            NumU += U[i] * Dom**(i)
    # Reading constant
    found = False
    for i in range(ModelStrInd+1, LengthFile):
        if (FileText[i].find( r'function(a' ) != -1):
            found = True
            break
    NumN = N = 0
    if found:
        ConstStrInd = i
        wstr = FileText[ConstStrInd]
        for i in wstr:
            if i.isdigit():
                NumN = N = int(i)
    # prepare return and return
    index = NumB + NumU*(Dom ** (Dom**2)) + NumN*(Dom ** (Dom**2 + Dom))
    bun = be.Bunny(B, U, N, index)
    return bun

def read_all_models(dest):
    Files = os.listdir(dest)
    MaceFiles = []
    for i in Files:
        if 'mace4' in i:
            MaceFiles.append(i)
    a = []
    for i in MaceFiles:
        a.append( read_model(dest + r'/' + i) )
    return a


###############################################################################
if __name__ == "__main__":
    id_prem = 'x = a*(-x)'
    id_conc = 'x = -(a*x)'
    imp = Implication(set((id_prem, )),
                      set((id_conc, )))