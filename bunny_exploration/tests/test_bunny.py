'''
Use with Nosetests (https://nose.readthedocs.org/en/latest/)

Created on Apr 28, 2013

@author: artem
'''
import bunny_exploration
from bunny_exploration.bunny import *

class TestBunny:

    def setUp(self):
        f2_dict = {'condition1': (lambda x, y: True,
                                  lambda x, y: x)}
        f1_dict = {'condition1': (lambda x: True,
                                  lambda x: 0)}
        f0 = 0
        self.id1 = bunny_exploration.identity.Identity.make_identity('x',
                                                                     '-(x*a)')
        self.id2 = bunny_exploration.identity.Identity.make_identity('x',
                                                                     'x*a')
        self.bunny = Bunny(f2_dict, f1_dict, f0, 'N')

    def tearDown(self):
        pass


    def test_check_id(self):
        assert not self.bunny.check_id(self.id1, 20)
        assert self.bunny.check_id(self.id2, 20)
        
        
def natural_output(bunny, limit):
    def natural_value(x):
        return (x >= 0) and isinstance(x, int)
    for i in range(limit):
        for j in range(limit):
            f2_val = bunny.f2(i, j)
            if not natural_value(f2_val):
                print 'f2({0}, {1}) ='.format(i, j), f2_val
                print bunny.f2_dict
                print
                assert False
        f1_val = bunny.f1(i)
        assert natural_value(f1_val)


class TestInfBunny():
    
    def setup(self):
        f2_dict = {'condition1': (lambda x, y: True,
                                  lambda x, y: x)}
        f1_dict = {'condition1': (lambda x: True,
                                  lambda x: 0)}
        f0 = 0
        self.id1 = bunny_exploration.identity.Identity.make_identity('x',
                                                                     '-(x*a)')
        self.id2 = bunny_exploration.identity.Identity.make_identity('x',
                                                                     'x*a')
        self.bunny = InfBunny(f2_dict, f1_dict)
        print '\n\n !!!!!!!!!!!!Next Case'

    def teardown(self):
        pass

      
    def test_init(self):
        natural_output(self.bunny, 6)
        
    def test_find1(self):
        id1 = bunny_exploration.identity.Identity.make_identity('x', 'a*(-x)') #45
        id2 = bunny_exploration.identity.Identity.make_identity('x', '-(a*x)') #55
        bunny_found = InfBunny.find([id1,], id2, limit=4)
        assert bunny_found != None
        #entspricht G_1 - G_351
        print bunny_found.f2_dict
        print bunny_found.f1_dict
        natural_output(bunny_found, 6)
        
    def test_find2(self):
        id1 = bunny_exploration.identity.Identity.make_identity('x', 'a*(-x)') #45
        id2 = bunny_exploration.identity.Identity.make_identity('x', '-(a*x)') #55
        bunny_found = InfBunny.find([id2,], id1, limit=4)
        assert bunny_found != None
        assert bunny_found.check_id(id2, 6)
        assert not bunny_found.check_id(id1, 6)
        #entspricht G_352 - G_602
        print bunny_found.f2_dict
        print bunny_found.f1_dict
        natural_output(bunny_found, 6)
        
    def test_find3(self):
        id1 = bunny_exploration.identity.Identity.make_identity('a', '(-a)') #3
        id2 = bunny_exploration.identity.Identity.make_identity('a', '-(x*a)') #34
        id3 = bunny_exploration.identity.Identity.make_identity('x', '-(x*x)') #57
        idn = bunny_exploration.identity.Identity.make_identity('a', '(x*a)') #10
        #entspricht G_603 - G_618
        bunny_found = InfBunny.find([id1, id2, id3], idn, limit=4)
        assert bunny_found != None
        print bunny_found.f2_dict
        print bunny_found.f1_dict
        natural_output(bunny_found, 6)
        
    def test_find4(self):
        print '\ttest_find4\n'
        id32 = bunny_exploration.identity.Identity.make_identity('a', '-(a*a)')
        id37 = bunny_exploration.identity.Identity.make_identity('-a', '-(-a)')
        id57 = bunny_exploration.identity.Identity.make_identity('x', '-(x*x)')
        id1 = bunny_exploration.identity.Identity.make_identity('x', 'x')
        id22 = bunny_exploration.identity.Identity.make_identity('a', 'a*(-(a))')
        id24 = bunny_exploration.identity.Identity.make_identity('a', '(-a)*a')
        idn = bunny_exploration.identity.Identity.make_identity('x', 'y')
        #entspricht G_603 - G_618
        bunny_found = InfBunny.find([id1, id22, id24, id32, id37, id57], idn, limit=4)
        assert bunny_found != None
        print bunny_found.f2_dict
        print bunny_found.f1_dict
        natural_output(bunny_found, 6)