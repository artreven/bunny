'''
Created on May 13, 2013

@author: artem
'''
import time
import cProfile

import fca

import identity
import term_parser
import reducing
import bunny
from prover9mace4 import *

####SIZE = 2
id1 = identity.Identity.make_identity('x', 'x')
id2 = identity.Identity.make_identity('x', 'y')

####SIZE = 3
id3 = identity.Identity.make_identity('a', '-a')
id4 = identity.Identity.make_identity('a', '-x')
id5 = identity.Identity.make_identity('x', '-x')

####SIZE = 4
id6 = identity.Identity.make_identity('a', '-[-a]')
id7 = identity.Identity.make_identity('a', '-[-x]')
id8 = identity.Identity.make_identity('a', 'a*a')
id9 = identity.Identity.make_identity('a', 'a*x')
id10 = identity.Identity.make_identity('a', 'x*a')
id11 = identity.Identity.make_identity('a', 'x*x')
id12 = identity.Identity.make_identity('a', 'x*y')
id13 = identity.Identity.make_identity('-a', '-x')
id14 = identity.Identity.make_identity('x', '-[-x]')
id15 = identity.Identity.make_identity('x', 'a*x')
id16 = identity.Identity.make_identity('x', 'x*a')
id17 = identity.Identity.make_identity('x', 'x*x')
id18 = identity.Identity.make_identity('x', 'x*y')
id19 = identity.Identity.make_identity('x', 'y*x')

####SIZE = 5
id20 = identity.Identity.make_identity('a', '-[-[-a]]')
id21 = identity.Identity.make_identity('a', '-[-[-x]]')
id22 = identity.Identity.make_identity('a', 'a*[-a]')
id23 = identity.Identity.make_identity('a', 'a*[-x]')
id24 = identity.Identity.make_identity('a', '[-a]*a')
id25 = identity.Identity.make_identity('a', '[-a]*x')
id26 = identity.Identity.make_identity('a', 'x*[-a]')
id27 = identity.Identity.make_identity('a', 'x*[-x]')
id28 = identity.Identity.make_identity('a', 'x*[-y]')
id29 = identity.Identity.make_identity('a', '[-x]*a')
id30 = identity.Identity.make_identity('a', '[-x]*x')
id31 = identity.Identity.make_identity('a', '[-x]*y')
id32 = identity.Identity.make_identity('a', '-[a*a]')
id33 = identity.Identity.make_identity('a', '-[a*x]')
id34 = identity.Identity.make_identity('a', '-[x*a]')
id35 = identity.Identity.make_identity('a', '-[x*x]')
id36 = identity.Identity.make_identity('a', '-[x*y]')
id37 = identity.Identity.make_identity('-a', '-[-a]')
id38 = identity.Identity.make_identity('-a', '-[-x]')
id39 = identity.Identity.make_identity('-a', 'a*a')
id40 = identity.Identity.make_identity('-a', 'a*x')
id41 = identity.Identity.make_identity('-a', 'x*a')
id42 = identity.Identity.make_identity('-a', 'x*x')
id43 = identity.Identity.make_identity('-a', 'x*y')
id44 = identity.Identity.make_identity('x', '-[-[-x]]')
id45 = identity.Identity.make_identity('x', 'a*[-x]')
id46 = identity.Identity.make_identity('x', 'x*[-a]')
id47 = identity.Identity.make_identity('x', 'x*[-x]')
id48 = identity.Identity.make_identity('x', 'x*[-y]')
id49 = identity.Identity.make_identity('x', 'y*[-x]')
id50 = identity.Identity.make_identity('x', '[-a]*x')
id51 = identity.Identity.make_identity('x', '[-x]*a')
id52 = identity.Identity.make_identity('x', '[-x]*x')
id53 = identity.Identity.make_identity('x', '[-x]*y')
id54 = identity.Identity.make_identity('x', '[-y]*x')
id55 = identity.Identity.make_identity('x', '-[a*x]')
id56 = identity.Identity.make_identity('x', '-[x*a]')
id57 = identity.Identity.make_identity('x', '-[x*x]')
id58 = identity.Identity.make_identity('x', '-[x*y]')
id59 = identity.Identity.make_identity('x', '-[y*x]')
id60 = identity.Identity.make_identity('-x', '-[-x]')
id61 = identity.Identity.make_identity('-x', 'a*a')
id62 = identity.Identity.make_identity('-x', 'a*x')
id63 = identity.Identity.make_identity('-x', 'a*y')
id64 = identity.Identity.make_identity('-x', 'x*a')
id65 = identity.Identity.make_identity('-x', 'x*x')
id66 = identity.Identity.make_identity('-x', 'x*y')
id67 = identity.Identity.make_identity('-x', 'y*a')
id68 = identity.Identity.make_identity('-x', 'y*x')
id69 = identity.Identity.make_identity('-x', 'y*y')
id70 = identity.Identity.make_identity('-x', 'y*z')

id_ls = [id1, id2, id3, id4, id5, id6, id7, id8, id9, id10,
         id11, id12, id13, id14, id15, id16, id17, id18, id19, id20,
         id21, id22, id23, id24, id25, id26, id27, id28, id29, id30,
         id31, id32, id33, id34, id35, id36, id37, id38, id39, id40,
         id41, id42, id43, id44, id45, id46, id47, id48, id49, id50,
         id51, id52, id53, id54, id55, id56, id57, id58, id59, id60,
         id61, id62, id63, id64, id65, id66, id67, id68, id69, id70]

###############################################################################
from collections import defaultdict

size = 2
bun_num = 0
total_bun = size ** (size**2 + size + 1)

def foo1():
    now = time.time()
    now_part = now
    i_sat = defaultdict(int)
    i = 0
    for bun in bunny.bunnies(size):
        i += 1
        if (i % (total_bun/50)) == 0:
            out = '{}% complete'.format((100*i) / total_bun)
            out += '\t it took {} sec'.format(time.time() - now_part)
            print out
            now_part = time.time()
        for j in range(70):
            sat = bun.check_id(id_ls[j])
            if sat == True:
                i_sat[j] += 1
    for j in range(70):
        out = '{:4} bunnies satisfy id{:3} : {}'.format(i_sat[j], j+1, id_ls[j])
        print out
    print 'total execution time: {}'.format(time.time() - now)
        
def foo2(*ids):
    for id_ in ids:
        print id_
    for bun in bunny.bunnies(size):
        if all(bun.check_id(id_) for id_ in ids):
            print bun

def foo3(lim):
    res = []
    for k in range(70):
        for j in range(k+1, 70):
            sat = [(k, j)
                   for bun in bunny.bunnies(size) 
                   if bun.check_id(id_ls[k])
                   if bun.check_id(id_ls[j])]
            if (len(sat) > 0) and (len(sat) <= lim):
                res.append(sat)
    print len(res)
    return res

def init_cxt(size):
    obj_ls = []
    att_ls = map(str, id_ls)
    table = []
    for bun in bunny.bunnies(size):
        obj_ls.append(str(size) + '_' + str(bun.index))
        row = [bun.check_id(id_) for id_ in id_ls]
        table.append(row)
    cxt = fca.Context(table, obj_ls, att_ls)
    return cxt

if __name__ == '__main__':
    now = time.time()
    cxt = init_cxt(1)
    print time.time() - now
    bb = read_model('./prover9mace4/impl1_33mace4.out')