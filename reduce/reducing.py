"""
Holds functions for clarifing and reducing contexts.

TOD: reduce_attributes, clarify_attributes, clarify_context, reduce_context
"""
from fca.context import Context

def clarify_objects(cxt):
    """
    Objects clarification
    Objects with intent equal to all attributes are not deleted.
    """
    if type(cxt) != Context:
        raise TypeError("An input object should be a context!")
    
    dict_cxt = dict(zip(map(tuple, cxt), cxt.objects))
    table = map(list, dict_cxt.keys())
    objects = dict_cxt.values()
    return Context(table, objects, cxt.attributes)
    
def reduce_objects(cxt):
    """
    Objects reducing.
    """
    if type(cxt) != Context:
        raise TypeError("An input object should be a context!")
    
    def int_repr(arr):
        """
        Represent every object's intent as decimal number as in list_to_number
        """
        return map(bool_list_bitvalue, arr)
    
    dict_cxt = dict(zip(int_repr(cxt), range(len(cxt))))#clarification
    keys = dict_cxt.keys()
    reducible = set()
    M = (1 << len(cxt.attributes)) - 1                  #set of attributes repr
    for i in range(len(keys)):                          #checking if i reducible
        if i in reducible:
            continue 
        rest = keys[:i] + keys[i+1:]
        current = new = M
        for j in rest:
            if j in reducible:
                continue
            i_int = keys[i]
            new = current & j
            if new & i_int < i_int:
                continue
            elif new == i_int:
                reducible.add(i_int)
            elif new > i_int:
                current = new
    for i in reducible:
        del dict_cxt[i]
    objects = [cxt.objects[i] for i in dict_cxt.values()]
    table = [cxt[i] for i in dict_cxt.values()]
    return Context(table, objects, cxt.attributes)

def bool_list_bitvalue(lst):
    """
    input lst - list of Trues and Falses. Translate them to 1s and 0s,
    then concatenate in binstring, then make it decimal integer
    """
    return int(''.join([str(int(i)) for i in lst]), 2)