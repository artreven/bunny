'''
Holds a class for representing (2,1,0) algebras (BUNnies) and functions for
finding bunnies satisfying given conditions.

Created on Apr 28, 2013

@author: Artem
'''
import re
import time
import itertools
import sympy
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
        s = '\tBUNNY No {0}, size = {1}'.format(self.index, self.size) + '\n'
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
    
    def __repr__(self):
        s = 'show(index={}, size={})'.format(self.index, self.size)
        return s
    
    def __eq__(self, other):
        return ((type(self) == type(other)) and
                (self.size == other.size) and
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
        evaluations = itertools.product(xrange(limit),
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
    all_f = ((dict([[(i, j), (v2 / (size ** (i + size*j)) % size)]
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
    f2_dict = dict([[(i, j), (v2 / (size ** (i + size*j)) % size)]
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
            v2 += f2_dict[(i, j)] * size**(i + size*j)
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

vary_syms = ['n', 'm'] # symbols that may vary. For piecewise functions.
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
    
    def __repr__(self):
        s = 'InfBunny({}, {}, {})'.format(*map(repr, [self.funcs['f2'],
                                                      self.funcs['f1'], 
                                                      self.funcs['f0']]))
        return s
    
    def __eq__(self, other):
        raise Exception, 'Equality not yet defined for infinite bunnies.'
    
    @classmethod
    def read(cls, bunny_str):
        '''
        Read infinite bunny from string.
        '''
        def get_graph(func_name, start_index):
            f_graph = []
            else_val = None
            for f_line in bunny_str_ls[start_index+1:]:
                is_else_val = False
                start_input = f_line.find(func_name + '(')
                end_input = f_line.find(')')
                if start_input == -1:
                    break
                input_str = f_line[start_input+3:end_input].split(',')
                input = []
                for i in input_str:
                    i = i.strip()
                    if i.isdigit():
                        input.append( Value(int(i)) )
                    elif 'n' in i or 'm' in i:
                        input.append( Value(i) )
                    elif i == 'else':
                        is_else_val = True
                    elif i == '':
                        continue
                    else:
                        assert 0
                start_output = f_line.find(':=')
                output_str = f_line[start_output+2:].strip()
                if output_str.isdigit():
                    output = Value(int(output_str))
                elif 'n' in output_str:
                    output = Value(output_str)
                if is_else_val:
                    else_val = output
                else:
                    f_graph.append( tuple(input + [output]) )
            return f_graph, else_val
            
        bunny_str_ls = bunny_str.split('\n')
        for i in xrange(len(bunny_str_ls)):
            if bunny_str_ls[i] == 'f2:':
                f2_i = i
            elif bunny_str_ls[i] == 'f1:':
                f1_i = i
            elif bunny_str_ls[i] == 'f0:':
                f0_i = i
        f2_graph, else_val = get_graph('f2', f2_i)
        f2 = PiecewiseFunc('f2', f2_graph)
        if else_val != None:
            f2.else_val = else_val
        f1_graph, else_val = get_graph('f1', f1_i)
        f1 = PiecewiseFunc('f1', f1_graph)
        if else_val != None:
            f1.else_val = else_val
        f0 = Value( int(bunny_str_ls[f0_i+1].strip()) )
        bun = InfBunny(f2, f1, f0)
        return bun
    
    @classmethod
    def find(cls, imp, wait_time, kern_size):
        '''
        Find infinite bunny which is counter-example to implication *imp*
        '''
        print 'Starting on implication: {}'.format(imp)
        try: 
            bun = _inf_bunnies(imp, wait_time, kern_size)
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
    
    def __init__(self, f_name, graph, size=None, else_val=None):
        '''
        Constructor.
        *graph* - list representing graph of the function - (*input, output).
        '''
        self.graph = graph
        self.name = f_name
        self.else_val = else_val
        self.size = size
        
    def __call__(self, *args):
        var_args = []
        for arg in args:
            if not isinstance(arg, Variable):
                arg = Value(arg)
            var_args.append(arg)
        args = tuple(var_args)
        # if in kern or no size
        for t in self.graph:
            if args == t[:-1]:
                return t[-1]
        # if not in kern or no size
        for t in sorted(self.graph, key=lambda x: len({v for v in ['n', 'm']
                                                       if v in ''.join(map(str, x)) })):
            if self.size and all(arg.isint() for arg in args) and all(arg.value < self.size for arg in args):
                break
            t_str = reduce(lambda x,y: x+y, map(str, t), '')
            if not any(c in t_str for c in vary_syms):
                continue
            if any(t[i] != args[i] for i in range(len(args)) if t[i].value == None):
                continue
            if any(v.isunset() for v in t): # this is experimental in order to avoid identifying n and m while imposing bindings
                continue
            
            eq_system = []
            gotonextt = False
            for i in range(len(args)):
                lhs = t[i].value
                rhs = args[i].value
                if lhs == None or rhs == None:
                    if t[i] != args[i]:
                        gotonextt = True
                        break
                    else:
                        continue
                if (isinstance(lhs, int) and rhs != lhs):
                    gotonextt = True
                    break
                elif lhs == rhs:
                    continue
                if isinstance(rhs, str):
                    rhs = rhs.replace('n', 'n1').replace('m', 'm1')
                equ = sympy.Eq( sympy.sympify(lhs), sympy.sympify(rhs) )
                eq_system.append(equ)
            if gotonextt: continue
            solution = sympy.solve(eq_system, ['n', 'm'])
            if not eq_system or (solution and
                                 not any(x in map(str, solution.keys())
                                         for x in ['n1', 'm1'])):
                if isinstance(t[-1], Variable) and t[-1].value == None:
                    return t[-1]
                else:
                    ans = sympy.sympify(str(t[-1])).subs(solution)
                    ans = str(ans).replace('n1', 'n').replace('m1', 'm')
                    try: ans = int(ans)
                    except: pass
                    return Value(ans)
        if self.else_val != None:
            return self.else_val
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
        entries = set(['\t' + self.name + str(t[:-1]) + ':= ' + str(t[-1]) + '\n'
                       for t in self.graph])
        out_str += ''.join(sorted(entries))
        if self.else_val != None:
            out_str += '\t' + self.name + '(else):= ' + str(self.else_val) + '\n'
        return out_str
    
    def __repr__(self):
        s = '('
        for t in self.graph:
            s += '('
            for v in t:
                if v.isunset():
                    s += 'Variable(), '
                elif v.isint():
                    s += 'Value({}), '.format(v.value)
                elif v.isvary():
                    s += 'Value("{}"), '.format(v.value)
            s += '), ' 
        s += ')'
        out_str = 'PiecewiseFunc(f_name="{}", graph={}, size={}, else_val={})'.format(self.name, s, self.size, self.else_val)
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
                (isinstance(new_value, str) and
                 any(c in new_value for c in vary_syms))):
            raise Exception, ("New value {} has to be".format(new_value) +
                              " either None or int or str with 'n' or 'm'")
        if isinstance(new_value, str) and ' ' in new_value:
            new_value = new_value.replace(' ', '')
        if isinstance(new_value, str) and not new_value[-1].isdigit():
            new_value += '+0'
        self._values_dict[self.id] = new_value
        
    def identify(self, other):
        if isinstance(other, Value):
            self.value = other.value
        elif isinstance(other, Variable):
            for var in filter(lambda v: v.id == self.id, Variable._registry):
                var.id = other.id
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
        
    __hash__ = None
        
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
        if isinstance(other, Variable):
            ans = sympy.sympify(self.value) + sympy.sympify(other.value)
        else:
            ans = sympy.sympify(self.value) + other
        ans = str(ans)
        try:
            ans = int(ans)
        except:
            pass
        return Value(ans)
     
    def __sub__(self, other):
        if isinstance(other, Variable):
            return self.__add__(-sympy.sympify(other.value))
        else:
            return self.__add__(-other)
        
    def isvary(self):
        return isinstance(self.value, str) and any(c in self.value
                                                   for c in ['n', 'm'])
    
    def isint(self):
        return isinstance(self.value, int)

    def isunset(self):
        return self.value == None
        
    @classmethod
    def clsreset(cls):
        cls._registry = []
        cls._ids = itertools.count(0)
        cls._values_dict = dict()
        
def identify_variables(var1, var2):
    if isinstance(var2, Variable) and var2.value == None:
        var2.identify(var1)
    elif isinstance(var1, Variable) and var1.value == None:
        var1.identify(var2)
    else:
        raise InconsistentBindingError, 'At least one variable from {} and {} has to be unset.'.format(var1, var2)
        
class Value(Variable):
    def __init__(self, arg):
        if not (isinstance(arg, int) or 
                (isinstance(arg, str) and
                 any(c in arg for c in vary_syms))):
            print type(arg), arg.isalnum(), arg
            raise Exception, ("New value {} has to be".format(arg) +
                              " either int or str with 'n' or 'm'")
        if isinstance(arg, str) and ' ' in arg:
            arg = arg.replace(' ', '')
        if isinstance(arg, str) and not arg[-1].isdigit():
            arg += '+0'
        self._value = arg
        
    def identify(self, other):
        raise Exception, 'No way to identify value with {}'.format(other)
    
    def __hash__(self):
        return self.value.__hash__()
        
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
    bun = construct(imp, wait_time, kern_size)
    try:
        assert not imp.conclusion or any(not bun.check_id(id_, kern_size+4) for id_ in imp.conclusion)
        assert all(bun.check_id(id_, kern_size+4) for id_ in imp.premise)
    except AssertionError:
        print [(str(id_), bun.check_id(id_, kern_size+4, v=True)) for id_ in imp.conclusion]
        print [(str(id_), bun.check_id(id_, kern_size+4, v=True)) for id_ in imp.premise]
        print bun
        raise Exception
    return bun
            
#######################################################################
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r)
                                         for r in range(len(s)+1))

def check_consistency(bun, ulimit=7):
    '''
    Check consistency of function in bunny: for every input there should be not
    more than one result.
    '''
    def check_f(f):
        f_graph = []
        for x in f.graph:
            if not x in f_graph:
                f_graph.append(x)
        def checkf1(f_graph):
            # Check for simple duplicates
            inputs = [x[:-1] for x in f_graph]
            duplicates = set([tuple(map(str, input)) for input in inputs if inputs.count(input) > 1])
            if duplicates:
                for x in duplicates:
                    results = [str(z[-1]) for z in f_graph
                               if tuple(map(str, z[:-1])) == x
                               if z[-1].value != None] 
                    if len(set(results + [None])) > 2:
                        return False
            return True
        def checkf2(f_graph):
            # check that the output varies only if the input varies
            for row in f_graph:
                if 'n' in str(row[-1]):
                    row_str = ''.join( map(str, row[:-1]) )
                    if not ('n' in row_str or 'Variable' in row_str):
                        return False
            return True
        def checkf3(f_graph):
            # check that if the input varies and several outputs possible, all the outputs are equal    
            var_syms = ['n', 'm']
            n_rows = [row for row in f_graph
                      if not any(v.isunset() for v in row)
                      if any(x in ''.join(map(str, row[:-1])) for x in var_syms)]
            for n_row in n_rows:
                f_row = PiecewiseFunc('', [n_row])
                #f_row.size = f.size
                
                local_vars = set([c for c in ''.join(map(str, n_row)) if c in var_syms])
                evaluations = itertools.product( *[range(f.size, f.size+5)]*len(local_vars) ) # important to start from f.size because f_row.size set to None
                str_n_row = map(str, n_row[:-1])
                for evaluation in evaluations:
                    subs = zip(local_vars, evaluation)
                    input = tuple(map(lambda x: eval(x, globals(), dict(subs)),
                                      str_n_row))
                    if any(x < 0 for x in input): continue
                    try: orig = f(*input)
                    except: continue
                    new = f_row(*input)
                    if (orig != new and 
                        (type(orig) != Variable or orig.value != None) and 
                        (type(new) != Variable or new.value != None)):
                            return False
            return True
        def checkf4(f_graph):
            # check that there are bindings beyond kern_size, they comply with varying case        
            for t in f_graph:
                if any(x > f.size for x in t[:-1]):
                    try:
                        f_out = f(*t[:-1])
                    except ArgError:
                        pass
                    else:
                        if t[-1] != f_out and (type(f_out) != Variable or
                                               f_out.value != None):
                            return False
            return True
        return checkf1(f_graph) and checkf2(f_graph) and checkf3(f_graph) and checkf4(f_graph)
    
    return check_f(bun.funcs['f1']) and check_f(bun.funcs['f2'])
                
def violates_ids(bun, ids):
    bun_copy = deepcopy(bun)
    kern_size = bun.funcs['f2'].size + 1
    it_dict = OrderedDict()
    if not ids:
        if bun.funcs['f2'].else_val == None:
            bun.funcs['f2'].else_val = 0
        if bun.funcs['f1'].else_val == None:
            bun.funcs['f1'].else_val = 0
        return True
    for idn in ids:
        while True:
            try:
                sat = bun.check_id(idn, kern_size+4)
            except ArgError as e:
                if not e.f_name in it_dict:
                    it_dict[e.f_name] = iter(xrange(kern_size+2))
                bun.funcs[e.f_name].else_val = next(it_dict[e.f_name])
            else:
                if sat == False:
                    if bun.funcs['f2'].else_val == None:
                        bun.funcs['f2'].else_val = 0
                    if bun.funcs['f1'].else_val == None:
                        bun.funcs['f1'].else_val = 0
                    return True
                else:
                    while it_dict:
                        f_name, else_it = it_dict.popitem()
                        try:
                            bun.funcs[f_name].else_val = next(else_it)
                            it_dict[f_name] = else_it
                            break
                        except StopIteration:
                            bun.funcs[f_name].else_val = None
                    else:
                        break
    bun = deepcopy(bun_copy)
    return False

def impose_bindings(bun, id_, domain_dict, var_deps):
    """
    Reveal constraints that arise from identities, put them into into bunny.
    We check and find constraints for points defined by *domain_dict*.
    *var_deps* represents the dependencies on the variables - keys are
    identification numbers of variables.
    """
    evaluations = itertools.product( *[domain_dict[v] for v in id_.var_symbols] )
    for evaluation in evaluations:    
        point_dict = dict( zip(id_.var_symbols, evaluation) )
        while True:
            try:
                lhs = id_.left_term(bun, point_dict)
                rhs = id_.right_term(bun, point_dict)
                if not rhs == lhs:
                    identify_variables(lhs, rhs)
                    ### Not sure if consistency check is needed here
                    consistent = check_consistency(bun)
                    if not consistent:
                        print 'raised from consistency check while imposing bindings'
                        raise InconsistentBindingError
                    ###
                break
            except ArgError as e:
                new_v = Variable()
                var_deps[new_v.id] = e.vals
                bun.funcs[e.f_name].add_value(e.vals, new_v)
            
def construct(imp, wait_time, kern_size=3):
    """
    Construct and return bunny that satisfies all identities from id_ls.
    
    @param kern_size: size of kernel of algebra, which is essentially the
    counter-example. 
    """
    def fetch_next(bun, undef_vars, def_vars, get_domain, ids_neg):
        vars_number = len(undef_vars) + len(def_vars)
        if vars_number == 0:
            if check_consistency(bun,
                                 ulimit=bun.funcs['f1'].size+4):
                return
            else:
                raise StopIteration
        while True:
            # Check time constraint
            if time.time()-ts >= wait_time:
                raise TimeoutError
            try:
                var = undef_vars.pop()
            except IndexError:
                var = def_vars.pop()
            consistent = None
            try:
                domain_it = domain_its[var.id]
            except KeyError:
                domain_it = get_domain(var)
                domain_its[var.id] = domain_it
            while consistent != True:
                try:
                    var.value = next(domain_it)
                    consistent = check_consistency(bun)
                except StopIteration:
                    var.value = None
                    del domain_its[var.id]
                    undef_vars.append(var)
                    try:
                        var = def_vars.pop()
                        domain_it = domain_its[var.id]
                    except IndexError:
                        raise StopIteration
            else:
                try:
                    neg_sat = all(bun.check_id(id_, limit=8) for id_ in ids_neg)
                except ArgError:
                    neg_sat = False
                if neg_sat:
                    undef_vars.append(var)
                else:
                    def_vars.append(var)
                assert len(undef_vars) + len(def_vars) == vars_number
                if not undef_vars:
                    break
    
    def get_domain(var):
        assert isinstance(var, Variable)
        dep_vars = var_deps[var.id]
        ans = range(kern_size + 2)
        var_syms = {c for c in ['n', 'm'] if c in ''.join(map(str, dep_vars))}
        if 'n' in var_syms:
            ans += ['n{:+}'.format(i) for i in range(-2, 3)]
            if 'm' in var_syms:
                ans += ['m+n{:+}'.format(i) for i in range(-2, 3)]
        if 'm' in var_syms:
            ans += ['m{:+}'.format(i) for i in range(-2, 3)]
        return iter(ans)
    
    Variable.clsreset()
    bun = InfBunny(PiecewiseFunc('f2', [], size=kern_size),
                   PiecewiseFunc('f1', [], size=kern_size),
                   Value(0))
    var_deps = dict()
    domain_dict = {'x': range(kern_size) + ["n+0"],
                   'y': range(kern_size) + ["m+0"],
                   'z': range(kern_size) + ["h+0"]}
    for id_ in imp.premise:
        impose_bindings(bun, id_, domain_dict, var_deps)
    def_vars = []; undef_vars = []
    for var in Variable._registry:
        if var.value == None and not var in undef_vars:
            undef_vars.insert(0, var)
        
    domain_its = OrderedDict()
    ts = time.time()
    while True:
        # Check time constraint
        if time.time()-ts >= wait_time:
            raise TimeoutError
        fetch_next(bun, undef_vars, def_vars, get_domain, imp.conclusion)
        if violates_ids(bun, imp.conclusion):
            return bun


######################IF MAIN ROUTINE##################################
if __name__ == '__main__':
    import identity
    import fca
    import cProfile
    
    import p9m4
    
    imp_str = 'x = f1(f2(x,y)) => x = f1(f2(x,f0)), x = f1(f2(x,x)), f0 = f1(f2(f0,f0)), f0 = f2(f1(f0),f0), f0 = f1(f2(f0,x))'
    premise, conclusion = imp_str.split('=>')
    premise_ids = map(lambda x: x.strip(), premise.split(', '))
    conclusion_ids = map(lambda x: x.strip(), conclusion.split(', '))
    ids_pos = map(lambda x: identity.Identity.func_str2id(x), premise_ids)
    ids_neg = map(lambda x: identity.Identity.func_str2id(x), conclusion_ids)
    imp = fca.Implication(ids_pos, ids_neg)
    
    ibun = InfBunny.find(imp, wait_time=15000, kern_size=1)[0]
    
    print [(str(id_), ibun.check_id(id_, 10, v=True)) for id_ in ids_neg]
    print [(str(id_), ibun.check_id(id_, 10, v=True)) for id_ in ids_pos]
#     assert not all(ibun.check_id(id_, 10) for id_ in ids_neg)
#     assert all(ibun.check_id(id_, 10) for id_ in ids_pos)