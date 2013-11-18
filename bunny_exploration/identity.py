'''
Created on Apr 27, 2013

@author: artem
'''
import copy
import itertools
from string import maketrans

import term_parser
import p9m4
import fca

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
    
    
def generate_ts(len_limit, num_vars=1):
    '''
    Generates terms of size len_limit. Size := length(ops_list) + 
                                               length(vars_list).
                                               
    @param len_limit: length limit of term.
    @return: list of Terms.
    '''
    def orders_types_product(orders_ls, types_ls):
        '''
        If type is 0 corresponding order is changed to 0.
        '''
        result = []
        for types in types_ls:
            nul_inds = [i for i, x in enumerate(types) if x == 0]
            for orders in orders_ls:
                cor_orders = orders[:]
                for i in nul_inds:
                    cor_orders[i] = 0
                result.append((cor_orders, types))
        return result
    
    num_types = 3
    ops_ls = []
    els_ords_types = []
    for len_ops in xrange(len_limit + 1):
        types_ls = [list(i) for i in
                     itertools.product(*itertools.repeat(range(num_types),
                                                        len_ops))]
        orders_ls = [list(i) for i in
                      itertools.permutations(range(1, len_ops+1), len_ops)]
        new_ops = orders_types_product(orders_ls, types_ls)
        ops_ls += new_ops  
    for ops in ops_ls:
        len_ops = len(ops[1]) - len(filter(lambda x: x == 0, ops[1]))
        elems_ls = [list(i) for i in 
                    itertools.product(*itertools.repeat(range(num_vars),
                                                        len_limit - len_ops))]
        els_ords_types += [(els, ops[0], ops[1])
                           for els in elems_ls
                           if (len(els) ==
                               1 + len(filter(lambda x: x == 2, ops[1])))]
    
    result = []
    for (elems, order, types) in els_ords_types:
        term = Term.parsed2term(('', len(elems), len(order),
                                 elems, order, types))
        term.name = term.func_str
        if not (term in result):
            result.append(term)
    
    return result
    
def generate_ids(len_limit, num_vars=2):
    '''
    Generates non-equivalent identities of size len_limit. The non-equality is
    checked via theorem prover Prover9. Identities are said to be equivalent if
    the imply each other. Examples: x=y <=> x=z, x*a=a <=> y*a=a. 
    Size := length(left_term) + length(right_term).
                                                    
                                               
    @param len_limit: length limit of identity.
    @return: list of identites.
    '''
    def not_equivalent(ids, left_term, right_term):
        '''
        True if among ids there is no equivalent identity to new_id, otherwise
        False.
        '''
        for var in 'xyzw':
            if ((left_term.func_str.strip('').startswith(var) and 
                 not var in right_term.func_str) or
                (right_term.func_str.strip('').startswith(var) and 
                 not var in left_term.func_str)):
                    return False
            elif ((left_term.func_str.strip('').startswith('f1({})'.format(var)) and
                   right_term.func_str.strip('').startswith('f1(') and
                   not var in right_term.func_str.strip('') and
                   not 'f2' in right_term.func_str.strip('')) or
                  (right_term.func_str.strip('').startswith('f1({})'.format(var)) and
                   left_term.func_str.strip('').startswith('f1(') and
                   not var in left_term.func_str.strip('') and
                   not 'f2' in left_term.func_str.strip(''))):
                return False
        str_ids = map(str, ids)
        str_new_id1 = left_term.func_str + ' = ' + right_term.func_str
        str_new_id2 = right_term.func_str + ' = ' + left_term.func_str
        vars_perms = map(''.join, itertools.permutations('xyzw', 4))
        for to in vars_perms:
            trans_table = maketrans('xyzw', to)
            equiv_id1 = str_new_id1.translate(trans_table)
            equiv_id2 = str_new_id2.translate(trans_table)
            if (equiv_id1 in str_ids or
                equiv_id2 in str_ids):
                return False
        return True
        
    result = []
    terms_ls = [generate_ts(length, num_vars) for length in range(1, len_limit)]
    for len_left_term in xrange(len_limit / 2):
        len_right_term = len_limit - len_left_term - 2
        if len_left_term == len_right_term:
            for i in xrange(len(terms_ls[len_left_term])):
                for j in xrange(i + 1, len(terms_ls[len_right_term])):
                    left_term = terms_ls[len_right_term][i]
                    right_term = terms_ls[len_right_term][j]
                    if not_equivalent(result, left_term, right_term):
                        new_id = Identity(left_term, right_term)
                        result.append(new_id)
        else:
            for left_term in terms_ls[len_left_term]:
                for right_term in terms_ls[len_right_term]:
                    if not_equivalent(result, left_term, right_term):
                        new_id = Identity(left_term, right_term)
                        result.append(Identity(left_term, right_term))
    return result

########################################################
if __name__ == '__main__':
    def print_ids(length, num_vars):
        g = generate_ids(length, num_vars)
        print '\n'.join(map(str, g))
        print '\ntotal: ', len(g)
        return g
    #for i in g:
    #    print i.func_str
    #print '\ntotal: ', len(g)