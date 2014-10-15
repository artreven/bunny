'''
Use with Nosetests (https://nose.readthedocs.org/en/latest/)

Created on Apr 28, 2013

@author: artem
'''
from nose.tools import nottest, raises

import fca

import bunny.identity, bunny.bunny

class TestVariable:    
    def setUp(self):
        self.v1 = bunny.bunny.Variable(5)
        self.v2 = bunny.bunny.Variable()
        self.v3 = bunny.bunny.Variable()

    def tearDown(self):
        pass
        
    def test_eq(self):
        assert self.v1 == 5
        assert self.v2.value == None
        self.v2.value = 5
        assert self.v1 == self.v2
        self.v2.value = 6
        assert not self.v1 == 6
        assert not self.v1 == self.v2
        assert not bunny.bunny.Variable() == bunny.bunny.Variable()
        
    def test_identify(self):
        self.v2.identify(self.v1)
        assert self.v2 == 5
        self.v2.value = 8
        assert self.v1 == 8
        self.v3.identify(self.v1)
        assert self.v3 == 8
        
    def test_str_diff(self):
        varn = bunny.bunny.Variable('n-1')
        varn1 = bunny.bunny.Variable('n+1')
        assert varn1 - varn == 2
        assert varn - varn1 == -2
        
    def test_str_diff2(self):
        varn1 = bunny.bunny.Variable('n+1')
        assert varn1 - 2 == 'n-1'
        
    def test_compare(self):
        assert not bunny.bunny.Variable('n') == bunny.bunny.Variable(0)
        assert not bunny.bunny.Variable(0) == bunny.bunny.Variable('n')
        tricky_val = bunny.bunny.Variable(0)
        tricky_val.vary = True
        assert not bunny.bunny.Variable('n') == tricky_val
        assert not tricky_val == bunny.bunny.Variable('n') 
        
class TestPFunc:    
    def setUp(self):
        varn = bunny.bunny.Variable('n')
        varn_1 = bunny.bunny.Variable('n-1')
        graph = ((varn, bunny.bunny.Variable(0), varn_1),)
        self.f1 = bunny.bunny.PiecewiseFunc('f', graph)
        varn = bunny.bunny.Variable('n')
        graph = ((varn, varn, varn_1),)
        self.f2 = bunny.bunny.PiecewiseFunc('f', graph)
    
    @raises(bunny.bunny.ArgError)
    def test_output1(self):
        self.f2(0, bunny.bunny.Variable('n+1'))
        
    @raises(bunny.bunny.ArgError)
    def test_output2(self):
        self.f2(9, 0)
        
    @raises(bunny.bunny.ArgError)
    def test_output3(self):
        print self.f1(bunny.bunny.Variable('n'), bunny.bunny.Variable('n'))
        
    def test_duplicates(self):
        varn1 = bunny.bunny.Variable('n+1')
        assert self.f1(varn1, 0) == 'n'
        assert self.f1(bunny.bunny.Variable('n+1'), 0) == 'n'
        
def test_consistency():
    val = bunny.bunny.Value
    f2_graph = [(val(0), val('n'), val('n-1')), (val(0), val(0), val(0)),
                (val('n'), val('n'), val(0)), (val('n'), val(0), val('n'))]
    f2 = bunny.bunny.PiecewiseFunc('f2', f2_graph)
    f1_graph = [(val('n'), val(0)), (val(0), val(0)), (val('n-1'), val('n'))]
    f1 = bunny.bunny.PiecewiseFunc('f1', f1_graph)
    bun = bunny.bunny.InfBunny(f2, f1, bunny.bunny.Value(0))
    assert not bunny.bunny.check_consistency(bun, limit=5)

class TestBunny:

    def setUp(self):
        f2_dict = {(0, 1): 1, (0, 0): 0,
                   (1, 1): 1, (1, 0): 0}
        f1_dict = {0: 1, 1: 1}
        f0 = 0
        self.id1 = bunny.identity.Identity.make_identity('x=-(x*a)')
        self.id2 = bunny.identity.Identity.make_identity('x=x*a')
        self.bunny = bunny.bunny.Bunny.dicts2bunny(f2_dict, f1_dict, f0)

    def tearDown(self):
        pass

    def test_check_id(self):
        assert self.bunny.check_id(self.id2) == self.bunny.check_id(self.id1)
    
    def test_index(self):
        bun2 = bunny.bunny.bunnies(2)
        for b in bun2:
            assert (b.index ==
                    bunny.bunny._index(b.f2.dict, b.f1.dict, b.f0, b.size))
        ind = 50
        b = bunny.bunny.show(ind, 3)
        assert bunny.bunny._index(b.f2.dict, b.f1.dict, b.f0, 3) == ind


