'''
Debugger based on error exploration of lines coverage for passes and failures

"EExp" stands for "error exploration". 

Created on Dec 9, 2012

@author: Artem Revenko
'''
import inspect
import sys
from copy import deepcopy

from fca import Context

from error_check.error_finder import inspect_errors_a_12 as inspect_errors
from error_check.error_finder import minimize_premise


class EExpDebugger(object):
    '''
    classdocs
    '''

    def __init__(self, function, goal, inputs=[]):
        '''
        Constructor
        '''
        self.function = function
        self.goal = goal
        self.inputs = inputs
        self.coverage = {}
        self.order_counter = 0
        (self.source_code, self.first_line) = inspect.getsourcelines(
                                                        self.function)
        
    def _traceit(self, frame, event, arg):
        '''
        Tracing function that saves the coverage data.
        To track function calls, you will have to check 'if event == "return"',
        and in that case the variable arg will hold the return value
        of the function, and frame.f_code.co_name will hold the function name.
        '''
        if event == "line":
            lineno = frame.f_lineno
            self.order_counter += 1
            self.coverage[repr(lineno)] = self.order_counter
            
        return self._traceit
    
    def run_tests(self, inputs=None):
        '''
        Run the program with each test case and record input, outcome and
        coverage of lines.
        Rewrite inputs (if given) in self.inputs.
        '''
        if inputs == None:
            inputs = self.inputs
        self.inputs = inputs
        
        runs = []
        for input_ in inputs:
            self.coverage = {}
            self.order_counter = 0
            sys.settrace(self._traceit)
            result = self.function(input_)
            sys.settrace(None)    
            if self.goal(result):
                outcome = "PASS"
            else:
                outcome = "FAIL"
            runs.append((input_, outcome, self.coverage))
        return runs
    
    def make_contexts(self, runs=None, inputs=None, delay=0):
        '''
        Create two contexts: one with successful runs, another with failures.
        input is used as object names, outcome determines to which
        context belongs an object. Attributes are pairs of 
        line numbers of the source code of self.function. Having X in context
        means that during particular run (defined by input) second line in pair
        was executed after first line in pair. 
        @param delay: TODO
        '''
        def make_attr(attr):
            '''
            TODO
            '''
            (line_no1, _, line_no2) = attr.partition("->")
            keys = coverage.keys()
            return (0 <= (coverage[line_no2] - coverage[line_no1]) <= delay
                    if (line_no1 in keys and line_no2 in keys)
                    else False) 
        attrs = [repr(line_no1) + "->" + repr(line_no2)
                 for line_no1 in range(self.first_line,
                                       self.first_line +
                                       len(self.source_code))
                 for line_no2 in range(self.first_line,
                                       self.first_line +
                                       len(self.source_code))]
        cxt_pass = Context(cross_table=[], objects=[], attributes=attrs)
        cxt_fail = Context(cross_table=[], objects=[], attributes=attrs)
        if runs is None:
            runs = self.run_tests(inputs)
        for (input_, outcome, coverage) in runs:
            assert outcome in ["PASS", "FAIL"]
            row = map(make_attr, attrs)
            if outcome is "PASS":
                cxt_pass.add_object(row, repr(input_))
            elif outcome is "FAIL":
                cxt_fail.add_object(row, repr(input_))
        return cxt_pass, cxt_fail
    
    def explore_bugs(self, original_cxt_pass, original_cxt_fail):
        '''
        Explore bugs using error_finder.inspect_errors. Failures are treated as
        new objects, cxt_pass as background knowledge. Objects from cxt_fail
        are added and explored all at once; we hope that if there is only one
        bug, it should work.
        '''
        cxt_pass = deepcopy(original_cxt_pass)
        cxt_fail = deepcopy(original_cxt_fail)
        for failed_run_ind in range(len(cxt_fail)):
            failed_run = cxt_fail[failed_run_ind]
            failed_input = cxt_fail.objects[failed_run_ind] 
            cxt_pass.add_object(failed_run, failed_input)
        new_inds = range(len(cxt_pass) - len(cxt_fail), len(cxt_pass))
        result = [minimize_premise(original_cxt_pass, imp)
                  for imp in inspect_errors(cxt_pass, new_inds)]
        return result