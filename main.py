import subprocess

#from tab_separated_objs_names import read_txt_objs_names
from reducing import *
from bunny_exploration.term_parser import make_input

bunny_list_test_path = './bunny_test_C/bin/bunny_list_test'
bunny_interval_test_path = './bunny_test_C/bin/bunny_interval_test'
args2 = ('3 attr1 2 3 0 0 3 2 1 1 2 0 attr2 2 3 0 0 3 2 1 1 2 0 attr3 2 3 0 0 2 3 1 1 2 0 3 0 1000 0 10 0 3').split()

'''str1 = "-x*a"
str2 = "-[x*a]"
exprs = make_input(True, str1, str2)
print exprs + ('3 0 1000 0 10 0 3').split()
print args2'''

str1 = "-x*a"
str2 = "-[x*a]"
str3 = "x*x"
exprs = make_input(True, str1, str2, str3)
subprocess.call([bunny_interval_test_path] + exprs + ('3 0 1000 0 10 0 3').split())
cxt_path = 'cxt.txt'
#cxt = read_txt_objs_names(cxt_path)
cProfile.run('clarify_objects(cxt)')
#print clarify_objects(cxt)