'''
Created on Jun 6, 2013

@author: artreven
'''
import os
import time
import shutil
import copy

import fca

import bunny_exploration as be

class AE(object):
    '''
    Class to represent Attribute Exploration procedure
    '''

    def __init__(self, cxt, dest, prover, ce_finder):
        '''
        Constructor
        
        @param cxt: initial cxt to start with
        @param dest: proposed destination for current AE. May be changed,
        see implementation.
        @param ce_finder: should output dictionary implication: counter-example.
        Every counter example should have method has_attribute accepting attribute
        from the context.
        @param prover: should output (self.proved, self.not_proved)
        @ivar proved: proved implications from *current* basis
        @ivar not proved: not proved yet implications from *current* basis
        @ivar step: current step of AE
        '''
        self.cxt = cxt
        #self.basis = None
        self.proved = []
        self.not_proved = []
        self.dest = def_dest(dest)
        self.prover = prover
        self.ce_finder = ce_finder
        # Remove progress left from previous runs
        self.step = 0
        try:
            os.remove(self.dest + '/progress.txt')
        except OSError:
            pass
        # Create directories for proofs and counter-examples
        if os.path.exists(self.dest + '/proofs'):
            shutil.rmtree(self.dest + '/proofs')
        os.makedirs(self.dest + '/proofs')
        if os.path.exists(self.dest + '/ces'):
            shutil.rmtree(self.dest + '/ces')
        os.makedirs(self.dest + '/ces')
        
    def find_basis(self):
        """
        Find implication basis and save it in self.basis in unit form
        """
        ts = time.time()
        basis = self.cxt.attribute_implications
        te = time.time()
        m = '\nIt took {0} seconds to compute the canonical basis.\n'.format(te-ts)
        print m
        with open(self.dest + '/progress.txt', 'a') as f:
            f.write(m)
        f.close()
        unit_basis = []
        for imp in basis:
            for j in (imp.conclusion - imp.premise):
                unit_basis.append(fca.Implication(imp.premise, set((j,))))
        self.not_proved = copy.deepcopy(unit_basis)
        self.proved = []
        return unit_basis
            
    def _delete_ces(self):
        """
        Delete all files output by ce_finder
        """
        for i in os.listdir(self.dest + '/ces'):
            os.remove(self.dest + '/ces/' + i)
                
    def _delete_proofs(self):
        """
        Delete all files output by prover
        """
        for i in os.listdir(self.dest + '/proofs'):
            os.remove(self.dest + '/proofs/' + i)
                
    def _clear_directory(self):
        self._delete_ces()
        self._delete_proofs()
        
    def _output_imps(self):
        with open(self.dest + '/proved.txt', 'w') as f:
            f.write('Proved Implications:\n')
            for imp in self.proved:
                f.write(str(imp) + '\n')
        f.close()
        with open(self.dest + '/not_proved.txt', 'w') as f:
            f.write('Not Proved Implications:\n')
            for imp in self.not_proved:
                f.write(str(imp) + '\n')
        f.close()
        
    def _output_cxt(self):
        with open(self.dest + '/cxt.txt', 'w') as f:
            f.write(str(self.cxt) + '\n')
        f.close()
        
    def add_object(self, row, object_name):
        self.cxt.add_object(row, object_name)
        self.not_proved = None
        self.proved = None
        
    def add_attribute(self, col, attr_name):
        self.cxt.add_attribute(self, col, attr_name)
        self.not_proved = None
        self.proved = None
        
    def prove(self, wait):
        """
        Run self.prover on not proved implications, record progress (timing of
        finding basis and work of prover).
        
        @param wait: time limit to wait for a proof
        """
        self._delete_proofs()
        ts = time.time()
        proved, not_proved = self.prover(self.not_proved, self.dest + '/proofs',
                                         wait)
        te = time.time() - ts
        for imp in proved:
            self.proved.append(imp)
            self.not_proved.remove(imp)
        assert self.not_proved == not_proved
        # construct message
        m = '\n\n\n\tPROOF PHASE:\n'
        m += 'It took {0} seconds\n'.format(te)
        m += '{0} unit implication proved\n'.format(len(self.proved))
        m += '{0} unit implication not proved\n'.format(len(self.not_proved))
        #print
        with open(self.dest + '/progress.txt', 'a') as f:
            f.write(m)
        f.close()
        self._output_imps()
        print m
        return (self.proved, self.not_proved)
    
    def find_ces(self, wait):
        """
        Try to find counter-examples for every implication and add them if found.
        Reduces objects in the context after adding counter-examples.
        
        @param wait: tuple of time limits for self.ce_finder
        @var ce_dict: dictionary {implication: counter-example}.
        Every counter example should have method has_attribute accepting
        attributes from the context.
        """
        self._delete_ces()
        self.step += 1
        ts = time.time()
        ce_dict = self.ce_finder(self.not_proved, self.dest, wait)
        # number of objects and implications before start for records
        no_objs = len(self.cxt.objects)
        no_imps = len(self.not_proved)
        for ce in ce_dict.values():
            if ce != None:
                row = [ce.has_attribute(att) for att in self.cxt.attributes]
                self.add_object(row, ce)
        self.cxt = self.cxt.reduce_objects()
        te = time.time() - ts
        # construct message
        m = '\n\n\n\tCOUNTER-EXAMPLE FINDING PHASE: STEP {0}\n'.format(self.step)
        m += 'It took {0} seconds.\n'.format(te)
        m += 'Run on {0} atomic implications.\n'.format(no_imps)
        m += 'There were {0} objects before the start of this step\n'.format(no_objs)
        m += 'There were {0} counter-examples found on this step\n'.format(len([x for x in ce_dict.values() if x != None]))
        self.cxt = self.cxt.reduce_objects()
        m += '{0} Objects left after reducing\n'.format(len(self.cxt.objects))
        # print
        with open(self.dest + '/progress.txt', 'a') as f:
            f.write(m)
        f.close()
        with open(self.dest + '/step{0}ces.txt'.format(self.step), 'w') as f:
            f.write('\tCounter-examples:\n')
            for imp, ce in ce_dict.items():
                f.write(str(imp) + '\n' + str(ce) + '\n\n')
            f.write('\n\n\n\t Context:\n' + str(self.cxt))
        f.close()
        print m
        return ce_dict
    
    def run(self, ce_wait, prove_wait):
        """
        Run Attribute Exploration procedure till no other counter-examples
        can be found. Try to prove, return proved and not proved implications.
        
        @param ce_wait: tuple of how long to wait for ces.
        @param prove_wait: tuple of how long to wait for proofs.
        """
        # try to find counter-examples
        ts = time.time()
        self.find_basis()
        ce_dict = self.find_ces(ce_wait)
        te = time.time()
        m = '_'*80 + '\n'
        m += '\tSTEP TIME: {0} sec\n\n\n'.format(te - ts)
        print m
        with open(self.dest + '/progress.txt', 'a') as f:
            f.write(m)
        f.close()
        # if no CE found try to prove
        if (not any(ce_dict.values())):
            self._output_cxt()
            return self.prove(prove_wait)
        # if CE found proceed to next step
        return self.run(ce_wait, prove_wait)
    
def def_dest(dest):
    """
    Create a new directory or modify name (if exists) and create.
    """
    if os.path.exists(dest):
        new_dest = dest + '1'
        return def_dest(new_dest)
    elif not os.path.exists(dest):
        os.makedirs(dest)
        return dest
    
########################################################
if __name__ == '__main__':
    pass