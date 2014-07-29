'''
Use with Nosetests (https://nose.readthedocs.org/en/latest/)

Created on Jun 7, 2013

@author: artreven
'''

import os.path
import shutil

import fca

import auto_ae.ae
import bunny.identity, bunny.p9m4, bunny.main

class Test:
    def setUp(self):
        id_ls = []
        id_ls.append(bunny.identity.Identity.make_identity('x=a*(-x)'))
        id_ls.append(bunny.identity.Identity.make_identity('x=-(a*x)'))
        id_ls.append(bunny.identity.Identity.make_identity('a=-(a*a)'))
        bun = bunny.bunny.Bunny({(0, 0):0}, {0:0}, 0, 0, 0)
        # bun_name = str(bun.index) + ' ' + str(bun.size)
        table = [[bun.check_id(id_ls[i]) for i in range(len(id_ls))], ]
        self.cxt = fca.Context(table, [bun, ], id_ls)
        self.ae = auto_ae.ae.AE((os.path.expanduser('~') + 
'/Dropbox/personal/Scripts/AptanaWorkspace/MIW/bunny_exploration/tests/p9m4_test'),
                                self.cxt, bunny.p9m4.prover9, bunny.main.ce_finder)

    def tearDown(self):
        shutil.rmtree(self.ae.dest)
        
    def test_prove(self):
        self.ae.find_basis()
        assert map(len, self.ae.prove(0)) == [0, 3]
        
    def test_run(self):
        assert map(len, self.ae.run((0, 1, 1), 2)) == [1, 0]
