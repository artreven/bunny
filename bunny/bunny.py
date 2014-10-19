'''
Holds a class for representing (2,1,0) algebras (BUNnies) and functions for
finding bunnies satisfying given conditions.

Created on Apr 28, 2013

@author: Artem
'''
import re
import time
import itertools
from collections import OrderedDict
from copy import deepcopy

####################################EXCEPTIONS#################################
class ArgError(Exception):
    """
    Thrown when function is not defined for input values
    """
    def __init__(self, vals, f_name):
        self.vals = vals
        self.f_name = f_name
        self.message = 'For input {0} function {1} is not defined'.format(vals,
                                                                        f_name)
    def __str__(self):
        return self.message
    
class TimeoutError(Exception): pass

class UndefError(Exception): pass

class InconsistentBindingError(Exception): pass
    
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

#Constant definition
#Because of 0*float('inf') := 'nan', I define infinity to be 1000.
INF = 1000

###############################################################################
class Bunny(object):
    '''
    General Bunny class, superclass for InfBunny
    '''
    
    def __init__(self, f2, f1, f0=0, index=None, size=None):
        '''
        Constructor
        '''
        self.funcs = dict()
        self.funcs['f2'] = f2
        self.funcs['f1'] = f1
        self.funcs['f0'] = f0
        if size == None:
            self.size = len(self.funcs['f1'].dict)
        else:
            self.size = size
        if index == None:
            if isinstance(self.size, int):
                self.index = _index(self.funcs['f2'].dict,
                                    self.funcs['f1'].dict,
                                    self.funcs['f0'],
                                    self.size)
            else:
                self.index = 'N/A'
        else:
            self.index = index
        
    def __str__(self):
        if not isinstance(self.size, int):
            raise Exception('Size not int')
        size = self.size
        s = '\tBUNNY No {0}'.format(self.index) + '\n'
        s += ('f2\t' + '\t'.join(map(str, range(size))) +
             '\t\tf1' + '\t\t\tf0' + '\n')
        for i in range(size):
            f2_vals = (self.funcs['f2'].dict[i, j] for j in range(size))
            s += (str(i) + '\t' + '\t'.join(map(str, f2_vals)) +
                  '\t\t' + str(i) + '\t' + str(self.funcs['f1'].dict[i]))
            if i == 0:
                s += '\t\t\t' + str(self.funcs['f0'])
            s += '\n'
        return s
    
    def __eq__(self, other):
        return ((self.size == other.size) and
                (self.funcs['f2'].dict == other.funcs['f2'].dict) and
                (self.funcs['f1'].dict == other.funcs['f1'].dict) and
                (self.funcs['f0'] == other.funcs['f0']))
    
    @classmethod
    def dicts2bunny(cls, f2_dict, f1_dict, f0, index=None, size=None):
        f2 = _dict2f(f2_dict, 'f2')
        f1 = _dict2f(f1_dict, 'f1')
        return cls(f2, f1, f0, index, size)

    def check_id(self, id_, limit=None, v=False):
        '''
        check if bunny satisfies id
        
        @param limit: checks up to this limit
        '''
        if isinstance(self.size, int):
            limit = self.size
        assert limit != None and limit != float('inf')
        
        current_vars = id_.var_symbols
        evaluations = itertools.product(xrange(limit-1, -1, -1),
                                        repeat=len(current_vars))
        for evaluation in evaluations:
            dict_subs = dict(zip(current_vars, evaluation))
            lhs = id_.left_term(self, dict_subs)
            rhs = id_.right_term(self, dict_subs) 
            if not lhs == rhs:
                if v:
                    return False, dict_subs, lhs, rhs
                else:
                    return False
        return True
        
