'''
Created on Apr 28, 2013

@author: artem
'''
import sympy

import identity

class Bunny(object):
    '''
    General Bunny class, superclass for fin_bunny and inf_bunny
    '''
    
    def __init__(self, f2_dict, f1_dict, f0_dict, index, size=None):
        '''
        Constructor
        '''
        self.f2_dict = f2_dict
        self.f1_dict = f1_dict
        self.f0_dict = f0_dict
        self.f2 = _generate_f2(f2_dict)
        self.f1 = _generate_f1(f1_dict)
        self.f0 = f0_dict
        self.index = index
        if size == None:
            self.size = len(self.f1_dict)
        else:
            self.size = size
        
    def __repr__(self):
        if self.size.__class__.__name__ != 'int':
            raise 'Size not int'
        size = self.size
        s = '\tBUNNY No {}'.format(self.index) + '\n'
        s += ('f2\t' + '\t'.join(map(str, range(size))) +
             '\t\tf1' + '\t\t\tf0' + '\n')
        for i in range(size):
            f2_vals = (self.f2_dict[i, j] for j in range(size))
            s += (str(i) + '\t' + '\t'.join(map(str, f2_vals)) +
                  '\t\t' + str(i) + '\t' + str(self.f1_dict[i]))
            if i == 0:
                s += '\t\t\t' + str(self.f0_dict)
            s += '\n'
        return s
    
    def __eq__(self, other):
        return ((self.f2_dict == other.f2_dict) and
                (self.f1_dict == other.f1_dict) and
                (self.f0_dict == other.f0_dict))
        
    def check_id(self, id_, limit=None):
        '''
        check if bunny satisfies id
        
        @param limit: checks up to this limit
        '''
        if limit == None:
            limit = self.size
        return id_(self, limit)
       
        
class InfBunny(Bunny):
    '''
    Class for infinite bunnies
    '''
    
    def __init__(self, f2_dict, f1_dict):
        '''
        Constructor
        '''
        super(InfBunny, self).__init__(f2_dict, f1_dict, 0, 'N/A', 'Inf')
        
    def __str__(self):
        raise 'NotImplementedYet'
        
    @classmethod
    def find(cls, id_pos_ls, id_neg, limit):
        '''
        find infinite bunny which satisfies all id_pos_ls and does not satisfy
        id_neg
        '''
        for bunny in inf_bunnies(id_pos_ls, id_neg):
            if (all([bunny.check_id(id_, limit) for id_ in id_pos_ls]) and
                ((id_neg == None) or not bunny.check_id(id_neg, limit))):
                    return bunny
                
################BUNNIES GENERATION#########################
def constraints(id_ls):
    '''
    Find the constraints coming from list of identities id_ls. Symbolic calculus
    is used.
    '''
    def replace(sym_str, pattern):
        replaced = sym_str.replace(pattern[0], pattern[1])
        if sym_str == replaced:
            return replaced
        else:
            return replace(replaced, pattern)
    def make_sym(func_str):
        sym_str = sympy.sympify(func_str).subs({a: a, b: b, c: c, d: d, e: e,
                                                f2: f2, f1: f1, f0: 0})
        return sym_str
    
    a, b, c, d, e = sympy.symbols('a, b, c, d, e')
    f0 = sympy.symbols('f0')
    f1 = sympy.Function('f1')
    f2 = sympy.Function('f2')
    pattern2 = (f2, lambda m, n: a*m + b*n + c)
    pattern1 = (f1, lambda n: d*n + e)
    
    eq_ls = []
    for id_ in id_ls:
        if ((str(id_).find('x') == -1) and
            (str(id_).find('y') == -1) and
            (str(id_).find('z') == -1)):
                continue
        left_repl = replace(replace(make_sym(id_.left_term.func_str),
                                    pattern1), pattern2)
        right_repl = replace(replace(make_sym(id_.right_term.func_str),
                                     pattern1), pattern2)
        eq_ls.append(left_repl - right_repl)
    return sympy.solve(eq_ls, a, b, c, d, e, dict=True), eq_ls

def _generate_f2(dict_values):
    '''
    Make binary function: N_0*N_0 -> N_0, from dict_values. 
    '''
    conds = [(cond_case[0], cond_case[1])
             for (name, cond_case) in dict_values.items()
             if (name.__class__.__name__ == 'str') and name.startswith('condition')]
    def f2(m, n):
        try:
            return dict_values[(m, n)]
        except KeyError:
            for (cond, case) in conds:
                if cond(m, n):
                    return case(m, n)
    return f2
        
def _generate_f1(dict_values):
    '''
    Make unary function: N_0 -> N_0, from dict_values. 
    '''
    conds = [(cond_case[0], cond_case[1])
             for (name, cond_case) in dict_values.items()
             if (name.__class__.__name__ == 'str') and name.startswith('condition')]
    def f1(n):
        try:
            return dict_values[n]
        except KeyError:
            for (cond, case) in conds:
                if cond(n):
                    return case(n)
    return f1

