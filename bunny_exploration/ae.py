'''
Created on Jun 6, 2013

@author: artreven
'''

class AE(object):
    '''
    Class to represent Attribute Exploration procedure
    '''

    def __init__(self, cxt):
        '''
        Constructor
        '''
        self.cxt = cxt
        self.basis = None
        self.proved = []