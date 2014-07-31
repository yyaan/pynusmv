import unittest

from pynusmv.init import init_nusmv, deinit_nusmv
from pynusmv import glob
from pynusmv.model import *
from pynusmv import node

from tools.dotDump.dump import dumpDot

class TestNode(unittest.TestCase):
    
    def setUp(self):
        init_nusmv()
    
    def tearDown(self):
        deinit_nusmv()
    
    def counters(self):
        class Counter(Module):
            max_ = 2
            run = Identifier("run")
            ARGS = [run]
            c = Var(Range(0, max_))
            INIT = c == 0
            TRANS = [run.implies(c.next() == (c + 1) % (max_ + 1)),
                     (~run).implies(c.next() == c)]

        class main(Module):
            run = IVar(Scalar(("rc1", "rc2")))
            c1 = Var(Counter(run == "rc1"))
            c2 = Var(Counter(run == "rc2"))
        
        return Counter, main
    
    
    def test_access_flat_hierarchy(self):
        glob.load(*self.counters())
        glob.compute_model()
        
        flat = glob.flat_hierarchy()
        
        self.assertIsNotNone(flat.init)
        self.assertIsNotNone(flat.trans)
        self.assertIsNone(flat.invar)
        self.assertIsNone(flat.justice)
        self.assertIsNone(flat.compassion)
    
    def test_change_trans_of_flat(self):
        glob.load(*self.counters())
        glob.flatten_hierarchy()
        flat = glob.flat_hierarchy()
        self.assertIsNotNone(flat)
        
        trans = flat.trans
        
        choose_run = node.Expression.from_string("run = rc1")
        flat.trans = flat.trans & choose_run
        
        glob.compute_model()
        fsm = glob.prop_database().master.bddFsm
        
        self.assertEqual(fsm.count_states(fsm.reachable_states), 3)
        