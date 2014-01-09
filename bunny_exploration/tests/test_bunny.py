'''
Use with Nosetests (https://nose.readthedocs.org/en/latest/)

Created on Apr 28, 2013

@author: artem
'''
from nose.tools import nottest, raises

import bunny_exploration
from bunny_exploration.bunny import *

class TestBunny:

    def setUp(self):
        f2_dict = {'condition1': (lambda x, y: True,
                                  lambda x, y: x)}
        f1_dict = {'condition1': (lambda x: True,
                                  lambda x: 0)}
        f0 = 0
        self.id1 = bunny_exploration.identity.Identity.make_identity('x=-(x*a)')
        self.id2 = bunny_exploration.identity.Identity.make_identity('x=x*a')
        self.bunny = Bunny(f2_dict, f1_dict, f0, 'N', 'Inf')

    def tearDown(self):
        pass


    def test_check_id(self):
        assert not self.bunny.check_id(self.id1, 10)
        assert self.bunny.check_id(self.id2, 10)
    
    def test_index(self):
        bun2 = bunnies(2)
        for b in bun2:
            assert (b.index ==
                    bunny_exploration.bunny._index(b.f2_dict, b.f1_dict, b.f0_dict, b.size))
        ind = 50
        b = show(ind, 3)
        assert bunny_exploration.bunny._index(b.f2_dict, b.f1_dict, b.f0_dict, 3) == ind


