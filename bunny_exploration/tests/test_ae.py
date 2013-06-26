'''
Use with Nosetests (https://nose.readthedocs.org/en/latest/)

Created on Jun 7, 2013

@author: artreven
'''
import os.path
import shutil

import fca

from bunny_exploration.ae import *
import bunny_exploration as be

class Test:
    def setUp(self):
        id_ls = []
        id_ls.append(be.Identity.make_identity('x', 'a*(-x)'))
        id_ls.append(be.Identity.make_identity('x', '-(a*x)'))
        id_ls.append(be.Identity.make_identity('a', '-(a*a)'))
        bun = be.Bunny({(0,0):0}, {0:0}, 0, 0, 0)
        #bun_name = str(bun.index) + ' ' + str(bun.size)
        table = [[bun.check_id(id_ls[i]) for i in range(len(id_ls))], ]
        self.cxt = fca.Context(table, [bun, ], id_ls)
        self.ae = AE(self.cxt, os.path.expanduser('~') + '/Dropbox/personal/Scripts/AptanaWorkspace/MIW/bunny_exploration/tests/p9m4_test', 
                     be.prover9, be.ce_finder)

    def tearDown(self):
        shutil.rmtree(self.ae.dest)
        
    def test_prove(self):
        self.ae.find_basis()
        assert map(len, self.ae.prove(0)) == [0, 3]
        
    def test_run(self):
        assert map(len, self.ae.run((0, 1, 1), 2)) == [1, 0]