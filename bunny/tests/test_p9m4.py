'''
Use with Nosetests (https://nose.readthedocs.org/en/latest/)

Created on Jul 29, 2014

@author: artreven
'''
import os
import sys

import fca
import bunny.identity, bunny.p9m4, bunny.bunny

class Test:

    def setUp(self):
        self.cwd = os.getcwd()
        id1 = bunny.identity.Identity.make_identity("-x = y*z")
        id2 = bunny.identity.Identity.make_identity("x = x")
        id3 = bunny.identity.Identity.make_identity("-x = -(-x)")
        self.imp1 = fca.Implication({id1, id2}, {id3})
        
        str_ids = "a = -(a*a), a = a*(-a), x = -(x*a), a = -(-a), x = -(x*x), a = x*(-a), -x = a*x, -a = a*a, x = x".split(",")
        premise2 = map(bunny.identity.Identity.make_identity, str_ids)
        str_ids = ["a = x*(-x)", "x = (-x)*a"]
        conclusion2 = map(bunny.identity.Identity.make_identity, str_ids)
        self.imp2 = fca.Implication(set(premise2), set(conclusion2))

    def tearDown(self):
        pass

    def test_prove1(self):
        assert not bunny.p9m4.mace4(self.imp1, self.cwd + r'/prove1', wait_time=1)[0]
        
    def test_ce1(self):
        assert bunny.p9m4.mace4(self.imp2, self.cwd + r'/ce1', wait_time=1)[0]
        os.remove(self.cwd + r'/ce1.mace4.out')