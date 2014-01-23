'''
Created on Apr 28, 2013

@author: artem
'''
#import time
import itertools
import signal
from contextlib import contextmanager

import identity

####################################EXCEPTIONS#################################
class ArgError(Exception):
    """
    Thrown when function is not defined for input values
    """
    def __init__(self, vals, f_name):
        self.vals = vals
        self.f_name = f_name
        self.message = 'For input {} function {} is not defined'.format(vals,
                                                                        f_name)
    def __str__(self):
        return self.message
    
class TimeoutException(Exception): pass
    
#######################DECORATORS############################################
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(*args)
    _f.__name__ = f.__name__
    return _f

###############################################################################
class Bunny(object):
    '''
    General Bunny class, superclass for InfBunny
    '''
    
    def __init__(self, f2_dict, f1_dict, f0_dict, index=None, size=None):
        '''
        Constructor
        '''
        self.f2_dict = f2_dict
        self.f1_dict = f1_dict
        self.f0_dict = f0_dict
        self.f2 = generate_f(f2_dict, 'f2')
        self.f1 = generate_f(f1_dict, 'f1')
        self.f0 = f0_dict
        if size == None:
            self.size = len(self.f1_dict)
        else:
            self.size = size
        if index == None:
            if isinstance(self.size, int):
                self.index = _index(f2_dict, f1_dict, f0_dict, size)
            else:
                self.index = 'N/A'
        else:
            self.index = index
        
    def __repr__(self):
        if self.size.__class__.__name__ != 'int':
            raise Exception('Size not int')
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
        
    def has_attribute(self, id_):
        return self.check_id(id_)
        
    def check_id(self, id_, limit=None, partial=False):
        '''
        check if bunny satisfies id
        
        @param limit: checks up to this limit
        @param partial: if partially defined f2 and f1 are accepted. In this
        case None is a valid result.
        @return: 1) *partial* == False => returns *result*
                 2) *partial* == True  => returns two values: (*result*, *values*);
                                          *values* - input for which functions
                                          should be defined next.
        '''
        if isinstance(self.size, int):
            limit = self.size
        assert limit != None
        
        #needed = []
        # substitutions. After every loop checks number of variables
        for w in xrange(limit):
            for z in xrange(limit):
                for y in xrange(limit):
                    for x in xrange(limit):
                        values = [x, y, z, w]
                        try:
                            left_val = id_.left_term(self, values)
                        except ArgError as e:
                            if not partial:
                                info = 'id: {}, '.format(id_)
                                info += 'values = {}, '.format(values)
                                info += 'left.func_str = {}, '.format(id_.left_term.func_str)
                                info += 'Bunny: {}'.format(self.__repr__())
                                raise Exception, info
                            needed = (e.vals, e.f_name)
                            return (None, needed)
                        else:
                            try:
                                right_val = id_.right_term(self, values)
                            except ArgError as e:
                                if not partial:
                                    info = 'id: {}, '.format(id_)
                                    info += 'values = {}, '.format(values)
                                    info += 'right.func_str = {}\n'.format(id_.right_term.func_str)
                                    info += 'Bunny: {}'.format(self.__repr__())
                                    raise Exception, info
                                needed = (e.vals, e.f_name)
                                return (None, needed)
                            else:
                                # Nothing to do if left_val == right_val
                                if left_val != right_val:
                                    return False if (not partial) else (False, values)
                    if id_.var_count == 1:
                        break
                if id_.var_count <= 2:
                    break
            if id_.var_count <= 3:
                break
        return True if not partial else (True, [])

        
