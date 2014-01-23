'''
Created on May 13, 2013

@author: artem
'''
import time
import cProfile
import os

import fca

import bunny_exploration as be

####SIZE = 2
id1 = be.Identity.make_identity('x=x')
id2 = be.Identity.make_identity('x=y')

####SIZE = 3
id3 = be.Identity.make_identity('a=-a')
id4 = be.Identity.make_identity('a=-x')
id5 = be.Identity.make_identity('x=-x')

####SIZE = 4
id6 = be.Identity.make_identity('a=-(-a)')
id7 = be.Identity.make_identity('a=-(-x)')
id8 = be.Identity.make_identity('a=a*a')
id9 = be.Identity.make_identity('a=a*x')
id10 = be.Identity.make_identity('a=x*a')
id11 = be.Identity.make_identity('a=x*x')
id12 = be.Identity.make_identity('a=x*y')
id13 = be.Identity.make_identity('-a=-x')
id14 = be.Identity.make_identity('x=-(-x)')
id15 = be.Identity.make_identity('x=a*x')
id16 = be.Identity.make_identity('x=x*a')
id17 = be.Identity.make_identity('x=x*x')
id18 = be.Identity.make_identity('x=x*y')
id19 = be.Identity.make_identity('x=y*x')

####SIZE = 5
id20 = be.Identity.make_identity('a=-(-(-a))')
id21 = be.Identity.make_identity('a=-(-(-x))')
id22 = be.Identity.make_identity('a=a*(-a)')
id23 = be.Identity.make_identity('a=a*(-x)')
id24 = be.Identity.make_identity('a=(-a)*a')
id25 = be.Identity.make_identity('a=(-a)*x')
id26 = be.Identity.make_identity('a=x*(-a)')
id27 = be.Identity.make_identity('a=x*(-x)')
id28 = be.Identity.make_identity('a=x*(-y)')
id29 = be.Identity.make_identity('a=(-x)*a')
id30 = be.Identity.make_identity('a=(-x)*x')
id31 = be.Identity.make_identity('a=(-x)*y')
id32 = be.Identity.make_identity('a=-(a*a)')
id33 = be.Identity.make_identity('a=-(a*x)')
id34 = be.Identity.make_identity('a=-(x*a)')
id35 = be.Identity.make_identity('a=-(x*x)')
id36 = be.Identity.make_identity('a=-(x*y)')
id37 = be.Identity.make_identity('-a=-(-a)')
id38 = be.Identity.make_identity('-a=-(-x)')
id39 = be.Identity.make_identity('-a=a*a')
id40 = be.Identity.make_identity('-a=a*x')
id41 = be.Identity.make_identity('-a=x*a')
id42 = be.Identity.make_identity('-a=x*x')
id43 = be.Identity.make_identity('-a=x*y')
id44 = be.Identity.make_identity('x=-(-(-x))')
id45 = be.Identity.make_identity('x=a*(-x)')
id46 = be.Identity.make_identity('x=x*(-a)')
id47 = be.Identity.make_identity('x=x*(-x)')
id48 = be.Identity.make_identity('x=x*(-y)')
id49 = be.Identity.make_identity('x=y*(-x)')
id50 = be.Identity.make_identity('x=(-a)*x')
id51 = be.Identity.make_identity('x=(-x)*a')
id52 = be.Identity.make_identity('x=(-x)*x')
id53 = be.Identity.make_identity('x=(-x)*y')
id54 = be.Identity.make_identity('x=(-y)*x')
id55 = be.Identity.make_identity('x=-(a*x)')
id56 = be.Identity.make_identity('x=-(x*a)')
id57 = be.Identity.make_identity('x=-(x*x)')
id58 = be.Identity.make_identity('x=-(x*y)')
id59 = be.Identity.make_identity('x=-(y*x)')
id60 = be.Identity.make_identity('-x=-(-x)')
id61 = be.Identity.make_identity('-x=a*a')
id62 = be.Identity.make_identity('-x=a*x')
id63 = be.Identity.make_identity('-x=a*y')
id64 = be.Identity.make_identity('-x=x*a')
id65 = be.Identity.make_identity('-x=x*x')
id66 = be.Identity.make_identity('-x=x*y')
id67 = be.Identity.make_identity('-x=y*a')
id68 = be.Identity.make_identity('-x=y*x')
id69 = be.Identity.make_identity('-x=y*y')
id70 = be.Identity.make_identity('-x=y*z')