class TestInfBunny():
    
    def test_find101(self):
        print '\ttest_find101\n'
        id1 = bunny.identity.Identity.make_identity('x=a*(-x)') #45
        id2 = bunny.identity.Identity.make_identity('x=-(a*x)') #55
        imp = fca.Implication({id1}, {id2})
        bunny_found = bunny.bunny.InfBunny.find(imp, wait_time=30, kern_size=4)[0]
        assert bunny_found != None
        assert bunny_found.check_id(id1, 10)
        assert not bunny_found.check_id(id2, 10)
        #entspricht G_1 - G_351
        #print bunny_found.f2_dict
        #print bunny_found.f1_dict
        
    def test_find102(self):
        print '\ttest_find102\n'
        id45 = bunny.identity.Identity.make_identity('x=a*(-x)') #45
        id50 = bunny.identity.Identity.make_identity('x=(-a)*x')
        id55 = bunny.identity.Identity.make_identity('x=-(a*x)') #55
        imp = fca.Implication({id45, id50}, {id55})
        bunny_found = bunny.bunny.InfBunny.find(imp, wait_time=30, kern_size=4)[0]
        assert bunny_found != None
        assert bunny_found.check_id(id45, 10)
        assert not bunny_found.check_id(id55, 10)
        #entspricht G_1 - G_351
        #print bunny_found.f2_dict
        #print bunny_found.f1_dict
        
    def test_find103(self):
        print '\ttest_find103\n'
        id1 = bunny.identity.Identity.make_identity('x=a*(-x)') #45
        id2 = bunny.identity.Identity.make_identity('x=-(a*x)') #55
        imp = fca.Implication({id2}, {id1})
        bunny_found = bunny.bunny.InfBunny.find(imp, wait_time=30, kern_size=4)[0]
        assert bunny_found != None
        assert bunny_found.check_id(id2, 10)
        assert not bunny_found.check_id(id1, 10)
        #entspricht G_352 - G_602
        #print bunny_found.f2_dict
        #print bunny_found.f1_dict
        
    def test_find104(self):
        print '\ttest_find104\n'
        id1 = bunny.identity.Identity.make_identity('a=(-a)') #3
        id2 = bunny.identity.Identity.make_identity('a=-(x*a)') #34
        id3 = bunny.identity.Identity.make_identity('x=-(x*x)') #57
        idn = bunny.identity.Identity.make_identity('a=(x*a)') #10
        #entspricht G_603 - G_618
        imp = fca.Implication({id1, id2, id3}, {idn})
        bunny_found = bunny.bunny.InfBunny.find(imp, wait_time=3, kern_size=4)[0]
        assert bunny_found != None
        assert bunny_found.check_id(id1, 10)
        assert bunny_found.check_id(id2, 10)
        assert bunny_found.check_id(id3, 10)
        assert not bunny_found.check_id(idn, 10)
        #print bunny_found.f2_dict
        #print bunny_found.f1_dict
    
    def test_find201(self):
        print '\ttest_find201\n'
        
        id20 = bunny.identity.Identity.make_identity('a=-(-(-a))')
        id22 = bunny.identity.Identity.make_identity('a=a*(-a)')
        id24 = bunny.identity.Identity.make_identity('a=(-a)*a')
        id32 = bunny.identity.Identity.make_identity('a=-(a*a)')
        id45 = bunny.identity.Identity.make_identity('x=a*(-x)')
        id50 = bunny.identity.Identity.make_identity('x=(-a)*x')
        
        id55 = bunny.identity.Identity.make_identity('x=-(a*x)')
        
        imp = fca.Implication({id20, id22, id24, id32, id45, id50}, {id55})
        bunny_found = bunny.bunny.InfBunny.find(imp, wait_time=20, kern_size=4)[0]
        assert bunny_found != None
        assert bunny_found.check_id(id20, 10)
        assert bunny_found.check_id(id22, 10)
        assert bunny_found.check_id(id24, 10)
        assert bunny_found.check_id(id32, 10)
        assert bunny_found.check_id(id45, 10)
        assert bunny_found.check_id(id50, 10)
        assert not bunny_found.check_id(id55, 10)
        
    def test_find202(self):
        print '\ttest_find202\n'
        id20 = bunny.identity.Identity.make_identity('a=-(-(-a))')
        id24 = bunny.identity.Identity.make_identity('a=(-a)*a')
        id32 = bunny.identity.Identity.make_identity('a=-(a*a)')
        id33 = bunny.identity.Identity.make_identity('a=-(a*x)')
        id50 = bunny.identity.Identity.make_identity('x=(-a)*x')
        id51 = bunny.identity.Identity.make_identity('x=(-x)*a')
        
        id56 = bunny.identity.Identity.make_identity('x=-(x*a)')
        
        imp = fca.Implication({id20, id24, id32, id33, id50, id51}, {id56})        
        bunny_found = bunny.bunny.InfBunny.find(imp, wait_time=20, kern_size=4)[0]
        assert bunny_found != None
        
    def test_find203(self):
        print '\ttest_find203\n'
        id6 = bunny.identity.Identity.make_identity('a=-(-a)')
        id22 = bunny.identity.Identity.make_identity('a=a*(-a)')
        id26 = bunny.identity.Identity.make_identity('a=x*(-a)')
        id32 = bunny.identity.Identity.make_identity('a=-(a*a)')
        id34 = bunny.identity.Identity.make_identity('a=-(x*a)')
        id39 = bunny.identity.Identity.make_identity('-a=a*a')
        id47 = bunny.identity.Identity.make_identity('x=x*(-x)')
        id55 = bunny.identity.Identity.make_identity('x=-(a*x)')
        id65 = bunny.identity.Identity.make_identity('-x=x*x')
        
        id41 = bunny.identity.Identity.make_identity('-a=x*a')
        
        id_pos_ls = [id47, id55, id65, id6, id22, id26, id32, id34, id39]
        
        imp = fca.Implication(id_pos_ls, {id41})        
        bunny_found = bunny.bunny.InfBunny.find(imp, wait_time=40, kern_size=4)[0]
        # see G566 from Kestler's dissertation
        assert bunny_found != None
        
    def test_find204(self):
        print '\ttest_find204\n'
        # [a = x*(-a), x = x, x = x*(-x), x = a*(-x), x = x*a, a = a*(-a), a = a*a] => -a = x*y

        id1 = bunny.identity.Identity.make_identity('a=x*(-a)')
        id2 = bunny.identity.Identity.make_identity('x=x')
        id3 = bunny.identity.Identity.make_identity('x=x*(-x)')
        id4 = bunny.identity.Identity.make_identity('x=a*(-x)')
        id5 = bunny.identity.Identity.make_identity('x=x*a')
        id6 = bunny.identity.Identity.make_identity('a=a*(-a)')
        id7 = bunny.identity.Identity.make_identity('a=a*a')
        
        idn = bunny.identity.Identity.make_identity('-a=x*y')
        
        id_pos_ls = [id1, id2, id3, id4, id5, id6, id7]
        
        imp = fca.Implication(id_pos_ls, {idn})  
        bunny_found = bunny.bunny.InfBunny.find(imp, wait_time=40, kern_size=4)[0]
        assert bunny_found != None
        
