"""
Holds functions for running Prover9 and Mace4 with some input.
"""
import subprocess
import os

from fca import Implication

def impls_to_mace4(dict_obj_imps, destination, wait_time=2):
    """
    Runs Mace4 with implications as theorems to reject.
    Result is written in destination in many files!
    Number of found counterexamples (CE) and implications in unit form
    are returned.
    """
    sos = 'formulas(sos).\n'
    goals = 'formulas(goals).\n'
    eol = 'end_of_list.\n\n'
    CE = 0

    for obj in dict_obj_imps:
        ImplNum = 0
        unit_imps = 0
        for imp in dict_obj_imps[obj]:
            ImplNum += 1
            count = 0
            for j in (imp.conclusion - imp.premise):
                count += 1
                unit_imps += 1
                InFileName = (destination +
                              r'/impl{}_{}_obj{}.in'.format(ImplNum, count, obj))
                InputFile = open(InFileName, 'w')
                InputFile.write(sos)
                for k in imp.premise:
                    InputFile.write('\t' + str(k) + '.\n')
                InputFile.write(eol)
    
                InputFile.write(goals)
                InputFile.write('\t' + str(j) + '.\n')
                InputFile.write(eol)
                InputFile.close()
    
                MaceOutput = (destination +
                              r'/impl{}_{}_obj{}.mace4.out'.format(ImplNum, count, obj))
                if subprocess.call('mace4 -c -t {} -f '.format(wait_time)
                                   + InFileName + ' > ' +
                                   MaceOutput, shell=True) != 0:
                    os.remove(MaceOutput)
                else: CE += 1
                InputFile.close()
                os.remove(InFileName)
    return CE

def prove9_impls(dict_obj_imps, destination, wait_time=2):
    """
    Runs Prover9 with dict_obj_imps.values() as theorems to prove.
    Result is written in destination in many files!
    Proved, not proved and dict_obj_imps in unit form are returned.
    """
    sos = 'formulas(sos).\n'
    goals = 'formulas(goals).\n'
    eol = 'end_of_list.\n\n'
    Proved = []
    NotProved = []
    
    for obj in dict_obj_imps:
        ImplNum = 0
        unit_imps = 0
        for imp in dict_obj_imps[obj]:
            ImplNum += 1
            count = 0
            for j in (imp.conclusion - imp.premise):
                count += 1
                unit_imps += 1
                InFileName = (destination +
                              r'/obj{}_impl{}_{}.in'.format(obj, ImplNum, count))
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
                              r'/obj{}_impl{}_{}.prover9.out'.format(obj, ImplNum, count))
                if subprocess.call('prover9 -t {} -f '.format(wait_time) +
                                   InFileName + ' > ' +
                                   ProvOutput, shell=True) != 0:
                    os.remove(ProvOutput)
                    NotProved.append('obj{}_impl{}_{}'.format(obj, ImplNum, count))
                else:
                    wset = set()
                    wset.add(j)
                    Proved.append(Implication(imp.premise, wset))
                InputFile.close()
                os.remove(InFileName)
    return Proved, NotProved