def bunnies(size):
    '''
    Create iterator over all finite bunnies on the domain of given size.
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
    
    for f2_dict, f1_dict, f0, index in all_f:
        f2 = _dict2f(f2_dict, 'f2')
        f1 = _dict2f(f1_dict, 'f1')
        yield Bunny(f2, f1, f0, index)
        
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
    f2 = _dict2f(f2_dict, 'f2')
    f1_dict = dict([[i, (v1 / size**i % size)]
                     for i in range(size)])
    f1 = _dict2f(f1_dict, 'f1')
    f0 = v0
    return Bunny(f2, f1, f0, index)

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
        
def _dict2f(dict_f, f_name):
    @memo
    def f(*args):
        if len(args) == 1: args = args[0]
        try:
            return dict_f[args]
        except KeyError:
            raise ArgError(args, f_name)
        
    f.__name__ = f_name
    f.dict = dict_f
    return f

################################INFINITE BUNNIES        
class InfBunny(Bunny):
    '''
    Class for infinite bunnies
    '''
    
    def __init__(self, f2, f1, f0):
        '''
        Constructor
        '''
        super(InfBunny, self).__init__(f2, f1, f0, 'N/A', 'Inf')
        
    def __deepcopy__(self, memo):
        newone = type(self)(None, None, None)
        newone.__dict__.update(self.__dict__)
        for f_name in ['f0', 'f1', 'f2']:
            self.funcs[f_name] = deepcopy(self.funcs[f_name], memo)
        return newone
    
    def __str__(self):
        s = '\n\tINFINITE BUNNY\n'
        s += (str(self.funcs['f2']) + str(self.funcs['f1']) +
              'f0:\n\t{}\n'.format(self.funcs['f0']))
        return s
    
    def __eq__(self, other):
        raise Exception, 'Equality not yet defined for infinite bunnies.'
    
    @classmethod
    def find(cls, imp, wait_time, kern_size):
        '''
        Find infinite bunny which is counter-example to implication *imp*
        '''
        print 'Starting on implication: {}'.format(imp)
        try: 
            bun = next(_inf_bunnies(imp, wait_time, kern_size))
            print 'Infinite bunny found', bun, '\n'
            return (bun, 'Success')
        except StopIteration:
            reason = 'No infinite bunny found - possibilities exhausted'
            print reason
            return (None, reason)
        except InconsistentBindingError:
            reason = 'No infinite bunny found - inconsistency found'
            print reason
            return (None, reason)
        except TimeoutError:
            reason = 'No infinite bunny found - timeout'
            print reason
            return (None, reason)
        
class PiecewiseFunc(object):
    '''
    Class for piecewise-defined functions
    '''
    
    def __init__(self, f_name, graph, size=None):
        '''
        Constructor.
        *graph* - list representing graph of the function - (*input, output).
        '''
        self.graph = graph
        self.name = f_name
        self.else_val = None
        self.size = size
        
    def __call__(self, *args):
        var_args = []
        for arg in args:
            if not isinstance(arg, Variable):
                arg = Value(arg)
            var_args.append(arg)
        args = tuple(var_args)
        if self.size == None or not any(args[i] > self.size for i in xrange(len(args))):
            for t in self.graph:
                if args == t[:-1]:
                    return t[-1]
        for t in sorted(self.graph, key=str):
            if not 'n' in reduce(lambda x,y: x+y, map(str, t), ''):
                continue
            n = None
            for i in xrange(len(args)):
                if (isinstance(t[i].value, str) and args[i].value != None):
                    new_n = args[i] - int(t[i].value[-2:])
                    if self.size != None and new_n.value < self.size:
                        break
                    if not isinstance(n, Variable):
                        n = new_n
                    elif new_n != n:
                        break
                else:
                    if t[i] != args[i]:
                        break
            else:
                if isinstance(t[-1], Variable) and t[-1].value == None:
                    return t[-1]
                else:
                    return eval(str(t[-1]))
        if self.else_val != None:
            return f.else_value
        raise ArgError(args, self.name)
    
    def add_value(self, input, output):
        assert not any(x[:-1] == input for x in self.graph)
        self.graph.append(input + (output,))
        
    def __deepcopy__(self, memo):
        newone = type(self)(None, None)
        newone.__dict__.update(self.__dict__)
        self.graph = deepcopy(self.graph, memo)
        return newone

    def __str__(self):
        out_str = self.name + ':\n'
        for t in set(self.graph):
            out_str += '\t' + self.name + str(t[:-1]) + ':= ' + str(t[-1]) + '\n'
        if self.else_val != None:
            out_str += '\t' + self.name + '(else):= ' + str(self.else_val) + '\n'
        return out_str
    
    def __eq__(self, other):
        raise Exception, 'Equality not yet defined for piecewise functions.'    

class Variable(object):
    '''
    Class for representing a variable which value can be assigned later
    '''
    _ids = itertools.count(0)
    _values_dict = dict()
    _registry = []
    
    def __init__(self, id_ = None):
        if id_ == None:
            self.id = self._ids.next()
            self._registry.append(self)
            self.value = None
        else:
            self.id = id_
        
    @property
    def value(self):
        return self._values_dict[self.id]
    
    @value.setter
    def value(self, new_value):
        '''
        *new_value* has to be either None or int or str
        '''
        if not (new_value == None or 
                isinstance(new_value, int) or 
                isinstance(new_value, str)):
            raise Exception, "New value {} has to be either None or int or str".format(new_value)
        if new_value == 'n':
            new_value = 'n+0'
        self._values_dict[self.id] = new_value
        
    def identify(self, other):
        if isinstance(other, Value):
            self.value = other.value
        elif isinstance(other, Variable):
            self.id = other.id
        elif isinstance(other, int) or isinstance(other, str):
            self.value = other
        else:
            raise Exception, 'Do not know how to identify to {}'.format(type(other))
        
    def __eq__(self, other):
        return str(self) == str(other)
        
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __gt__(self, other):
        if isinstance(other, int):
            if isinstance(self.value, int):
                return self.value > other
            elif isinstance(self.value, str):
                return True
        else:
            raise Exception, 'Not implemented yet'
        
    def __hash__(self):
        return self.__repr__().__hash__()
        
    def __deepcopy__(self, memo):
        newone = type(self)(self.value)
        return newone
    
    def __repr__(self):
        val = self.value
        if val == None:
            return 'Variable(id_={})'.format(self.id)
        else:
            return str(val)
        
    def __add__(self, other):
        if isinstance(other, int):
            if isinstance(self.value, int):
                new_value = self.value + other
            elif isinstance(self.value, str):
                new_value = 'n{:+}'.format(int(self.value[-2:]) + other)
            return Value(new_value)
        elif isinstance(other, Variable) and isinstance(other.value, int):
            return self + other.value
    
    def __sub__(self, other):
        if isinstance(other, Variable):
            if isinstance(other.value, str):
                if not isinstance(self.value, str):
                    raise Exception, 'Trying to subtract {} from {}'.format(other, self)
                return Value( int(self.value[-2:]) - int(other.value[-2:]) )
            elif isinstance(other.value, int):
                return self - other.value
        else:
            return self.__add__(-other)
        
    @classmethod
    def clsreset(cls):
        cls._registry = []
        cls._ids = itertools.count(0)
        cls._values_dict = dict()
        
class Value(Variable):
    def __init__(self, arg):
        if not (isinstance(arg, int) or 
                isinstance(arg, str)):
            raise Exception, "New value {} has to be either int or str".format(arg)
        if arg == 'n':
            arg = 'n+0'
        self._value = arg
        
    def identify(self, other):
        raise Exception, 'No way to identify value with {}'.format(other)
        
    @property
    def value(self):
        return self._value
    
#############################GENERATION OF INFINITE BUNNIES 2###############
def _inf_bunnies(imp, wait_time, kern_size):
    '''
    Create infinite bunnies that satisfy all id_pos_ls and do not satisfy id_neg.
    
    Alternative version, uses bindings obtained from id_pos_ls and kind of
    backtracking.
    '''
    for bun in construct(imp, wait_time, kern_size):
        yield bun
            
#########################################################################
def identify_values(value1, value2):
    if isinstance(value1, Variable) and value1.value == None:
        value1.identify(value2)
    elif isinstance(value2, Variable) and value2.value == None:
        value2.identify(value1)
    else:
        raise InconsistentBindingError, 'At least one variable from {} and {} has to be unset.'.format(value1, value2)
        
def check_consistency(bun, llimit=3, ulimit=7):
    '''
    Check consistency of function in bunny: for every input there should be only
    one result. After evaluating a variable there can appear inconsistencies.
    '''
    def check_f(f):
        inputs = [x[:-1] for x in f.graph]
        duplicates = set([input for input in inputs if inputs.count(input) > 1])
        if duplicates:
            for x in duplicates:
                results = [str(z[-1]) for z in f.graph if z[:-1] == x if z[-1].value != None] 
                if len(set(results + [None])) > 2:
                    return False
                
        for row in f.graph:
            if 'n' in str(row[-1]):
                row_str = ''.join( map(str, row[:-1]) )
                if not ('n' in row_str or 'Variable' in row_str):
                    return False
        n_rows = set([row for row in f.graph if 'n' in ''.join(map(str, row[:-1]))])
        old_size = f.size
        for n_row in n_rows:
            # Find exactly n_row, not just equal row
            n_row_vars_profile = []
            for j in xrange(len(n_row)):
                row_var = n_row[j]
                if type(row_var) == Variable:
                    n_row_vars_profile.append(row_var.id)
                else:
                    n_row_vars_profile.append(None)
            for i in xrange(len(f.graph)):
                if f.graph[i] == n_row:
                    graph_vars_profile = []
                    for j in xrange(len(n_row)):
                        graph_var = f.graph[i][j]
                        if type(graph_var) == Variable:
                            graph_vars_profile.append(graph_var.id)
                        else:
                            graph_vars_profile.append(None)
                    if n_row_vars_profile == graph_vars_profile:
                        n_row_i = i
                        break
            del f.graph[n_row_i]
            f.graph.append(n_row)
            # Delete row, check results are the same.
            for n in range(llimit, ulimit):
                input = tuple(map(eval, [str(x) for x in n_row[:-1]]))
                orig = f(*input)
                try:
                    f.graph.pop()
                    f.size = None
                    new = f(*input)
                except ArgError:
                    pass
                else:
                    if orig != new:
                        return False
                finally:
                    f.size = old_size
                    f.graph.append(n_row)
        return True
        
    return check_f(bun.funcs['f1']) and check_f(bun.funcs['f2'])

def fetch_next(bun, undef_vars, def_vars, vars_its, get_new_var_it):
    vars_number = len(undef_vars) + len(def_vars)
    while True:
        try:
            var = undef_vars.pop()
        except IndexError:
            var = def_vars.pop()
        else:
            vars_its[var.id] = get_new_var_it(var)
        var_it = vars_its[var.id]
        consistent = None
        while consistent != True:
            try:
                var.value = next(var_it)
                consistent = check_consistency(bun,
                                               bun.funcs['f1'].size,
                                               bun.funcs['f1'].size+3)
            except StopIteration:
                var.value = None
                undef_vars.append(var)
                try:
                    var = def_vars.pop()
                    var_it = vars_its[var.id]
                except IndexError:
                    raise StopIteration
        else:
            def_vars.append(var)
            assert len(undef_vars) + len(def_vars) == vars_number
            if not undef_vars:
                break

def impose_bindings(bun, id_, domain):
    evaluations = itertools.product(domain, repeat=len(id_.var_symbols))
    for evaluation in evaluations:
        point_dict = dict( zip(id_.var_symbols, evaluation) )
        while True:
            try:
                lhs = id_.left_term(bun, point_dict)
                rhs = id_.right_term(bun, point_dict)
                if not rhs == lhs:
                    identify_values(lhs, rhs)
                    ### Not sure if consistency check is needed here
                    consistent = check_consistency(bun)
                    if not consistent:
                        print 'raised from consistency check while imposing bindings'
                        raise InconsistentBindingError
                    ###
                break
            except ArgError as e:
                new_v = Variable()
                bun.funcs[e.f_name].add_value(e.vals, new_v)
             
def construct(imp, wait_time, kern_size=3):
    """
    Construct and return bunny that satisfies all identities from id_ls.
    
    @param limit: size of kern of algebra, which is essentially the counter-example. 
    """
    def get_range(var):
        if isinstance(var, Variable):
            return iter(range(kern_size+1) + ['n+0', 'n-1', 'n+1', 'n-2', 'n+2'])
        print 'no range for {} ;('.format(var)
        raise Exception
    
    Variable.clsreset()
    ids_to_sat = list(imp.premise)
    bun = InfBunny(PiecewiseFunc('f2', [], size=kern_size-1),
                   PiecewiseFunc('f1', [], size=kern_size-1),
                   Value(0))
    for id_ in ids_to_sat:
        impose_bindings(bun, id_, range(kern_size) + ["'n+0'"])
    # Initialize parameters
    vars_its = dict(); def_vars = []; undef_vars = []
    for var in Variable._registry:
        if var.value == None and not var in undef_vars:
            undef_vars.append(var)
    id_c = list(imp.conclusion)[0]
    ts = time.time()
    while True:
        # Check time constraint
        if time.time()-ts >= wait_time:
            raise TimeoutError
        fetch_next(bun, undef_vars, def_vars, vars_its, get_range)
        undef_vars_conc = []; vars_its_conc = dict(); def_vars_conc = []
        while True:
            bun.funcs['f1'].size = None
            bun.funcs['f2'].size = None
            try:
                sat = bun.check_id(id_c, kern_size+4)
            except ArgError as e:
                # Tested only for one absent value, may not work as expected for more values
                new_v = Variable()
                bun.funcs[e.f_name].add_value(e.vals, new_v)
                undef_vars_conc.append(new_v)
            else:
                if sat == False:
                    bun.funcs['f2'].else_val = 0
                    bun.funcs['f1'].else_val = 0
                    yield bun
            bun.funcs['f2'].size = kern_size-1
            bun.funcs['f1'].size = kern_size-1
            if undef_vars_conc or def_vars_conc:
                try:
                    fetch_next(bun, undef_vars_conc, def_vars_conc,
                               vars_its_conc, get_range)
                except StopIteration:
                    break
            else:
                break




     
######################IF MAIN ROUTINE##################################
if __name__ == '__main__':
    pass