def inf_bunnies(id_pos_ls, id_neg):
    '''
    Create infinite bunnies that satisfy all id_pos_ls. See the pattern in all_f.
    Some bunnies that satisfy may be not found!
    '''
    a, b, c, d, e, m, n = sympy.symbols('a, b, c, d, e, m, n')
    constrs = constraints(id_pos_ls)[0][0]
    
    f0 = 0
    all_f = (({(0,0): b00, (0,1): b01,
               (1,0): b10, (1,1): b11,
               'condition1': (lambda m, n: (n in [0,1]) and (m >= 2),
                              lambda m, n: a1*m + b1*n + c1,
                              '{0}*m + {1}*n + {2}'.format(a1, b1, c1)),
               'condition2': (lambda m, n: (m in [0,1]) and (n >= 2), 
                              lambda m, n: a2*m + b2*n + c2,
                              '{0}*m + {1}*n + {2}'.format(a2, b2, c2)),
               'condition3': (lambda m, n: (m >= 2) and (n >= 2),
                              lambda m, n: a3*m + b3*n + c3,
                              '{0}*m + {1}*n + {2}'.format(a3, b3, c3))},
              
              {0: u0, 1: u1,
               'condition1': (lambda n: n>0,
                              lambda n: d1*n + e1,
                              '{0}*n + {1}'.format(d1, e1))})
             
             for d1 in [0, 1, 2]
             for e1 in [0, 1, -1, 2, -2]
             if (d1*2 + e1 >= 0)           
             
             for a3 in [0, 1]
             for b3 in [0, 1]
             for c3 in [0, 1, -1, 2, -2, 3, -3]
             if (a3*2 + b3*2 + c3 >= 0)
             if all([constrs[i].subs({a: a3, b: b3, c: c3, d: d1, e: e1}) ==
                     i.subs({a: a3, b: b3, c: c3, d: d1, e: e1})
                     for i in constrs.keys()])
             
             for a1 in [0, 1]
             for b1 in [0, 1]
             for c1 in [0, 1, -1, 2, -2, 3]
             if (a1*2 + c1 >= 0)
             if all([constrs[i].subs({a: a1, b: b1, c: c1, d: d1, e: e1}) ==
                     i.subs({a: a1, b: b1, c: c1, d: d1, e: e1})
                     for i in constrs.keys()])
             
             for a2 in [0, 1]
             for b2 in [0, 1]
             for c2 in [0, 1, -1, 2, -2, 3]
             if (b2*2 + c2 >= 0)
             if all([constrs[i].subs({a: a2, b: b2, c: c2, d: d1, e: e1}) ==
                     i.subs({a: a2, b: b2, c: c2, d: d1, e: e1})
                     for i in constrs.keys()])
             
             for b00 in range(2)
             for b10 in range(3)
             for b01 in range(3)
             for b11 in range(3)
             
             for u0 in range(2)
             for u1 in range(2))
    
    for f2_dict, f1_dict in all_f:
        yield InfBunny(f2_dict, f1_dict)
        
def bunnies(size):
    '''
    Create all bunnies on the domain of given size.
    '''
    all_f = ((dict([[(i, j), (v2 / (size ** (size*i + j)) % size)]
                     for i in range(size)
                     for j in range(size)]),
              
              dict([[i, (v1 / size**i % size)]
                     for i in range(size)]),
              
              v0,
              
              v2 + v1*(size ** (size**2)) + v0*(size ** (size**2 + size)))
             
             for v2 in xrange(size ** (size**2))
             for v1 in xrange(size ** size)
             for v0 in xrange(1))
    
    for f2_dict, f1_dict, f0_dict, index in all_f:
        yield Bunny(f2_dict, f1_dict, f0_dict, index)
        
def show(index, size):
    '''
    Show bunny with given index.
    '''
    v2 = index % (size ** (size**2))
    v1 = ((index - v2) / (size ** (size**2))) % (size ** size)
    v0 = ((index - v2 - v1) / (size ** (size**2 + size))) % (size ** (size**2))
    f2_dict = dict([[(i, j), (v2 / (size ** (size*i + j)) % size)]
                     for i in range(size)
                     for j in range(size)])
    f1_dict = dict([[i, (v1 / size**i % size)]
                     for i in range(size)])
    f0 = v0
    return Bunny(f2_dict, f1_dict, f0, index)
    
        
########################################################
def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    import itertools
    return next(itertools.islice(iterable, n, None), default)

if __name__ == '__main__':
    import time
    
    now = time.time()
    for _ in bunnies(2):
        pass
    print time.time() - now
    
    id1 = identity.Identity.make_identity('x', 'a*[-x]') #45
    id2 = identity.Identity.make_identity('x', '-[a*x]') #55
    #found = InfBunny.find([id1,], id2, limit=6)
    #assert found != None
    
    id1 = identity.Identity.make_identity('a', '-a')
    id2 = identity.Identity.make_identity('a', '-[x*a]')
    id3 = identity.Identity.make_identity('x', '-[x*x]')
    id4 = identity.Identity.make_identity('x', '-[a*x]')
    id5 = identity.Identity.make_identity('x', '[-x]')
    id6 = identity.Identity.make_identity('x', 'y')
    #found = InfBunny.find([id1, id2, id3, id4, id5], id6, limit=3)
    #assert found != None
    
    id1 = identity.Identity.make_identity('a', '[-a]') #3
    id2 = identity.Identity.make_identity('a', '-[x*a]') #34
    id3 = identity.Identity.make_identity('x', '-[x*x]') #57
    idn = identity.Identity.make_identity('a', '[x*a]') #10
    #found = InfBunny.find([id1, id2, id3], idn, limit=4)
    #assert found != None