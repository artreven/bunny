'''
Created on May 13, 2013

@author: artem
'''
import fca

import auto_ae.ae as ae

from bunny import *
import identity
import p9m4

#####################Some necessary definitions to start########################
def read_ids(path):
    """
    Reads identities from given path. One identity per line.
    """
    id_ls = []
    with open(path, 'r') as f_ids:
        for line_id in f_ids:
            new_id = identity.Identity.func_str2id(line_id)
            id_ls.append(new_id)
    return id_ls

def init_cxt(size, id_ls):
    obj_ls = []
    att_ls = id_ls
    table = []
    for bun in bunnies(size):
        obj_ls.append(repr(bun))
        row = [bun.check_id(id_) for id_ in id_ls]
        table.append(row)
    cxt = fca.Context(table, obj_ls, map(str, att_ls))
    return cxt.reduce_objects()

dest = '../etc/test_run'
def ce_finder(imp, wait):
    if any(str(id_) == 'x = y' for id_ in imp.conclusion):
        old_conclusion = imp.conclsuion.copy()
        imp.conclusion = {id_ for id_ in imp.conclusion if str(id_) == 'x = y'} 
        proved = p9m4.prover9(imp, dest  + '/ces', wait / 100.)
        imp.conclsuion = old_conclusion
    else:
        proved = p9m4.prover9(imp, dest  + '/ces', wait / 100.)
    if proved == True:
        ans = (None, 'Implication proved.')
    else:
        found, reason = p9m4.mace4(imp, dest  + '/ces', wait / 100.)
        if not found == None:
            ans = (found, reason)
            premise = map(lambda x: identity.Identity.func_str2id(x), imp.premise)
            conclusion = map(lambda x: identity.Identity.func_str2id(x), imp.conclusion)
        else:
            premise = map(lambda x: identity.Identity.func_str2id(x), imp.premise)
            conclusion = map(lambda x: identity.Identity.func_str2id(x), imp.conclusion)
            id_imp = fca.Implication(premise, conclusion)
            bun, reason = InfBunny.find(id_imp, wait, kern_size=3)
            ans = (bun, reason)
    return ans

def has_attribute(object_repr, attr_name):
    id_ = identity.Identity.func_str2id(attr_name)
    bun = eval(object_repr)
    limit = None
    if type(bun) == InfBunny:
        limit = 8
    return bun.check_id(id_, limit=limit)

########MULTIPROCESSING
import multiprocessing as mp
import time

def f(l, i):
    l.acquire()
    print 'hello world', i
    l.release()

################################################################
if __name__ == '__main__':
    ################################################
#     lock = mp.Lock()
# 
#     for num in range(10):
#         mp.Process(target=f, args=(lock, num)).start()
#     
#     p1 = mp.Process(target=time.sleep, args=(1000,))
#     p2 = mp.Process(target=time.sleep, args=(3,))
#     p1.start()
#     p2.start()
#     while p2.is_alive():
#         pass
#     print 'Is p2 alive? -', p2.is_alive()
#     print 'Is p1 alive? -', p1.is_alive()
#     p1.terminate()
#     time.sleep(1)
#     print 'Is p1 alive? -', p1.is_alive()
#     print p1.exitcode, p2.exitcode
    #################################################
        
#     id_ls = read_ids('../utils/ids5.txt')
#     cxt = init_cxt(2, id_ls)
    cxt = fca.read_cxt('../etc/current_cxt.cxt')
    print 'context read'
    ae_bunnies = ae.AE(dest, cxt, has_attribute, ce_finder)
    ae_bunnies.step = 4174
    ae_bunnies.run(300, 1)

