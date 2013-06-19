'''
Created on Jun 6, 2013

@author: artreven
'''
import os
import time

import fca

import bunny_exploration as be

class AE(object):
    '''
    Class to represent Attribute Exploration procedure for bunnies
    '''

    def __init__(self, cxt, dest):
        '''
        Constructor
        '''
        self.cxt = cxt
        self.basis = None
        self.proved = []
        self.dest = dest
        
    def find_basis(self):
        """
        Find implication basis
        """
        basis = self.cxt.attribute_implications
        self.basis = basis
        return self.cxt.attribute_implications
            
    def _delete_models(self):
        """
        Delete all files output by Mace4
        """
        for i in os.listdir(self.dest):
            if 'mace4' in i:
                os.remove(self.dest + '/' + i)
                
    def _delete_proves(self):
        """
        Delete all files output by Prover9
        """
        for i in os.listdir(self.dest):
            if 'prover9' in i:
                os.remove(self.dest + '/' + i)
                
    def _clear_directory(self):
        self._delete_ces()
        self._delete_proves()
        
    def _output_basis(self):
        if self.basis == None:
            self.basis = self.find_basis()
        with open(self.dest + '/canon_imp_basis.txt', 'w') as file:
            for imp in self.basis:
                file.write(str(imp) + '\n')
        file.close()
        
    def _output_cxt(self):
        with open(self.dest + '/cxt.txt', 'w') as file:
            file.write(str(self.cxt) + '\n')
        file.close()
        
    def add_object(self, row, object_name):
        self.cxt.add_object(row, object_name)
        self.basis = None
        
    def add_attribute(self, col, attr_name):
        self.cxt.add_attribute(self, col, attr_name)
        self.basis = None
        
    def prove(self):
        """
        Run Prover9 on implication basis
        """
        if self.basis == None:
            self.basis = self.find_basis()
        return be.prover9(self.basis, self.dest)
    
    #TODO: probably delete, because differs from working with infinite bunnies
    def _add_models(self):
        """
        Add models found by Mace4
        """
        models = be.read_all_models(self.dest)
        for bun in models:
            self.add_object([bun.check_id(id_) for id_ in self.cxt.attributes],
                            bun)
    
    #TODO: not sure if this is needed
    def mace(self, add=True, delete=True):
        """
        Run Mace4 on implications from basis and add found CE to context
        """
        if self.basis == None:
            self.basis = self.find_basis()
        N = be.mace4(self.basis, self.dest)
        if add == True:
            self._add_models()
            self.basis = None
        if delete == True:
            self._delete_models()
        return N
    
    #TODO: not sure if this is needed
    def find_inf_ce(self, add=True):
        """
        Find infinite counter-examples and add them to the context
        @return: Dictionary {implication: counter-example}
        """
        #limit for checking the infinite bunnies
        limit = 10
        ce_dict = {}
        if self.basis == None:
            self.basis = self.find_basis()
        for imp in self.basis:
            for j in imp.conclusion:
                bun = be.InfBunny.find(imp.premise, j, limit)
                ce_dict[fca.Implication(imp.premise, set((j,)))] = bun
                if (bun != None) and (add == True):
                    self.add_object([bun.check_id(id_, limit)
                                     for id_ in self.cxt.attributes],
                                    bun)
        return ce_dict
    
    def find_ces(self, add=True):
        """
        Try to find counter-examples (first with mace, than infinite) for every
        implication.
        """
        if self.basis == None:
            self.basis = self.find_basis()
        #limit for checking of the infinite bunnies
        limit = 10
        ce_dict = {}
        fin = 0
        N = 0
        for imp in self.basis:
            for j in imp.conclusion:
                atomic_imp = fca.Implication(imp.premise, set((j,)))
                found = be.mace4((atomic_imp,), self.dest)
                if found == 1:
                    fin += 1
                    bun = be.read_model(self.dest + '/impl1_1_mace4.out')
                    os.remove(self.dest + '/impl1_1_mace4.out')
                elif found == 0:
                    (proved, _) = be.prover9((atomic_imp,), self.dest, 1)
                    if len(proved) == 1:
                        os.remove(self.dest + '/impl1_1.prover9.out')
                        continue
                    bun = be.InfBunny.find(imp.premise, j, limit)
                ce_dict[atomic_imp] = bun
                if (add == True) and (bun != None):
                    N += 1
                    self.add_object([bun.check_id(id_, limit)
                                     for id_ in self.cxt.attributes],
                                    bun)
        inf = N - fin
        return ce_dict, fin, inf
    
    def run(self, step=0):
        """
        Run Attribute Exploration procedure till no other counter-examples
        can be found. Try to prove, return proved and not proved implications.
        """
        # Remove progress left from previous runs
        if step == 0:
            try:
                os.remove(self.dest + '/progress.txt')
            except OSError:
                pass
        # tick
        now = time.time()
        if self.basis == None:
            self.basis = self.find_basis()
        # for info
        basis_time = time.time() - now
        basis = self.basis
        no_objs = len(self.cxt.objects)
        ce_dict, fin, inf = self.find_ces()
        N = fin + inf
        # tack
        m = '\n\n\n\tStep {}, it took {} seconds'.format(step + 1,
                                                         time.time() - now)
        m += ', of which {} seconds to find basis\n'.format(basis_time)
        m += 'Canonical basis consists of {} implications, '.format(len(basis))
        m += 'or {} atomic implications\n'.format(len(ce_dict.values()))
        m += 'There were {} objects before the start of this step\n'.format(no_objs)
        m += 'There were {} counter-examples found on this step, '.format(N)
        m += 'of which {} finite and {} infinite\n'.format(fin, inf)
        m += '{} atomic implications were not rejected\n'.format(len(ce_dict.values()) - N)
        self.cxt = self.cxt.reduce_objects()
        m += '{} Objects left after reducing\n'.format(len(self.cxt.objects))
        print m
        with open(self.dest + '/progress.txt', 'a') as file:
            file.write(m)
        file.close()
        with open(self.dest + '/step{}ces.txt'.format(step + 1), 'w') as file:
            file.write(str(ce_dict))
        file.close()
        # if no CE found try to prove
        if (not any(ce_dict.values())):
            self._output_basis()
            self._output_cxt()
            proved, not_proved = self.prove()
            with open(self.dest + '/progress.txt', 'a') as file:
                file.write('\n\nProved implications:\n')
                for imp in proved:
                    file.write(str(imp) + '\n')
                file.write('\n\nNot proved implications:\n')
                for imp in not_proved:
                    file.write(str(imp) + '\n')
            file.close()
            return (proved, not_proved)
        # if CE found proceed to next step
        return self.run(step + 1)
    
    
########################################################
if __name__ == '__main__':
    import time
    
    id_ls = []
    id_ls.append(be.Identity.make_identity('x', 'a*(-x)'))
    id_ls.append(be.Identity.make_identity('x', '-(a*x)'))
    id_ls.append(be.Identity.make_identity('a', '-(a*a)'))
    bun = be.Bunny({(0,0):0}, {0:0}, 0, 0, 0)
    table = [[bun.check_id(id_ls[i]) for i in range(len(id_ls))], ]
    cxt = fca.Context(table, [bun, ], id_ls)
    ae = AE(cxt, '/home/artreven/Dropbox/personal/Scripts/AptanaWorkspace/MIW/bunny_exploration/tests/p9m4_test')
    now = time.time()
    print ae.run()
    print time.time() - now
