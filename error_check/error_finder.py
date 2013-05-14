"""
Holds functions for finding errors in object intents
"""
from copy import deepcopy
from itertools import chain, combinations
import re

from fca import Context, Implication
from fca.algorithms.closure_operators import oprime, aprime


def split_implications(imps):
    """
    Split implications from set imps in unit implications
    """
    unit_imps = set()
    for imp in imps:
        for str_conclusion in imp.conclusion:
            conclusion = set()
            conclusion.add(str_conclusion)
            unit_imps.add( Implication(imp.premise, conclusion) )
    return unit_imps

def inspect_dg_empty(cxt, objs_inds, imp_basis=None):
    """
    Finds those implication, that hold in context without objects but are not
    respected by objects
    Allows for implications to have empty support.
    """
    new_cxt = deepcopy(cxt)
    for obj in objs_inds[::-1]:
        new_cxt.delete_object(obj)
    if imp_basis == None:
        imp_basis = new_cxt.attribute_implications
    result = []
    cxt.get_int = cxt.get_object_intent_by_index
    for imp in imp_basis:
        if all([not imp.is_respected(cxt.get_int(obj)) for obj in objs_inds]):
            result.append(imp)
    return result

def inspect_errors_a_12(cxt_original, objs_indices):
    """
    Inspect objects objs_inds (indices) from cxt.
    
    Returns a set of implications of Types A -> b and A -> not(b),
    that are respected by all the objects of the context,
    but the objects objs_inds.
    """
    obj_intents = [cxt_original.get_object_intent_by_index(obj_ind)
                   for obj_ind in objs_indices]
    new_inds = set(range(len(cxt_original))) - set(objs_indices)
    table = [cxt_original[i] for i in new_inds]
    objects = [cxt_original.objects[i] for i in new_inds]
    attributes = cxt_original.attributes
    cxt = Context(table, objects, attributes)
        
    common_attrs = reduce(set.intersection, obj_intents)
    candidates = set([frozenset(int & common_attrs) for int in cxt.intents()])
    included = lambda x: not any([x < cand for cand in candidates])
    candidates = filter(included, candidates)
    imps = set()
    for cand in candidates:
        cand_closure = oprime(aprime(cand, cxt), cxt)
        negated_attrs = set( map(lambda x: 'not ' + x,
                                 (common_attrs - cand)) )
        if negated_attrs != set():
            imps.add( Implication(cand, negated_attrs) )
        if all([not (cand_closure <= obj_intent)
                for obj_intent in obj_intents]):
            imps.add( Implication(cand, (cand_closure - common_attrs)) )
    return imps

def make_dual_imps(imps):
    """
    First split imps in unit imps, then return imps with negated conclusions
    """
    unit_imps = split_implications(imps)
    dual_imps = set()
    for imp in unit_imps:
        for str_conc in imp.conclusion:
            pass
        if (re.match(r'not ', str_conc) != None):
            new_conc = str_conc[4:]
        elif (re.match(r'not ', str_conc) == None):
            new_conc = 'not ' + str_conc
        dual_imps.add( Implication(imp.premise, frozenset((new_conc, ))) )
    return dual_imps

def minimize_premise(cxt, imp):
    """
    Minimize premise in naive manner by simple iterating though all subsets.
    First found is used.
    """
    def powerset(iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    
    premise = imp.premise
    generators = set()
    for subset in powerset(premise):
        subset = frozenset(subset)
        pos_conc = set([conc_attr for conc_attr in imp.conclusion
                        if (re.match(r'not ', conc_attr) == None)])
        neg_conc = set([conc_attr[4:] for conc_attr in imp.conclusion
                        if (re.match(r'not ', conc_attr) != None)])
        closure = oprime(aprime(subset, cxt), cxt)
        if (pos_conc <= closure and
            premise <= closure and
            not any([gen < subset for gen in generators]) and
            all([(not (neg_attr in closure)) for neg_attr in neg_conc])):
            generators.add(subset)
            break
    return [Implication(set(min_gen), imp.conclusion) for min_gen in generators]