"""Holds functions for parsing mathematical terms given in strings
and preparing input for bunny_test

For EXAMPLES see ./tests/test_parser.py"""

from functools import update_wrapper
from string import split
from collections import Iterable
import re

def grammar(description, whitespace=r'\s*'):
    """Convert a description to a grammar.  Each line is a rule for a
    non-terminal symbol; it looks like this:
        Symbol =>  A1 A2 ... | B1 B2 ... | C1 C2 ...
    where the right-hand side is one or more alternatives, separated by
    the '|' sign.  Each alternative is a sequence of atoms, separated by
    spaces.  An atom is either a symbol on some left-hand side, or it is
    a regular expression that will be passed to re.match to match a token.
    
    Notation for *, +, or ? not allowed in a rule alternative (but ok
    within a token). Use '\' to continue long lines.  You must include spaces
    or tabs around '=>' and '|'. That's within the grammar description itself.
    The grammar that gets defined allows whitespace between tokens by default;
    specify '' as the second argument to grammar() to disallow this (or supply
    any regular expression to describe allowable whitespace between tokens)."""
    G = {' ': whitespace}
    description = description.replace('\t', ' ') # no tabs!
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
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
            return f(args)
    return _f

def parse(start_symbol, text, grammar):
    """Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure iff remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T'"""

    tokenizer = grammar[' '] + '(%s)'

    def parse_sequence(sequence, text):
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
        return result, text

    @memo
    def parse_atom(atom, text):
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom]+tree, rem  
            return Fail
        else:  # Terminal: match characters against start of text
            m = re.match(tokenizer % atom, text)
            return Fail if (not m) else (m.group(1), text[m.end():])
    
    # Body of parse:
    return parse_atom(start_symbol, text)

Fail = (None, None)

term_grammar = grammar("""val => exp bin val | exp
exp => sym bin exp | [[] exp []] | un exp | sym
bin => [*]
un => -
sym => var | nul
var => un [w-z] | [w-z]
nul => un [a-c] | [a-c]""", whitespace='\s*')
                  
def term_parse(text):
    return parse('val', text, term_grammar)

def parse_str(text):
    """This function takes term in form of string and returns the name,
    two sizes of arrays and lists of elements, orders of operations, and
    the types of operations in the form, compatible with bunny_test programm.
    
    First it parses the text, then it flattens parsed with tracking. Inversed
    tracked levels are exactly the priorities of operations.
    
    NOTE Spaces are allowed and processed correctly here, but can not be
    processed correctly when input to bunny_test, so dont use spaces in
    terms"""
    parsed = term_parse(text)[0]
    flattened = flatten(parsed, track=True)

    elements = []
    types = []
    order = []
    for i in flattened:
        if i[0] in 'wxyz':
            d = {'x' : 0,
                 'y' : 1,
                 'z' : 2,
                 'w' : 3}
            elements.append(d[i[0]])
        elif i[0] == 'nul':
            elements.append(0)
            types.append(0)
            order.append(i[1])
        elif i[0] == 'un':
            types.append(1)
            order.append(i[1])
        elif i[0] == 'bin':
            types.append(2)
            order.append(i[1])
    if order:
        m = max(order)
        order = [(m - i + 1) for i in order]
    return text, len(elements), len(order), elements, order, types

def flatten(lst, track=False):
    """
    Flattens iterable input, except strings
    """
    
    def make_flat(lst, result, level):
        if track:
            level += 1
        for i in lst:
            if isinstance(i, Iterable) and type(i) is not str:
                make_flat(i, result, level)
            else:
                if track:
                    result.append((i,level))
                else: 
                    result.append(i)
        return result
    
    return make_flat(lst, [], 0)

def make_input(with_term_names, *term_strings):
    """
    Prepares input for bunny_test. if with_term_names == True, then output
    contains names of terms.
    """
    num = len(term_strings)
    result = [str(num)]
    for term_string in term_strings:
        if with_term_names:
            result += [str(i) for i in flatten( parse_str(term_string) )]
        elif not with_term_names:
            result += [str(i) for i in flatten( parse_str(term_string)[1:] )]
    return result