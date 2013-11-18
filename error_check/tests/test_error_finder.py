#from nose.tools import *
from fca import read_txt_with_names

#from bunny_exploration.tab_separated_objs_names import read_txt_objs_names
from error_check.error_finder import *
from fca import Context, Implication
#from suspicion_support import *

class TestErrorFinder:
    @classmethod
    def setup_class(self):
        test_cxt_path = './tests/test_cxt2.txt'
        cxt = read_txt_with_names(test_cxt_path)
        self.cxt = cxt
        self.cxt_correct = Context(cxt[4:], cxt.objects[4:], cxt.attributes)
        
        self.cxt4 = Context(cxt[3:], cxt.objects[3:],
                            cxt.attributes)
        self.cxt3 = Context(cxt[2:3] + cxt[4:], cxt.objects[2:3] + cxt.objects[4:],
                            cxt.attributes)
        self.cxt2 = Context(cxt[1:2] + cxt[4:], cxt.objects[1:2] + cxt.objects[4:],
                            cxt.attributes)
        self.cxt1 = Context(cxt[:1] + cxt[4:], cxt.objects[:1] + cxt.objects[4:],
                            cxt.attributes)
        self.cxt12 = Context(cxt[:2] + cxt[4:], cxt.objects[:2] + cxt.objects[4:],
                            cxt.attributes)
        self.cxt23 = Context(cxt[1:3] + cxt[4:], cxt.objects[1:3] + cxt.objects[4:],
                             cxt.attributes)
        
        self.objs_ints1 = [set(["at1", "at2"])]
        self.objs_ints2 = [set(["at1", "at2"]), set(['at2', 'at3'])]
        self.premise1 = set(['at2', 'at4'])
        self.premise2 = set(['at1'])
        self.conc1 = set(['at3', 'at4', 'at5'])
        self.conc2 = set(['at2', 'at3', 'at4'])
        self.imp1 = Implication(self.premise1, self.conc1)
        self.imp2 = Implication(self.premise2, self.conc2)
        self.imps = [self.imp1, self.imp2]
        
    @classmethod
    def teardown_class(self):
        pass
        
    def test_split_imps(self):
        assert len(split_implications(inspect_direct(self.cxt_correct,
                        [self.cxt1.get_object_intent_by_index(0),]))) == 4
    
    def test_inspect_dg(self):
        for cxt in [self.cxt1, self.cxt2, self.cxt3, self.cxt4]:
            for i in inspect_dg(cxt, (0, )):
                assert not i.is_respected(cxt.get_object_intent_by_index(0))
                assert i.is_respected(cxt.get_object_intent_by_index(1))
        for cxt in [self.cxt12, self.cxt2, self.cxt23]:
            for i in inspect_dg(cxt, (0, 1)):
                assert not i.is_respected(cxt.get_object_intent_by_index(0))
                assert not i.is_respected(cxt.get_object_intent_by_index(1))
                assert i.is_respected(cxt.get_object_intent_by_index(2))
        
    def test_inspect(self):
        for cxt in [self.cxt1, self.cxt2, self.cxt3, self.cxt4]:
            for i in inspect_direct(self.cxt_correct,
                                    [cxt.get_object_intent_by_index(0),]):
                assert not i.is_respected(cxt.get_object_intent_by_index(0))
                # Probably rewrite is_respected for imps with negation
                #assert i.is_respected(cxt.get_object_intent_by_index(1))
                ints = cxt.intents()
                next(ints)
                assert any([(i.premise <= int) for int in ints])
        for cxt in [self.cxt12, self.cxt2, self.cxt23]:
            print cxt
            print
            for i in inspect_direct(self.cxt_correct,
                                    [cxt.get_object_intent_by_index(0), 
                                     cxt.get_object_intent_by_index(1)]):
                print i
            print
            print
            for i in inspect_direct(self.cxt_correct,
                                    [cxt.get_object_intent_by_index(0), 
                                     cxt.get_object_intent_by_index(1)]):
                assert not i.is_respected(cxt.get_object_intent_by_index(0))
                assert not i.is_respected(cxt.get_object_intent_by_index(1))
                #assert i.is_respected(cxt.get_object_intent_by_index(2))
                ints = cxt.intents()
                next(ints)
                next(ints)
                assert any([(i.premise <= int) for int in ints])
                
    def test_make_dual_imps(self):
        premise = set(('attr1', 'attr2'))
        conc1 = set(('not attr3', 'attr4'))
        conc2 = set(('attr5', 'attr6'))
        conc3 = set(('not attr7', 'not attr8'))
        imp1 = Implication(premise, conc1)
        imp2 = Implication(premise, conc2)
        imp3 = Implication(premise, conc3)
        imps = set((imp1, imp2, imp3))
        dual_imps = make_dual_imps(imps)
        assert any([Implication(premise, frozenset(('not attr6', ))) == i
                    for i in dual_imps])
        assert any([Implication(premise, frozenset(('attr8', ))) == i
                    for i in dual_imps])
        assert len(dual_imps) == 6
            
    #@nottest
    def test_results_print(self):
        """
        Function for printing out some results. Usage: 'nosetests -s' and
        delete '@nottest' decorator 
        """
        for cxt in [self.cxt1, self.cxt3, self.cxt2, self.cxt4]:
            print '\n{0} = {1} is deleted\n'.format(cxt.objects[0],
                                                    cxt.get_object_intent_by_index(0))
            for i in inspect_direct(self.cxt_correct,
                                    [cxt.get_object_intent_by_index(0),]):
                print i
            print 'inspect_direct ended\n'
            for i in inspect_dg(cxt, (0,)):
                print i
            print 'inspect_dg ended\n'
        
        for cxt in [self.cxt12, self.cxt23]:
            print '\n{0} and {1} are deleted\n'.format(cxt.objects[0], cxt.objects[1])
            for i in inspect_direct(self.cxt_correct,
                                    [cxt.get_object_intent_by_index(0), 
                                     cxt.get_object_intent_by_index(1)]):
                print i
            print 'inspect_direct ended\n'
            for i in inspect_dg(cxt, (0, 1)):
                print i
            print 'inspect_dg ended\n'