###############################################################################
    @nottest    
    def test_find6(self):
        print '\ttest_find6\n'
        # [a = x*(-a), x = x, x = x*(-x), x = a*(-x), x = x*a, a = a*(-a), a = a*a] => -a = x*y

        id1 = bunny.identity.Identity.make_identity('a=x*(-a)')
        id2 = bunny.identity.Identity.make_identity('x=x')
        id3 = bunny.identity.Identity.make_identity('x=x*(-x)')
        id4 = bunny.identity.Identity.make_identity('x=a*(-x)')
        id5 = bunny.identity.Identity.make_identity('x=x*a')
        id6 = bunny.identity.Identity.make_identity('a=a*(-a)')
        id7 = bunny.identity.Identity.make_identity('a=a*a')
        idn = bunny.identity.Identity.make_identity('-a=x*y')
        bunny_found = bunny.bunny.InfBunny.find([id1, id2, id3, id5, id6, id7], idn, limit=8, t_limit=65)
        assert bunny_found != None
        
    @nottest
    def test_find8(self):
        print '\ttest_find8\n'
        id22 = bunny.identity.Identity.make_identity('a=a*(-a)')
        id59 = bunny.identity.Identity.make_identity('x=-(y*x)')
        bunny_found = bunny.bunny.InfBunny.find([id59, ], id22, limit=8, t_limit=10)
        f2 = {'condition1': (lambda m, n: True, 
                             lambda m, n: n + 1,
                             'True',
                             'n + 1')}
        f1 = {'condition1': (lambda n: n >= 1, 
                             lambda n: n - 1,
                             'n >= 1',
                             'n - 1'),
              0: 1}
        bun = bunny.bunny.InfBunny(f2, f1)
        check59 = bun.check_id(id59, 8)
        check22 = bun.check_id(id22, 8)
        print check59, check22
        assert bunny_found != None