######################Identities manually###########################
####SIZE = 2
# id1 = be.Identity.make_identity('x=x')
# id2 = be.Identity.make_identity('x=y')
# 
# ####SIZE = 3
# id3 = be.Identity.make_identity('a=-a')
# id4 = be.Identity.make_identity('a=-x')
# id5 = be.Identity.make_identity('x=-x')
# 
# ####SIZE = 4
# id6 = be.Identity.make_identity('a=-(-a)')
# id7 = be.Identity.make_identity('a=-(-x)')
# id8 = be.Identity.make_identity('a=a*a')
# id9 = be.Identity.make_identity('a=a*x')
# id10 = be.Identity.make_identity('a=x*a')
# id11 = be.Identity.make_identity('a=x*x')
# id12 = be.Identity.make_identity('a=x*y')
# id13 = be.Identity.make_identity('-a=-x')
# id14 = be.Identity.make_identity('x=-(-x)')
# id15 = be.Identity.make_identity('x=a*x')
# id16 = be.Identity.make_identity('x=x*a')
# id17 = be.Identity.make_identity('x=x*x')
# id18 = be.Identity.make_identity('x=x*y')
# id19 = be.Identity.make_identity('x=y*x')
# 
# ####SIZE = 5
# id20 = be.Identity.make_identity('a=-(-(-a))')
# id21 = be.Identity.make_identity('a=-(-(-x))')
# id22 = be.Identity.make_identity('a=a*(-a)')
# id23 = be.Identity.make_identity('a=a*(-x)')
# id24 = be.Identity.make_identity('a=(-a)*a')
# id25 = be.Identity.make_identity('a=(-a)*x')
# id26 = be.Identity.make_identity('a=x*(-a)')
# id27 = be.Identity.make_identity('a=x*(-x)')
# id28 = be.Identity.make_identity('a=x*(-y)')
# id29 = be.Identity.make_identity('a=(-x)*a')
# id30 = be.Identity.make_identity('a=(-x)*x')
# id31 = be.Identity.make_identity('a=(-x)*y')
# id32 = be.Identity.make_identity('a=-(a*a)')
# id33 = be.Identity.make_identity('a=-(a*x)')
# id34 = be.Identity.make_identity('a=-(x*a)')
# id35 = be.Identity.make_identity('a=-(x*x)')
# id36 = be.Identity.make_identity('a=-(x*y)')
# id37 = be.Identity.make_identity('-a=-(-a)')
# id38 = be.Identity.make_identity('-a=-(-x)')
# id39 = be.Identity.make_identity('-a=a*a')
# id40 = be.Identity.make_identity('-a=a*x')
# id41 = be.Identity.make_identity('-a=x*a')
# id42 = be.Identity.make_identity('-a=x*x')
# id43 = be.Identity.make_identity('-a=x*y')
# id44 = be.Identity.make_identity('x=-(-(-x))')
# id45 = be.Identity.make_identity('x=a*(-x)')
# id46 = be.Identity.make_identity('x=x*(-a)')
# id47 = be.Identity.make_identity('x=x*(-x)')
# id48 = be.Identity.make_identity('x=x*(-y)')
# id49 = be.Identity.make_identity('x=y*(-x)')
# id50 = be.Identity.make_identity('x=(-a)*x')
# id51 = be.Identity.make_identity('x=(-x)*a')
# id52 = be.Identity.make_identity('x=(-x)*x')
# id53 = be.Identity.make_identity('x=(-x)*y')
# id54 = be.Identity.make_identity('x=(-y)*x')
# id55 = be.Identity.make_identity('x=-(a*x)')
# id56 = be.Identity.make_identity('x=-(x*a)')
# id57 = be.Identity.make_identity('x=-(x*x)')
# id58 = be.Identity.make_identity('x=-(x*y)')
# id59 = be.Identity.make_identity('x=-(y*x)')
# id60 = be.Identity.make_identity('-x=-(-x)')
# id61 = be.Identity.make_identity('-x=a*a')
# id62 = be.Identity.make_identity('-x=a*x')
# id63 = be.Identity.make_identity('-x=a*y')
# id64 = be.Identity.make_identity('-x=x*a')
# id65 = be.Identity.make_identity('-x=x*x')
# id66 = be.Identity.make_identity('-x=x*y')
# id67 = be.Identity.make_identity('-x=y*a')
# id68 = be.Identity.make_identity('-x=y*x')
# id69 = be.Identity.make_identity('-x=y*y')
# id70 = be.Identity.make_identity('-x=y*z')
# 
# ####SIZE = 6
# id71 = be.Identity.make_identity('a*x=-(-a)')
# id72 = be.Identity.make_identity('a*x=-(-x)')
# id73 = be.Identity.make_identity('a*x=a*a')
# id74 = be.Identity.make_identity('a*x=a*x')
# id75 = be.Identity.make_identity('a*x=x*a')
# id76 = be.Identity.make_identity('a*x=x*x')
# id77 = be.Identity.make_identity('a*x=x*y')
# id78 = be.Identity.make_identity('(-a)*x=-x')
# id79 = be.Identity.make_identity('x*x=-(-x)')
# id80 = be.Identity.make_identity('x*x=a*x')
# id81 = be.Identity.make_identity('x*x=x*a')
# id82 = be.Identity.make_identity('x*x=x*x')
# id83 = be.Identity.make_identity('x*x=x*y')
# id84 = be.Identity.make_identity('x*y=y*x')
# 
# id85 = be.Identity.make_identity('x*(-x)=(-x)*x')
# id86 = be.Identity.make_identity('x*(y*z)=(x*y)*z')
# 
# id_ls_manually = [id1, id2, id3, id4, id5, id6, id7, id8, id9, id10,
#                   id11, id12, id13, id14, id15, id16, id17, id18, id19, id20,
#                   id21, id22, id23, id24, id25, id26, id27, id28, id29, id30,
#                   id31, id32, id33, id34, id35, id36, id37, id38, id39, id40,
#                   id41, id42, id43, id44, id45, id46, id47, id48, id49, id50,
#                   id51, id52, id53, id54, id55, id56, id57, id58, id59, id60,
#                   id61, id62, id63, id64, id65, id66, id67, id68, id69, id70,
#                   id71, id72, id73, id74, id75, id76, id77, id78, id79, id80,
#                   id81, id82, id83, id84, id85, id86]