class InfBunny(Bunny):
    '''
    Class for infinite bunnies
    '''
    
    def __init__(self, f2_dict, f1_dict):
        '''
        Constructor
        '''
        super(InfBunny, self).__init__(f2_dict, f1_dict, 0, 'N/A', 'Inf')
    
    def __repr__(self):
        s = '\n\tINFINITE BUNNY\n'
        if hasattr(self.f2_dict, '__call__') or hasattr(self.f1_dict, '__call__'):
            return s
        s += 'f2(m, n):\n'
        # f2
        for k in sorted(self.f2_dict.keys()):
            s += '\t'
            try:
                s += str(self.f2_dict[k][2]) + ':\t' + str(self.f2_dict[k][3]) + '\n'
            except TypeError:
                s += str(k) + ':\t' + str(self.f2_dict[k]) + '\n'
        # f1
        s += 'f1(n):\n'
        for k in sorted(self.f1_dict.keys()):
            s += '\t'
            try:
                s += str(self.f1_dict[k][2]) + ':\t' + str(self.f1_dict[k][3]) + '\n'
            except TypeError:
                s += str(k) + ':\t' + str(self.f1_dict[k]) + '\n'
            except IndexError:
                s += str(k) + '\n'
        # f0
        s += 'f0:\n\t' + str(0) + '\n'
        return s
    
    def has_attribute(self, id_):
        return self.check_id(id_, 10)      

    @classmethod
    def find(cls, id_pos_ls, id_neg, limit, t_limit, previous=None):
        '''
        find infinite bunny which satisfies all id_pos_ls and does not satisfy
        id_neg
        '''
        print 'Starting on positive identities: ', id_pos_ls,
        print ',\tnegative identity: ', id_neg
        if (previous and
            (all([previous.check_id(id_, limit) for id_ in id_pos_ls]) and
            ((id_neg == None) or not previous.check_id(id_neg, limit)))):
                print 'Infinite bunny found - previous', previous, '\n'
                return previous
        try:
            with time_limit(t_limit):
                for bunny in inf_bunnies(id_pos_ls, id_neg):
                    if (all([bunny.check_id(id_, limit) for id_ in id_pos_ls]) and
                        ((id_neg == None) or not bunny.check_id(id_neg, limit))):
                            print 'Infinite bunny found', bunny, '\n'
                            return bunny
        except TimeoutException, msg:
            print 'Time limit = {} sec reached, no infinite bunny found\n'.format(t_limit)
            return None
        print 'No infinite bunny found'
        return None
    
def generate_f(dict_values, f_name):
    '''
    Make function from dict_values. 
    '''
    @memo
    def f(*args):
        try:
            return dict_values[args[0]] if (len(args) == 1) else dict_values[args]
        except KeyError:
            conds = [(cond_case[0], cond_case[1])
                     for (name, cond_case) in sorted(dict_values.items())
                     if (isinstance(name, str) and name.startswith('condition'))]
            for (cond, case) in conds:
                if cond(*args):
                    return case(*args)
            else:
                raise ArgError(args, f.__name__)
    f.__name__ = f_name
    return dict_values if hasattr(dict_values, '__call__') else f

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Timed out!"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

