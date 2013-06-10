'''
Use with Nosetests (https://nose.readthedocs.org/en/latest/)

Created on Jun 7, 2013

@author: artreven
'''
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
        self.ae = AE(self.cxt, '/home/artreven/Dropbox/personal/Scripts/AptanaWorkspace/MIW/bunny_exploration/tests/p9m4_test')

    def tearDown(self):
        pass


    def test_find_basis(self):
        assert self.ae.basis == None
        assert self.ae.find_basis() == self.cxt.attribute_implications
        assert self.ae.basis == self.cxt.attribute_implications
        
    def test_mace(self):
        assert self.ae.mace() == 3
        assert len(self.cxt.objects) == 4
        print self.ae.cxt
        
    def test_prove(self):
        assert map(len, self.ae.prove()) == [0, 3]
        
    def test_find_inf_ce(self):
        self.ae.mace()
        assert map(len, self.ae.prove()) == [1, 3]
        N = 0
        for i in self.ae.find_inf_ce().items():
            if i[1] != None:
                N += 1
        assert N >= 0
        assert len(self.ae.cxt.objects) == 6 
        assert self.ae.basis == None
        
    def test_run(self):
        print self.ae.run()