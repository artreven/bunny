'''
Use with nosetests (https://nose.readthedocs.org/en/latest/)

Created on Dec 9, 2012

@author: artem
'''
#from fca.readwrite import write_cxt
from error_check.debug import *

class Test_toy(object):

    def setUp(self):
        def foo(x):
            x += 1
            return x
        self.inputs = [-2, -1, 0, 1]
        self.debugger = eexp_debugger.EExpDebugger(foo, lambda x: x > 0,
                                                   self.inputs)
        self.frame = lambda: None
        self.frame.f_lineno = 24
        (self.cxt_pass, self.cxt_fail) = self.debugger.make_contexts()
        
    def tearDown(self):
        pass

    def test_traceit(self):
        self.debugger._traceit(self.frame, "line", 0)
        assert self.debugger.coverage[repr(self.frame.f_lineno)]
        
    def test_run_tests1(self):
        runs = self.debugger.run_tests() #runs = [(input1, outcome1, coverage1), ...]
        below_zeros_inds = [self.debugger.inputs.index(i)
                            for i in self.debugger.inputs if i < 0]
        for fail_ind in below_zeros_inds:
            assert runs[fail_ind][1] == "FAIL"
        for i in range(len(runs)):
            assert "15" in runs[i][2].keys()
    
    def test_run_tests2(self):
        inputs = [-1, 0]
        runs = self.debugger.run_tests(inputs)
        below_zeros_inds = [inputs.index(i)
                            for i in self.debugger.inputs if i < 0]
        for fail_ind in below_zeros_inds:
            assert runs[fail_ind][1] == "FAIL"
        for i in range(len(runs)):
            assert "15" in runs[i][2].keys()
        assert self.debugger.inputs == inputs
            
    def test_make_contexts(self):
        assert (self.cxt_pass.get_object_intent(repr(self.inputs[2])) ==
                set(["15->15", "16->16"]))
        assert len(self.cxt_pass) == 2
        assert (self.cxt_fail.get_object_intent(repr(self.inputs[0])) ==
                set(["15->15", "16->16"]))
        assert len(self.cxt_fail) == 2
        
    def test_make_seq_contexts(self):
        #print self.debugger.make_seq_contexts()
        pass
    
    def test_explore_bugs1(self):
        self.debugger.explore_bugs(self.cxt_pass, self.cxt_fail)
        assert True
        
    def test_explore_bugs2(self):
        # The buggy program
        def remove_html_markup(s):
            tag   = False
            quote = False
            out   = ""
            for c in s:
                if (c == '<' and
                    not quote):
                    tag = True
                elif (c == '>' and
                      not quote):
                    tag = False
                elif (c == '"' or
                      c == "'" and
                      tag):
                    quote = not quote
                elif not tag:
                    out = out + c
            return out
        
        def goal(result):
            return result.find('<') == -1
        
        inputs_line = ['foo', 
                       '<b>foo</b>', 
                       '"<b>foo</b>"',
                       '"<b>a</b>"',
                       '"<b></b>"',
                       '"<>"',
                       '"foo"',
                       "'foo'", 
                       '<em>foo</em>', 
                       '<a href="foo">foo</a>',
                       '""',
                       '<"">',
                       "<p>",
                       '<a href=">">foo</a>']
        debugger = eexp_debugger.EExpDebugger(remove_html_markup, goal,
                                              inputs_line)
        (cxt_pass, cxt_fail) = debugger.make_contexts()
        print cxt_pass
        print cxt_fail
        print (debugger.explore_bugs(cxt_pass, cxt_fail))
        print '\n\n\n'
        #write_cxt(cxt_pass, './cxt_pass.cxt')
        #write_cxt(cxt_fail, './cxt_fail.cxt')
        (cxt_pass, cxt_fail) = debugger.make_contexts(delay=1)
        print cxt_pass
        print cxt_fail
        print (debugger.explore_bugs(cxt_pass, cxt_fail))