class TestInfBunny():
    
    def setup(self):
        f2_dict = {(0, 0): 0, (0, 1): 0,
                   (1, 0): 1,
                   'condition1': (lambda x, y: True,
                                  lambda x, y: x)}
        f1_dict = {0: 1,
                   'condition1': (lambda x: True,
                                  lambda x: 0)}
        f0 = 0
        self.bunny = InfBunny(f2_dict, f1_dict)
        
        f2_dict2 = {(0, 0): 0, (0, 1): 0,
                    (1, 0): 1}
        self.bunny2 = InfBunny(f2_dict2, f1_dict)
        
        self.id1 = bunny_exploration.identity.Identity.make_identity('x=-(x*a)')
        self.id2 = bunny_exploration.identity.Identity.make_identity('x=x*a')
        print '\n\n !!!!!!!!!!!!Next Case'

    def teardown(self):
        pass
        
    def test_check_id(self):
        assert not self.bunny.check_id(self.id1, 6)
        assert self.bunny.check_id(self.id2, 6)
        
    @raises(bunny_exploration.identity.NoneValueError)
    def test_check_id_bad_partial(self):
        self.bunny2.check_id(self.id2, 6)
        
    def test_partial(self):
        assert not self.bunny2.check_id(self.id1, 6, True)[0]
        assert len(self.bunny2.check_id(self.id1, 6, True)[1]) == 4
        assert self.bunny2.check_id(self.id2, 6, True)[0] == None
        assert len(self.bunny2.check_id(self.id2, 6, True)[1]) == 4
        
    def test_generate(self):
        d = {(0, 0): 0, (0, 1): 1}
        f2 = generate_f(d)
        try:
            f2(2, 0)
        except ArgError:
            pass
        else:
            assert False
        assert f2(0, 0) == 0
        
    @nottest
    def test_repr(self):
        id1 = bunny_exploration.identity.Identity.make_identity('x=a*(-x)') #45
        id2 = bunny_exploration.identity.Identity.make_identity('x=-(a*x)') #55
        bunny_found = InfBunny.find([id1,], id2, limit=4, t_limit=15)
        #print bunny_found        
        
    @nottest
    def test_find1(self):
        id1 = bunny_exploration.identity.Identity.make_identity('x=a*(-x)') #45
        id2 = bunny_exploration.identity.Identity.make_identity('x=-(a*x)') #55
        bunny_found = InfBunny.find([id1,], id2, limit=4, t_limit=15)
        assert bunny_found != None
        #entspricht G_1 - G_351
        #print bunny_found.f2_dict
        #print bunny_found.f1_dict
        
    @nottest
    def test_find2(self):
        id1 = bunny_exploration.identity.Identity.make_identity('x=a*(-x)') #45
        id2 = bunny_exploration.identity.Identity.make_identity('x=-(a*x)') #55
        bunny_found = InfBunny.find([id2,], id1, limit=4, t_limit=15)
        assert bunny_found != None
        assert bunny_found.check_id(id2, 6)
        assert not bunny_found.check_id(id1, 6)
        #entspricht G_352 - G_602
        #print bunny_found.f2_dict
        #print bunny_found.f1_dict
        
    @nottest
    def test_find3(self):
        id1 = bunny_exploration.identity.Identity.make_identity('a=(-a)') #3
        id2 = bunny_exploration.identity.Identity.make_identity('a=-(x*a)') #34
        id3 = bunny_exploration.identity.Identity.make_identity('x=-(x*x)') #57
        idn = bunny_exploration.identity.Identity.make_identity('a=(x*a)') #10
        #entspricht G_603 - G_618
        bunny_found = InfBunny.find([id1, id2, id3], idn, limit=4, t_limit=15)
        assert bunny_found != None
        #print bunny_found.f2_dict
        #print bunny_found.f1_dict
        
    @nottest
    def test_find4(self):
        print '\ttest_find4\n'
        id32 = bunny_exploration.identity.Identity.make_identity('a=-(a*a)')
        id37 = bunny_exploration.identity.Identity.make_identity('-a=-(-a)')
        id57 = bunny_exploration.identity.Identity.make_identity('x=-(x*x)')
        id1 = bunny_exploration.identity.Identity.make_identity('x=x')
        id22 = bunny_exploration.identity.Identity.make_identity('a=a*(-(a))')
        id24 = bunny_exploration.identity.Identity.make_identity('a=(-a)*a')
        idn = bunny_exploration.identity.Identity.make_identity('x=y')
        #entspricht G_603 - G_618
        bunny_found = InfBunny.find([id1, id22, id24, id32, id37, id57], idn, limit=4, t_limit=120)
        assert bunny_found != None
        #print bunny_found.f2_dict
        #print bunny_found.f1_dict
        
    @nottest
    def test_find5(self):
        print '\ttest_find5\n'
        #x = (-x)*y => x = -(x*y)
        id58 = bunny_exploration.Identity.make_identity('x=-(x*y)')
        id53 = bunny_exploration.Identity.make_identity('x=(-x)*y')        
        bunny_found = InfBunny.find([id53, ], id58, limit=8, t_limit=15)
        assert bunny_found != None
    
    @nottest    
    def test_find6(self):
        print '\ttest_find6\n'
        # [a = x*(-a), x = x, x = x*(-x), x = a*(-x), x = x*a, a = a*(-a), a = a*a] => -a = x*y

        id1 = bunny_exploration.Identity.make_identity('a=x*(-a)')
        id2 = bunny_exploration.Identity.make_identity('x=x')
        id3 = bunny_exploration.Identity.make_identity('x=x*(-x)')
        id4 = bunny_exploration.Identity.make_identity('x=a*(-x)')
        id5 = bunny_exploration.Identity.make_identity('x=x*a')
        id6 = bunny_exploration.Identity.make_identity('a=a*(-a)')
        id7 = bunny_exploration.Identity.make_identity('a=a*a')
        idn = bunny_exploration.Identity.make_identity('-a=x*y')
        bunny_found = InfBunny.find([id1, id2, id3, id5, id6, id7], idn, limit=8, t_limit=65)
        assert bunny_found != None
        
    @nottest
    def test_find7(self):
        print '\ttest_find7\n'
        id27 = bunny_exploration.Identity.make_identity('a=x*(-x)')
        id31 = bunny_exploration.Identity.make_identity('a=(-x)*y')
        id45 = bunny_exploration.Identity.make_identity('x=a*(-x)')
        idn = bunny_exploration.Identity.make_identity('x=y')
        bunny_found = InfBunny.find([id27, id31, id45], idn, limit=8, t_limit=160)
        assert bunny_found != None
        
    @nottest
    def test_find8(self):
        print '\ttest_find8\n'
        id22 = bunny_exploration.Identity.make_identity('a=a*(-a)')
        id59 = bunny_exploration.Identity.make_identity('x=-(y*x)')
        bunny_found = InfBunny.find([id59, ], id22, limit=8, t_limit=10)
        f2 = {'condition1': (lambda m, n: True, 
                             lambda m, n: n + 1,
                             'True',
                             'n + 1')}
        f1 = {'condition1': (lambda n: n >= 1, 
                             lambda n: n - 1,
                             'n >= 1',
                             'n - 1'),
              0: 1}
        bun = InfBunny(f2, f1)
        check59 = bun.check_id(id59, 8)
        check22 = bun.check_id(id22, 8)
        print check59, check22
        assert bunny_found != None
        
    @nottest
    def test_find9(self):
        #a = -(a*a), a = (-a)*a, x = x, x = (-x)*x, x = (-x)*a, x = x*(-x), a = a*(-a) => a = a*a
        print '\ttest_find9\n'
        
        id22 = bunny_exploration.Identity.make_identity('a=a*(-a)')
        id24 = bunny_exploration.Identity.make_identity('a=(-a)*a')
        id32 = bunny_exploration.Identity.make_identity('a=-(a*a)')
        id47 = bunny_exploration.Identity.make_identity('x=x*(-x)')
        id51 = bunny_exploration.Identity.make_identity('x=(-x)*a')
        id52 = bunny_exploration.Identity.make_identity('x=(-x)*x')
        
        id8 = bunny_exploration.Identity.make_identity('a=a*a')
        
        bunny_found = InfBunny.find([id22, id24, id32, id47, id51, id52], id8, limit=8, t_limit=100)
        assert bunny_found != None
    
    @nottest    
    def test_find10(self):
        #a = -(a*a), a = a*(-a), x = x*(-x), x = -(x*x), x = x, x = (-x)*x, a = (-a)*a, -a = -(-a) => a = -(-a)
        print '\ttest_find10\n'
        
        id22 = bunny_exploration.Identity.make_identity('a=a*(-a)')
        id24 = bunny_exploration.Identity.make_identity('a=(-a)*a')
        id32 = bunny_exploration.Identity.make_identity('a=-(a*a)')
        id37 = bunny_exploration.Identity.make_identity('-a=-(-a)')
        id47 = bunny_exploration.Identity.make_identity('x=x*(-x)')
        id52 = bunny_exploration.Identity.make_identity('x=(-x)*x')
        id57 = bunny_exploration.Identity.make_identity('x=-(x*x)')
        
        id6 = bunny_exploration.Identity.make_identity('a=-(-a)')
        
        bunny_found = InfBunny.find([id22, id24, id32, id32, id47, id52, id57], id6, limit=8, t_limit=100)
        assert bunny_found != None
    
    @nottest    
    def test_find11(self):
        #a = (-a)*a, a = -(-(-a)), a = -(-a), a = x*x, x = x*(-x), x = (-x)*x,
        #a = -(x*x), a = a*(-a), a = -(a*a), x = x, a = a*a, -a = -(-a), x = -(a*x), -a = x*x, a = -a, -a = a*a => x = a*(-x)
        print '\ttest_find11\n'
        
        id3  = bunny_exploration.Identity.make_identity('a=-a')
        id6  = bunny_exploration.Identity.make_identity('a=-(-a)')
        id8  = bunny_exploration.Identity.make_identity('a=a*a')
        id11 = bunny_exploration.Identity.make_identity('a=x*x')
        id22 = bunny_exploration.Identity.make_identity('a=a*(-a)')
        id20 = bunny_exploration.Identity.make_identity('a=-(-(-a))')
        id24 = bunny_exploration.Identity.make_identity('a=(-a)*a')
        id32 = bunny_exploration.Identity.make_identity('a=-(a*a)')
        id35 = bunny_exploration.Identity.make_identity('a=-(x*x)')
        id37 = bunny_exploration.Identity.make_identity('-a=-(-a)')
        id39 = bunny_exploration.Identity.make_identity('-a=a*a')
        id42 = bunny_exploration.Identity.make_identity('-a=x*x')
        id47 = bunny_exploration.Identity.make_identity('x=x*(-x)')
        id52 = bunny_exploration.Identity.make_identity('x=(-x)*x')
        id55 = bunny_exploration.Identity.make_identity('x=-(a*x)')
        
        id45 = bunny_exploration.Identity.make_identity('x=a*(-x)')
        
        bunny_found = InfBunny.find([id3, id11, id35, id42, id47, id52, id55], None, limit=8, t_limit=200)
        
        f2 = {'condition1': (lambda m, n: m == n, 
                             lambda m, n: 0,
                             'm == n',
                             '0'),
              'condition2': (lambda m, n: (m == 1 and n == 3) or (m == 3 and n == 1), 
                             lambda m, n: 1,
                             '(m == 1 and n == 3) or (m == 3 and n == 1)',
                             '1'),
              'condition3': (lambda m, n: (m != 0 and (n == 0 or n == m + 1)), 
                             lambda m, n: m + 1,
                             '(m != 0 and (n == 0 or n == m + 1))',
                             'm + 1'),
              'condition4': (lambda m, n: True, 
                             lambda m, n: n + 1,
                             'else',
                             'n + 1')}
        f1 = {'condition1': (lambda n: n >= 1, 
                             lambda n: n - 1,
                             'n >= 1',
                             'n - 1'),
              0: 0, 1: 3}
        bun = InfBunny(f2, f1)
        print bun.check_id(id3, 8, True), bun.check_id(id11, 8, True), bun.check_id(id35, 8, True), bun.check_id(id42, 8, True), bun.check_id(id47, 8, True), bun.check_id(id52, 8, True), bun.check_id(id55, 8, True)
        print bun.check_id(id45, 8, True)
        assert bunny_found != None
    
    @nottest    
    def test_find12(self):
        print '\ttest_find12\n'
        
        id20 = bunny_exploration.Identity.make_identity('a=-(-(-a))')
        id22 = bunny_exploration.Identity.make_identity('a=a*(-a)')
        id24 = bunny_exploration.Identity.make_identity('a=(-a)*a')
        id32 = bunny_exploration.Identity.make_identity('a=-(a*a)')
        id45 = bunny_exploration.Identity.make_identity('x=a*(-x)')
        id50 = bunny_exploration.Identity.make_identity('x=(-a)*x')
        
        id55 = bunny_exploration.Identity.make_identity('x=-(a*x)')
        
        bunny_found = InfBunny.find([id20, id22, id24, id32, id45, id50], id55, limit=8, t_limit=200)
        assert bunny_found != None
    
    @nottest    
    def test_find13(self):
        print '\ttest_find13\n'
        
        id6  = bunny_exploration.Identity.make_identity('a=-(-a)')
        id24 = bunny_exploration.Identity.make_identity('a=(-a)*a')
        id25 = bunny_exploration.Identity.make_identity('a=(-a)*x')
        id32 = bunny_exploration.Identity.make_identity('a=-(a*a)')
        id52 = bunny_exploration.Identity.make_identity('x=(-x)*x')
        id57 = bunny_exploration.Identity.make_identity('x=-(x*x)')
        
        id39 = bunny_exploration.Identity.make_identity('-a=a*a')
        
        bunny_found = InfBunny.find([id6, id24, id25, id32, id52, id57], id39, limit=8, t_limit=10)
        assert bunny_found != None
    
    @nottest    
    def test_find14(self):
        print '\ttest_find14\n'
        
        id6  = bunny_exploration.Identity.make_identity('a=-(-a)')
        id24 = bunny_exploration.Identity.make_identity('a=(-a)*a')
        id25 = bunny_exploration.Identity.make_identity('a=(-a)*x')
        id32 = bunny_exploration.Identity.make_identity('a=-(a*a)')
        id33 = bunny_exploration.Identity.make_identity('a=-(a*x)')
        id39 = bunny_exploration.Identity.make_identity('-a=a*a')
        id52 = bunny_exploration.Identity.make_identity('x=(-x)*x')
        id57 = bunny_exploration.Identity.make_identity('x=-(x*x)')
        
        id40 = bunny_exploration.Identity.make_identity('-a=a*x')
        
        bunny_found = InfBunny.find([id6, id24, id25, id32, id39, id52, id57], id40, limit=8, t_limit=10)
        assert bunny_found != None
    
    @nottest    
    def test_find15(self):
        print '\ttest_find15\n'
        id6 = bunny_exploration.Identity.make_identity('a=-(-a)')
        id22 = bunny_exploration.Identity.make_identity('a=a*(-a)')
        id24 = bunny_exploration.Identity.make_identity('a=(-a)*a')
        id27 = bunny_exploration.Identity.make_identity('a=x*(-x)')
        id32 = bunny_exploration.Identity.make_identity('a=-(a*a)')
        id39 = bunny_exploration.Identity.make_identity('-a=a*a')
        id46 = bunny_exploration.Identity.make_identity('x=x*(-a)')
        id50 = bunny_exploration.Identity.make_identity('x=(-a)*x')
        id55 = bunny_exploration.Identity.make_identity('x=-(a*x)')
        
        id45 = bunny_exploration.Identity.make_identity('x=a*(-x)')
        
        bunny_found = InfBunny.find([id6, id22, id24, id27, id32, id39, id46, id50, id55], id45, limit=8, t_limit=150)
        assert bunny_found != None
    
    @nottest    
    def test_find16(self):
        print '\ttest_find16\n'
        id20 = bunny_exploration.Identity.make_identity('a=-(-(-a))')
        id24 = bunny_exploration.Identity.make_identity('a=(-a)*a')
        id32 = bunny_exploration.Identity.make_identity('a=-(a*a)')
        id33 = bunny_exploration.Identity.make_identity('a=-(a*x)')
        id50 = bunny_exploration.Identity.make_identity('x=(-a)*x')
        id51 = bunny_exploration.Identity.make_identity('x=(-x)*a')
        
        id56 = bunny_exploration.Identity.make_identity('x=-(x*a)')
        
        bunny_found = InfBunny.find([id20, id24, id32, id33, id50, id51], id56, limit=8, t_limit=150)
        assert bunny_found != None
    
    @nottest    
    def test_find17(self):
        be = bunny_exploration
        print '\ttest_find17\n'
        id6 = be.Identity.make_identity('a=-(-a)')
        id22 = be.Identity.make_identity('a=a*(-a)')
        id24 = be.Identity.make_identity('a=(-a)*a')
        id30 = be.Identity.make_identity('a=(-x)*x')
        id32 = be.Identity.make_identity('a=-(a*a)')
        id39 = be.Identity.make_identity('-a=a*a')
        id50 = be.Identity.make_identity('x=(-a)*x')
        id55 = be.Identity.make_identity('x=-(a*x)')
        id64 = be.Identity.make_identity('-x=x*a')

        id45 = be.Identity.make_identity('x=a*(-x)')
        
        id_pos_ls = [id6, id22, id24, id30, id32, id39, id50, id55, id64] #id25, id33
        bunny_found = InfBunny.find(id_pos_ls, id45, limit=8, t_limit=500)
        assert bunny_found != None
    
    @nottest    
    def test_find18(self):
        be = bunny_exploration
        print '\ttest_find18\n'
        id6 = be.Identity.make_identity('a=-(-a)')
        id22 = be.Identity.make_identity('a=a*(-a)')
        id26 = be.Identity.make_identity('a=x*(-a)')
        id32 = be.Identity.make_identity('a=-(a*a)')
        id34 = be.Identity.make_identity('a=-(x*a)')
        id39 = be.Identity.make_identity('-a=a*a')
        id47 = be.Identity.make_identity('x=x*(-x)')
        id55 = be.Identity.make_identity('x=-(a*x)')
        id65 = be.Identity.make_identity('-x=x*x')
        
        id41 = be.Identity.make_identity('-a=x*a')
        
        id_pos_ls = [id6, id22, id26, id32, id34, id39, id47, id55, id65]
        bunny_found = InfBunny.find(id_pos_ls, id41, limit=8, t_limit=100)
        assert bunny_found != None