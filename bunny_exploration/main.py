'''
Created on May 13, 2013

@author: artem
'''
import time
import cProfile

import fca

import reducing
import bunny_exploration as be

####SIZE = 2
id1 = be.Identity.make_identity('x', 'x')
id2 = be.Identity.make_identity('x', 'y')

####SIZE = 3
id3 = be.Identity.make_identity('a', '-a')
id4 = be.Identity.make_identity('a', '-x')
id5 = be.Identity.make_identity('x', '-x')

####SIZE = 4
id6 = be.Identity.make_identity('a', '-(-a)')
id7 = be.Identity.make_identity('a', '-(-x)')
id8 = be.Identity.make_identity('a', 'a*a')
id9 = be.Identity.make_identity('a', 'a*x')
id10 = be.Identity.make_identity('a', 'x*a')
id11 = be.Identity.make_identity('a', 'x*x')
id12 = be.Identity.make_identity('a', 'x*y')
id13 = be.Identity.make_identity('-a', '-x')
id14 = be.Identity.make_identity('x', '-(-x)')
id15 = be.Identity.make_identity('x', 'a*x')
id16 = be.Identity.make_identity('x', 'x*a')
id17 = be.Identity.make_identity('x', 'x*x')
id18 = be.Identity.make_identity('x', 'x*y')
id19 = be.Identity.make_identity('x', 'y*x')

####SIZE = 5
id20 = be.Identity.make_identity('a', '-(-(-a))')
id21 = be.Identity.make_identity('a', '-(-(-x))')
id22 = be.Identity.make_identity('a', 'a*(-a)')
id23 = be.Identity.make_identity('a', 'a*(-x)')
id24 = be.Identity.make_identity('a', '(-a)*a')
id25 = be.Identity.make_identity('a', '(-a)*x')
id26 = be.Identity.make_identity('a', 'x*(-a)')
id27 = be.Identity.make_identity('a', 'x*(-x)')
id28 = be.Identity.make_identity('a', 'x*(-y)')
id29 = be.Identity.make_identity('a', '(-x)*a')
id30 = be.Identity.make_identity('a', '(-x)*x')
id31 = be.Identity.make_identity('a', '(-x)*y')
id32 = be.Identity.make_identity('a', '-(a*a)')
id33 = be.Identity.make_identity('a', '-(a*x)')
id34 = be.Identity.make_identity('a', '-(x*a)')
id35 = be.Identity.make_identity('a', '-(x*x)')
id36 = be.Identity.make_identity('a', '-(x*y)')
id37 = be.Identity.make_identity('-a', '-(-a)')
id38 = be.Identity.make_identity('-a', '-(-x)')
id39 = be.Identity.make_identity('-a', 'a*a')
id40 = be.Identity.make_identity('-a', 'a*x')
id41 = be.Identity.make_identity('-a', 'x*a')
id42 = be.Identity.make_identity('-a', 'x*x')
id43 = be.Identity.make_identity('-a', 'x*y')
id44 = be.Identity.make_identity('x', '-(-(-x))')
id45 = be.Identity.make_identity('x', 'a*(-x)')
id46 = be.Identity.make_identity('x', 'x*(-a)')
id47 = be.Identity.make_identity('x', 'x*(-x)')
id48 = be.Identity.make_identity('x', 'x*(-y)')
id49 = be.Identity.make_identity('x', 'y*(-x)')
id50 = be.Identity.make_identity('x', '(-a)*x')
id51 = be.Identity.make_identity('x', '(-x)*a')
id52 = be.Identity.make_identity('x', '(-x)*x')
id53 = be.Identity.make_identity('x', '(-x)*y')
id54 = be.Identity.make_identity('x', '(-y)*x')
id55 = be.Identity.make_identity('x', '-(a*x)')
id56 = be.Identity.make_identity('x', '-(x*a)')
id57 = be.Identity.make_identity('x', '-(x*x)')
id58 = be.Identity.make_identity('x', '-(x*y)')
id59 = be.Identity.make_identity('x', '-(y*x)')
id60 = be.Identity.make_identity('-x', '-(-x)')
id61 = be.Identity.make_identity('-x', 'a*a')
id62 = be.Identity.make_identity('-x', 'a*x')
id63 = be.Identity.make_identity('-x', 'a*y')
id64 = be.Identity.make_identity('-x', 'x*a')
id65 = be.Identity.make_identity('-x', 'x*x')
id66 = be.Identity.make_identity('-x', 'x*y')
id67 = be.Identity.make_identity('-x', 'y*a')
id68 = be.Identity.make_identity('-x', 'y*x')
id69 = be.Identity.make_identity('-x', 'y*y')
id70 = be.Identity.make_identity('-x', 'y*z')

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
    for bun in be.bunnies(size):
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
    for bun in be.bunnies(size):
        if all(bun.check_id(id_) for id_ in ids):
            print bun

def foo3(lim):
    res = []
    for k in range(70):
        for j in range(k+1, 70):
            sat = [(k, j)
                   for bun in be.bunnies(size) 
                   if bun.check_id(id_ls[k])
                   if bun.check_id(id_ls[j])]
            if (len(sat) > 0) and (len(sat) <= lim):
                res.append(sat)
    print len(res)
    return res

def init_cxt(size):
    obj_ls = []
    att_ls = id_ls
    table = []
    for bun in be.bunnies(size):
        obj_ls.append(bun)
        row = [bun.check_id(id_) for id_ in id_ls]
        table.append(row)
    cxt = fca.Context(table, obj_ls, att_ls)
    return cxt

if __name__ == '__main__':
    now = time.time()
    cxt = init_cxt(2)
    dest = '/home/artreven/Dropbox/personal/Scripts/AptanaWorkspace/MIW/bunny_exploration/70ids_size_leq_5'
    ae = be.AE(cxt, dest)
    ae.run()
    print time.time() - now