###############################GENERATION OF FINITE BUNNIES##############
def bunnies(size):
    '''
    Create all finite bunnies on the domain of given size.
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

def _index(f2_dict, f1_dict, f0_dict, size):
    """
    Find index given f2, f1, f0, and size
    """
    #calc v2
    v2 = 0
    for i in range(size):
        for j in range(size):
            v2 += f2_dict[(i, j)] * size**(j + size*i)
    #calc v1
    v1 = 0
    for i in range(size):
        v1 += f1_dict[i] * size**i
    #v0 is just f0_dict=f0
    v0 = f0_dict
            
    return (v2 + v1*(size ** (size**2)) + v0*(size ** (size**2 + size)))
                
#############################GENERATION OF INFINITE BUNNIES 2###############
def finish(f2_dict, f1_dict):
    """
    Finalize partially defined f2 and f1 to total functions.  
    """
    def add_val(fs, field, dom):
        return (dict(f_d.items() + {field: i}.items())
                for f_d in fs
                for i in dom)
        
    normal_vals2 = [(0, 0), (0, 1), (1, 0), (1, 1),
                    (2, 2),
                    (0, 2), (2, 0),
                    (1, 2), (2, 1),
                    (0, 3), (3, 0),
                    (1, 3), (3, 1),
                    (1, 4), (0, 4), 
                    (4, 1), (4, 0),
                    (4, 4), (4, 9),
                    (3, 4), (4, 3),
                    (3, 5), (5, 3)]
    normal_vals1 = [0, 1, 2, 3, 4]
    f2s = [f2_dict,]
    f1s = [f1_dict,]
    for val in normal_vals2:
        (field, dom) = domain(val)
        if not (field in f2_dict.keys()):
            f2s = add_val(f2s, field, dom)
    for val in normal_vals1:
        (field, dom) = domain(val)
        if not (field in f1_dict.keys()):
            f1s = add_val(f1s, field, dom)
    return itertools.product(f2s, f1s)

def domain(field):
    """
    @return: next field and possible values for this field
    """
    dom = None
    if hasattr(field, '__len__') and len(field) == 1:
        field = field[0]
    # Case for unary function
    if isinstance(field, int):
        if field >= 3:
            field = 'condition1'
            dom = ((lambda n: n >= 3,
                    lambda n: d1*n + e1,
                    'n >= 3',
                    '{0}*n + {1}'.format(d1, e1))
                   for d1 in [0, 1, 2]
                   for e1 in [0, 1, -1, 2, -2, 3, -3]
                   if (d1*3 + e1 >= 0))
        elif field < 3:
            dom = iter(range(5))
    # Case for binary function
    elif len(field) == 2:
        if ((field[0] in [0, 1] and field[1] in [2, 3]) or
            (field[0] in [2, 3] and field[1] in [0, 1])):
            dom = iter(range(6))
        elif (field[0] == 2 and field[1] == 2):
            dom = iter(range(6))
        elif (field[0] == 0) and (field[1] >= 3):
            field = 'condition1'
            dom = ((lambda m, n: (m  == 0) and (n >= 3), 
                    lambda m, n: b1*n + c1,
                    '(m == 0) and (n >= 3)',
                    '{0}*n + {1}'.format(b1, c1))
                   for b1 in [0, 1]
                   for c1 in [0, 1, -1, 2, -2, 3]
                   if (b1*2 + c1 >= 0))
        elif (field[0] == 1) and (field[1] >= 4):
            field = 'condition2'
            dom = ((lambda m, n: (m  == 1) and (n >= 4), 
                    lambda m, n: b1*n + c1,
                    '(m == 1) and (n >= 4)',
                    '{0}*n + {1}'.format(b1, c1))
                   for b1 in [0, 1]
                   for c1 in [0, 1, -1, 2, -2, 3, 4, 5]#, -3]
                   if (b1*4 + c1 >= 0))
        elif (field[1] == 0) and (field[0] >= 3):
            field = 'condition3'
            dom = ((lambda m, n: (n == 0) and (m >= 3), 
                    lambda m, n: a2*m + c2,
                    '(n == 0) and (m >= 3)',
                    '{0}*m + {1}'.format(a2, c2))      
                   for a2 in [0, 1]
                   for c2 in [0, 1, -1, 2, -2, 3]
                   if (a2*2 + c2 >= 0))
        elif (field[1] == 1) and (field[0] >= 4):
            field = 'condition4'
            dom = ((lambda m, n: (n == 1) and (m >= 4), 
                    lambda m, n: a2*m + c2,
                    '(n == 1) and (m >= 4)',
                    '{0}*m + {1}'.format(a2, c2))      
                   for a2 in [0, 1]
                   for c2 in [0, 1, -1, 2, -2, 3, 4, 5]#, -3]
                   if (a2*2 + c2 >= 0))
        elif (field[1] >= 3) and (field[0] == field[1]):
            field = 'condition5'
            dom = ((lambda m, n: (n >= 3) and (m == n), 
                    lambda m, n: a3*m + b3*n + c3,
                    '(n >= 3) and (m == n)',
                    '{0}*m + {1}*n + {2}'.format(a3, b3, c3))     
                   for a3 in [0, 1]
                   for b3 in [0, 1]
                   for c3 in [0, 1, -1, 2, -2, 3]
                   if (a3*3 + b3*3 + c3 >= 0))
        elif (field[1] >= 2) and (field[0] == (field[1]+1)):
            field = 'condition6'
            dom = ((lambda m, n: (n >= 2) and (m == (n+1)), 
                    lambda m, n: a3*m + b3*n + c3,
                    '(n >= 2) and (m == (n+1))',
                    '{0}*m + {1}*n + {2}'.format(a3, b3, c3))     
                   for a3 in [0, 1]
                   for b3 in [0, 1]
                   for c3 in [0, 1, -1, 2, -2, 3]
                   if (a3*3 + b3*2 + c3 >= 0))
        elif (field[0] >= 2) and (field[0] == (field[1]-1)):
            field = 'condition7'
            dom = ((lambda m, n: (m >= 2) and (m == (n-1)), 
                    lambda m, n: a3*m + b3*n + c3,
                    '(m >= 2) and (m == (n-1))',
                    '{0}*m + {1}*n + {2}'.format(a3, b3, c3))     
                   for a3 in [0, 1]
                   for b3 in [0, 1]
                   for c3 in [0, 1, -1, 2, -2, 3]
                   if (a3*2 + b3*3 + c3 >= 0))
        elif (field[1] >= 2) and (field[0] == (field[1]+2)):
            field = 'condition8'
            dom = ((lambda m, n: (n >= 2) and (m == (n+2)), 
                    lambda m, n: a3*m + b3*n + c3,
                    '(n >= 2) and (m == (n+2))',
                    '{0}*m + {1}*n + {2}'.format(a3, b3, c3))     
                   for a3 in [0, 1]
                   for b3 in [0, 1]
                   for c3 in [0, 1, -1, 2, -2, 3]
                   if (a3*4 + b3*2 + c3 >= 0))
        elif (field[0] >= 2) and (field[0] == (field[1]-2)):
            field = 'condition9'
            dom = ((lambda m, n: (m >= 2) and (m == (n-2)), 
                    lambda m, n: a3*m + b3*n + c3,
                    '(m >= 2) and (m == (n-2))',
                    '{0}*m + {1}*n + {2}'.format(a3, b3, c3))     
                   for a3 in [0, 1]
                   for b3 in [0, 1]
                   for c3 in [0, 1, -1, 2, -2, 3]
                   if (a3*2 + b3*4 + c3 >= 0))
        elif ((field[1] >= 2) and (field[0] >= 2) and
              (field[0] != field[1]) and (field[0] != field[1]-1) and
              (field[0] != field[1]+1) and (field[0] != field[1]-2) and
              (field[0] != field[1]+2)):
            field = 'condition10'
            dom = ((lambda m, n: ((n >= 2) and (m >= 2) and
                                  (m != n) and (m != n-1) and
                                  (m != n+1) and (m != n+2) and
                                  (m != n-2)), 
                    lambda m, n: a3*m + b3*n + c3,
                    '((n >= 2) and (m >= 2) and \
(m != n) and (m != n-1) and (m != n+1) and (m != n+2) and (m != n-2))',
                    '{0}*m + {1}*n + {2}'.format(a3, b3, c3))     
                   for a3 in [0, 1]
                   for b3 in [0, 1]
                   for c3 in [0, 1, -1, 2, -2, 3, -3]
                   if (a3*2 + b3*2 + c3 >= 0))
        elif (field[1] < 2) and (field[0] < 2):
            dom = iter(range(4))
    if not dom:
        raise ValueError('field = {}, dom is not defined.'.format(field))
    return (field, dom)

def construct(id_ls, id_neg):
    """
    Construct and return bunny that satisfies all identities from id_ls.
    """        
    fields = []
    assigns = []
    def f_updates(f2_dict, f1_dict):
        """
        iterator over all possibly valid updates of f2 and f1
        """
        if not fields:
            raise StopIteration
        (next_field, f_name) = fields[-1]
        if next_field == None:
            yield (f2_dict, f1_dict)
        assign = assigns[-1]
        for b in assign:
            if f_name == 'f1':
                f1_new = dict(f1_dict.items() + {next_field: b}.items())
                yield (f2_dict, f1_new)
            elif f_name == 'f2':
                f2_new = dict(f2_dict.items() + {next_field: b}.items())
                yield (f2_new, f1_dict)
            
    def backtrack(f2_dict, f1_dict):
        try:
            return next(f_updates(f2_dict, f1_dict))
        except StopIteration:
            if not fields:
                raise StopIteration
            (field, f_name) = fields.pop()
            assign = assigns.pop()
            if f_name == 'f1':
                del(f1_dict[field])
            elif f_name == 'f2':
                del(f2_dict[field])
            return backtrack(f2_dict, f1_dict)
        
    def complete(f2_dict, f1_dict):
        """
        iterator over all f2 and f1 satisfying id_ls and not satisfying id_neg
        """
        while(True):
            if id_neg != None:
                sat, needed = InfBunny(f2_dict, f1_dict).check_id(id_neg, limit, True)
                if sat == True:
                    f2_dict, f1_dict = backtrack(f2_dict, f1_dict)
                    continue
            for id_ in id_ls:
                sat, needed = InfBunny(f2_dict, f1_dict).check_id(id_, limit, True)
                if sat == None:
                    vals, f_name = needed 
                    (next_field, assign) = domain(vals)
                    fields.append((next_field, f_name))
                    assigns.append(assign)
                    break
                elif sat == False:
                    break
            else:
                if id_neg != None:
                    sat, needed = InfBunny(f2_dict, f1_dict).check_id(id_neg, limit, True)
                    if sat == None:
                        vals, f_name = needed 
                        (next_field, assign) = domain(vals)
                        fields.append((next_field, f_name))
                        assigns.append(assign)
                    elif sat == False:
                        yield f2_dict, f1_dict
                else:
                    yield f2_dict, f1_dict
            f2_dict, f1_dict = backtrack(f2_dict, f1_dict)
                    
    f2_dict = {}
    f1_dict = {}
    limit = 9
    return complete(f2_dict, f1_dict)

def inf_bunnies(id_pos_ls, id_neg):
    '''
    Create infinite bunnies that satisfy all id_pos_ls and do not satisfy id_neg.
    
    Alternative version, uses bindings obtained from id_pos_ls and kind of
    backtracking.
    '''    
    for f2_dict, f1_dict in construct(id_pos_ls, id_neg):
        for f2_d, f1_d in finish(f2_dict, f1_dict):
            yield InfBunny(f2_d, f1_d)
        
######################IF MAIN ROUTINE##################################
if __name__ == '__main__':
    id1 = identity.Identity.make_identity('x = a*(-x)')
    id2 = identity.Identity.make_identity('x = -(a*x)')
    print InfBunny.find([id1,], id2, limit=10, t_limit=10)