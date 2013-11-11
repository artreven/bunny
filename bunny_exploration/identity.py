'''
Created on Apr 27, 2013

@author: artem
'''
import copy
import itertools

import term_parser

# Two errors to throw when the result of substitution into term is less 0 or not int
class NoneValueError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
    
class NegativeError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
    
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

##############################################################################
class Identity(object):
    '''
    Class defines identities consisting of two terms: left and right. Used to
    represent algebraic identity.
    '''

    def __init__(self, left_term, right_term):
        '''
        Constructor
        '''
        self.left_term = left_term
        self.right_term = right_term
        self.var_count = max([left_term.var_count, right_term.var_count])
        
    def __repr__(self):
        return str(self.left_term.name) + ' = ' + str(self.right_term.name)
    
    @classmethod
    def make_identity(cls, left_str, right_str):
        '''
        make identity from two strings
        '''
        left_term = Term.str2term(left_str)
        right_term = Term.str2term(right_str)
        
        return cls(left_term, right_term)
    
    
class Term(object):
    '''
    Represents mathematical term
    '''
    
    def __init__(self, func_str, name, var_count):
        '''
        Constructor
        '''
        self.func_str = func_str
        self.compiled_str = compile(func_str, '', 'eval') #term rewritten as applications of functions
        self.name = name
        self.var_count = var_count
        
    @memo
    def __call__(self, bunny, values):
        '''
        evaluate the term given bunny and values of variables.
        
        @return: value from bunny's domain or None if not defined
        '''
        (x, y, z, w) = values
        (f2, f1, f0) = (bunny.f2, bunny.f1, bunny.f0)
        result = eval(self.compiled_str)
        if isinstance(result, int) and (result < 0):
            info = 'result = {}, '.format(result)
            info += 'values = {}, '.format(values)
            info += 'func_str = {}'.format(self.func_str)
            raise NegativeError(info)
        return result
         
    def __repr__(self):
        return self.name
    
    def __eq__(self, other):
        return self.func_str == other.func_str
        
    @classmethod
    def str2term(cls, str_):
        '''
        make term from str
        '''
        parsed = term_parser.parse_str(str_)
        return cls.parsed2term(parsed)
    
    @classmethod
    def parsed2term(cls, parsed):
        '''
        make term from parsed output from bunny_exploration.term_parser
        '''
        def apply_op(var_list, op_order, op_types):
            '''
            find and execute next operation
            '''
            if len(op_order) == 0:
                assert len(var_list) == 1
                return var_list[0]
            
            ind = op_order.index(min(op_order))
            apply_ind = ind - len([1 for typ in op_types[:ind]
                                   if typ < 2])
            if op_types[ind] == 2:
                var_list[apply_ind] = ('f2(' + var_list[apply_ind] + ',' +
                                       var_list[apply_ind + 1] +')')
                del var_list[apply_ind + 1]
            elif op_types[ind] == 1:
                var_list[apply_ind] = ('f1(' + var_list[apply_ind] + ')')
            elif op_types[ind] == 0:
                var_list[apply_ind] = 'f0'
            else:
                assert False
            del op_order[ind]
            del op_types[ind]
            
            return apply_op(var_list, op_order, op_types)
            
        (name, _, _, elems, op_order, op_types) = copy.deepcopy(parsed)
        assert len(elems) == 1 + len(filter(lambda x: x == 2, op_types))
        var_count = max(elems) + 1
        # change numbers in elements into variable names
        var_dict = {0: 'x', 1: 'y', 2: 'z', 3: 'w'}
        var_list = [var_dict[elem] for elem in elems]
        
        func_str = apply_op(var_list, op_order, op_types)
        return cls(func_str, name, var_count)
    
    
def generate_ts(len_limit_elems, len_limit_ops, num_vars=1):
    '''
    Generates terms of size up to 2*len_limit. Size := length(ops_list) + 
                                                       length(vars_list),
    where nulary operation is counted twice: in vars_list and in ops_list. This
    is due to input to programs written in C.
    
    @attention: every nulary is counted twice: in vars_list and in ops_list.
    @param len_limit: length limit of 1) the number and 2) the num of ops.
    @return: list of Terms
    '''
    name = 'Missing'
    num_types = 3
    elems_ls = []
    for len_vars in range(1, len_limit_elems + 1):
        elems = itertools.product(*itertools.repeat(range(num_vars),
                                                    len_vars))
        elems_ls += [list(i) for i in elems]
    ops_ls = []
    for len_ops in range(len_limit_ops + 1):
        orders = itertools.permutations(range(len_ops), len_ops)
        orders_ls = [list(i) for i in orders]
        types = itertools.product(*itertools.repeat(range(num_types),
                                                    len_ops))
        types_ls = [list(i) for i in types]
        ops_ls += list(itertools.product(orders_ls, types_ls))
    els_ords_types = [(els, ops[0], ops[1])
                      for els in elems_ls
                      for ops in ops_ls
                      if (len(els) == 1 + len(filter(lambda x: x == 2, ops[1])))]
    result = []
    for (elems, order, types) in els_ords_types:
        term = Term.parsed2term((name, len(elems), len(order),
                                 elems, order, types))
        if not (term in result):
            result.append(term)
    
    return result
    
def generate_ids(len_limit, variables=1):
    # TODO:    
    return None

########################################################
if __name__ == '__main__':
    g = generate_ts(2, 2)
    for i in g:
        print i
    print len(g)