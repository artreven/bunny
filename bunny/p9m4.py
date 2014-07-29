"""
Holds functions for running Prover9 and Mace4 with some input.
"""
import subprocess
import os
import shutil

import fca

import bunny

def mace4(imp, file_path, wait_time=1):
    """
    Runs Mace4 with implication as theorems to reject.
    
    @param imp: implication
    @param file_path: name of (input and output) files for Mace4
    @param wait_time: time constraint for mace4
    @return: (counter-example, reason)
    """
    sos = 'formulas(sos).\n'
    goals = 'formulas(goals).\n'
    eol = 'end_of_list.\n\n'
    
    file_name = (file_path + r'.in')
    with open(file_name, 'w') as file:
        if imp.premise:
            file.write(sos)
            file.write('\t' + '.\n\t'.join(str(k) for k in imp.premise) + '.\n')
            file.write(eol)

        file.write(goals)
        file.write('\t')
        file.write('(' + ') & ('.join(str(j) for j in imp.conclusion) + ').\n')
        file.write(eol)
    file.close()

    output = (file_path + r'.mace4.out')
    call_str = 'mace4 -t {0} -N 75 -f '.format(wait_time)
    call_str += file_name + ' > ' + output
    ce = None
    reason = None
    # Process output codes in to reasons
    with open(os.devnull, "w") as fnull:
        output_code = subprocess.call(call_str, shell=True, stdout=fnull, stderr=fnull) 
        if output_code == 2:
            # not found
            reason = 'Search complete with no models'
            os.remove(output)
        elif output_code == 5:
            # not found
            reason = 'Timeout'
            os.remove(output)
        elif output_code == 0:
            # found 
            ce = read_model(output)
        else:
            raise Exception, 'Unexpected output code {0} from Mace4'.format(output_code)
    os.remove(file_name)
    return (ce, reason)

def prover9(imp, file_path, wait_time=1):
    """
    Runs Prover9 with implication as theorem to prove.
    
    @param imp: implication
    @param file_path: name of (input and output) files for Prover9
    @param wait_time: time constraint for Prover9
    @return: True or False
    """
    sos = 'formulas(sos).\n'
    goals = 'formulas(goals).\n'
    eol = 'end_of_list.\n\n'
    
    file_name = (file_path + r'.in')
    with open(file_name, 'w') as file:
        if imp.premise:
            file.write(sos)
            file.write('\t' + '.\n\t'.join(str(k) for k in imp.premise) + '.\n')
            file.write(eol)

        file.write(goals)
        file.write('\t')
        file.write('(' + ') & ('.join(str(j) for j in imp.conclusion) + ').\n')
        file.write(eol)
    file.close()

    output = (file_path + r'.prover9.out')
    call_str = 'prover9 -t {0} -f '.format(wait_time)
    call_str += file_name + ' > ' + output
    with open(os.devnull, "w") as fnull:
        # Process output codes in to reasons
        output_code = subprocess.call(call_str, shell=True, stdout=fnull, stderr=fnull)
        if output_code != 0:
            # not proved
            os.remove(output)
            proved = False
        else:
            # proved
            proved = True
    os.remove(file_name)
    return proved


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
    bun = bunny.Bunny(B, U, N, index)
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
    pass