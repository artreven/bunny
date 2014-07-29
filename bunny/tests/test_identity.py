'''
Use with Nosetests (https://nose.readthedocs.org/en/latest/)

Created on Apr 28, 2013

@author: artem
'''
import bunny
from bunny.identity import *

def test_make_identity():
    left_str = 'x'
    right_str = '-(a*x)'
    iden = Identity.make_identity(left_str + '=' + right_str)
    left_term = Term.parsed2term(bunny.term_parser.parse_str(left_str))
    right_term = Term.parsed2term(bunny.term_parser.parse_str(right_str))
    print 'id: ', iden
    assert iden.left_term == left_term
    assert iden.right_term == right_term
    assert iden.left_term.name == left_str
    assert iden.right_term.name == right_str
    
def test_term():
    str1 = 'x'
    str2 = '-(x*a)'
    t1 = Term.parsed2term(bunny.term_parser.parse_str(str1))
    t2 = Term.parsed2term(bunny.term_parser.parse_str(str2))
    print 't1: ', t1
    print 't2: ', t2
    assert t1 == Term.str2term(str1)
    assert t2 == Term.str2term(str2)
    
def test_parsed2term():
    str1 = 'x'
    str2 = '-(x*a)'
    str3 = '(a*(-x))*(-y)'
    t1 = Term.parsed2term(bunny.term_parser.parse_str(str1))
    t2 = Term.parsed2term(bunny.term_parser.parse_str(str2))
    t3 = Term.parsed2term(bunny.term_parser.parse_str(str3))
    assert t1.func_str == 'x'
    assert t2.func_str == 'f1(f2(x,f0))'
    assert t3.func_str == 'f2(f2(f0,f1(x)),f1(y))'
    
def test_evaluate_term():
    f2_dict = {'condition1': (lambda x, y: True,
                              lambda x, y: x)}
    f1_dict = {'condition1': (lambda x: True,
                              lambda x: x + 1)}
    f0 = 0
    bun = bunny.bunny.Bunny(f2_dict, f1_dict, f0, 'N')
    str1 = 'x'
    str2 = '-(x*a)'
    t1 = Term.parsed2term(bunny.term_parser.parse_str(str1))
    t2 = Term.parsed2term(bunny.term_parser.parse_str(str2))
    assert t1(bun, {'x': 0}) == 0
    assert t1(bun, {'x': 1}) == 1
    assert t2(bun, {'x': 0}) == 1
    assert t2(bun, {'x': 1}) == 2
    
def test_str2term():
    str1 = 'x'
    str2 = '-(x*a)'
    assert Term.str2term(str1).func_str == 'x'
    assert Term.str2term(str2).func_str == 'f1(f2(x,f0))'
    
def test_generate_ts():
    # term_parser.parse_str('a*[-x]') := ('a*[-x]', 2, 3, [0, 0], [2, 3, 1], [0, 2, 1])
    t0 = Term.str2term('a*(-x)')
    assert (t0 in generate_ts(4))
    assert (t0 not in generate_ts(2))