####SIZE = 6
id71 = be.Identity.make_identity('a*x=-(-a)')
id72 = be.Identity.make_identity('a*x=-(-x)')
id73 = be.Identity.make_identity('a*x=a*a')
id74 = be.Identity.make_identity('a*x=a*x')
id75 = be.Identity.make_identity('a*x=x*a')
id76 = be.Identity.make_identity('a*x=x*x')
id77 = be.Identity.make_identity('a*x=x*y')
id78 = be.Identity.make_identity('(-a)*x=-x')
id79 = be.Identity.make_identity('x*x=-(-x)')
id80 = be.Identity.make_identity('x*x=a*x')
id81 = be.Identity.make_identity('x*x=x*a')
id82 = be.Identity.make_identity('x*x=x*x')
id83 = be.Identity.make_identity('x*x=x*y')
id84 = be.Identity.make_identity('x*y=y*x')

id85 = be.Identity.make_identity('x*(-x)=(-x)*x')
id86 = be.Identity.make_identity('x*(y*z)=(x*y)*z')

id_ls = [id1, id2, id3, id4, id5, id6, id7, id8, id9, id10,
         id11, id12, id13, id14, id15, id16, id17, id18, id19, id20,
         id21, id22, id23, id24, id25, id26, id27, id28, id29, id30,
         id31, id32, id33, id34, id35, id36, id37, id38, id39, id40,
         id41, id42, id43, id44, id45, id46, id47, id48, id49, id50,
         id51, id52, id53, id54, id55, id56, id57, id58, id59, id60,
         id61, id62, id63, id64, id65, id66, id67, id68, id69, id70,
         id71, id72, id73, id74, id75, id76, id77, id78, id79, id80,
         id81, id82, id83, id84, id85, id86]

###############################################################################
def init_cxt(size):
    obj_ls = []
    att_ls = id_ls
    table = []
    for bun in be.bunnies(size):
        obj_ls.append(bun)
        row = [bun.check_id(id_) for id_ in id_ls]
        table.append(row)
    cxt = fca.Context(table, obj_ls, att_ls)
    return cxt.reduce_objects()

def ce_finder(basis, dest, wait):
    limit = 10
    ce_dict = {}
    fin = 0
    no_ces = 0
    bun = None
    prev = None
    found = {}
    proved = []
    for imp in basis:
        for j in (imp.conclusion - imp.premise):
            atomic_imp = fca.Implication(imp.premise, set((j,)))
            # first try mace
            if wait[1] >= 0:
                found = be.mace4((atomic_imp,), dest  + '/ces', wait[1])
            if found != {}:
                fin += 1
                no_ces += 1
                ce_dict.update(found)
            elif found == {}:
                if wait[2] >= 0:
                    (proved, _) = be.prover9((atomic_imp,), dest  + '/ces', wait[2])
                if len(proved) == 1:
                    continue
                elif len(proved) == 0:
                    bun = be.InfBunny.find(imp.premise, j, limit, wait[0], prev)
                    if bun != None:
                        prev = bun
                        ce_dict[atomic_imp] = bun
                        no_ces += 1
    inf = no_ces - fin
    m = '\n\n\n***{0} CEs found: {1} finite and {2} infinite\n'.format(no_ces, fin, inf)
    with open(dest + '/progress.txt', 'a') as file:
        file.write(m)
    file.close()
    print dest
    print m
    return ce_dict

if __name__ == '__main__':
    import getpass
    
    cxt = init_cxt(2)
    dest = os.path.expanduser('~') + '/Dropbox/personal/Scripts/AptanaWorkspace/MIW/bunny_exploration/70ids_leq5/3'
    prover = be.prover9
    ae = be.AE(cxt, dest, prover, ce_finder)
    ae.run((5, 1, 1), 2)