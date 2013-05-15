'''
Created on May 13, 2013

@author: artem
'''
import fca

import identity
import term_parser
import reducing

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

if __name__ == '__main__':
    t0 = 'x'
    t1 = 'a'
    t2 = 'a*x'
    parsed = term_parser.make_input(True, t0, t1, t2)
    print parsed