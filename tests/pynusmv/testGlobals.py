import unittest

from pynusmv_lower_interface.nusmv.parser import parser as nsparser
from pynusmv_lower_interface.nusmv.cmd import cmd as nscmd

from pynusmv.init import init_nusmv, deinit_nusmv
from pynusmv import glob
from pynusmv.exception import (NuSMVNoReadModelError,
                               NuSMVCannotFlattenError,
                               NuSMVModelAlreadyFlattenedError,
                               NuSMVNeedFlatModelError,
                               NuSMVNeedFlatHierarchyError,
                               NuSMVModelAlreadyReadError,
                               NuSMVParsingError,
                               NuSMVModelAlreadyEncodedError,
                               NuSMVFlatModelAlreadyBuiltError,
                               NuSMVNeedVariablesEncodedError,
                               NuSMVModelAlreadyBuiltError)
from pynusmv.parser import parse_simple_expression

class TestGlobals(unittest.TestCase):
    
    def setUp(self):
        init_nusmv()
        
    def tearDown(self):
        deinit_nusmv()
        
        
    def test_parsing(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
    
    
    def test_load_from_string(self):
        main = """
        MODULE main
            VAR state : boolean;
            INIT state
            TRANS next(state) = !state
        """
        glob.load(main)
    
    
    def test_load_from_string_syntax_errors(self):
        main = """
        MODULE main
            VAR state : boolean
            INIT state
            TRANS next(state) = !state
        """
        with self.assertRaises(NuSMVParsingError):
            glob.load(main)
    
    
    def test_load_errors(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        with self.assertRaises(NuSMVModelAlreadyReadError):
            glob.load_from_file("tests/pynusmv/models/counters.smv")
            
            
    def test_load_allow_flattening_with_command(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        ret = nscmd.Cmd_SecureCommandExecute("flatten_hierarchy")
        self.assertEqual(ret, 0)
        
    
    def test_no_flattening_hierarchy(self):
        with self.assertRaises(NuSMVNoReadModelError):
            glob.flatten_hierarchy()
        
    
    def test_flattening_hierarchy_already_done(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        glob.flatten_hierarchy(keep_single_enum=True)
        with self.assertRaises(NuSMVModelAlreadyFlattenedError):
            glob.flatten_hierarchy()
            
            
    def test_load_and_flat_allow_encoding_with_command(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        glob.flatten_hierarchy()
        ret = nscmd.Cmd_SecureCommandExecute("encode_variables")
        
        
    def test_no_encoding(self):
        with self.assertRaises(NuSMVNeedFlatHierarchyError):
            glob.encode_variables()
        
    def test_already_encoded(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        glob.flatten_hierarchy()
        glob.encode_variables()
        with self.assertRaises(NuSMVModelAlreadyEncodedError):
            glob.encode_variables()
    
    def test_no_bdd_encoding(self):
        with self.assertRaises(NuSMVNeedFlatHierarchyError):
            glob.bdd_encoding()
    
    def test_no_encoding_after_parsing(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        with self.assertRaises(NuSMVNeedFlatHierarchyError):
            glob.encode_variables()
    
    def test_no_bdd_encoding_after_parsing(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        with self.assertRaises(NuSMVNeedFlatHierarchyError):
            glob.bdd_encoding()
    
    
    def test_bdd_encoding(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        glob.flatten_hierarchy()
        be = glob.bdd_encoding()
        self.assertIsNotNone(be)
        
        
    def test_flat_command_allow_prop_db(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        ret = nscmd.Cmd_SecureCommandExecute("flatten_hierarchy")
        self.assertEqual(ret, 0)
        pd = glob.prop_database()
        self.assertIsNotNone(pd)
        
        
    def test_no_prop_database(self):
        with self.assertRaises(NuSMVNeedFlatHierarchyError):
            glob.prop_database()
        with self.assertRaises(NuSMVNeedFlatHierarchyError):
            glob.load_from_file("tests/pynusmv/models/counters.smv")
            glob.prop_database()
        
        
    def test_prop_database(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        glob.flatten_hierarchy()
        pd = glob.prop_database()
        self.assertIsNotNone(pd)
        
        
    def test_no_flat_model(self):
        with self.assertRaises(NuSMVNeedFlatHierarchyError):
            glob.build_flat_model()
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        glob.flatten_hierarchy()
        glob.build_flat_model()
            
    
    def test_no_flat_model_after_parsing(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        with self.assertRaises(NuSMVNeedFlatHierarchyError):
            glob.build_flat_model()
    

    def test_flat_model(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        glob.flatten_hierarchy()
        glob.build_flat_model()
        with self.assertRaises(NuSMVFlatModelAlreadyBuiltError):
            glob.build_flat_model()
        

    def test_no_model(self):
        with self.assertRaises(NuSMVNeedFlatModelError):
            glob.build_model()
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        with self.assertRaises(NuSMVNeedFlatModelError):
            glob.build_model()
        glob.flatten_hierarchy()
        with self.assertRaises(NuSMVNeedFlatModelError):
            glob.build_model()
        glob.build_flat_model()
        with self.assertRaises(NuSMVNeedVariablesEncodedError):
            glob.build_model()
        glob.encode_variables()
        glob.build_model()
        with self.assertRaises(NuSMVModelAlreadyBuiltError):
            glob.build_model()
    

    def test_model(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        glob.flatten_hierarchy()
        glob.encode_variables()
        glob.build_flat_model()
        glob.build_model()
    
    
    def test_get_symb_table(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        symb_table = glob.symb_table()
    
    
    def test_get_flat_hierarchy(self):
        with self.assertRaises(NuSMVNeedFlatHierarchyError):
            flat = glob.flat_hierarchy()
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        glob.compute_model()
        flat = glob.flat_hierarchy()
        
        
    def test_compute_model(self):
        glob.load_from_file("tests/pynusmv/models/counters.smv")
        glob.compute_model()
        
    
    def test_no_compute_model(self):
        with self.assertRaises(NuSMVNoReadModelError):
            glob.compute_model()
            
            
    def test_file_error(self):
        with self.assertRaises(IOError):
            glob.load_from_file(
                            "tests/pynusmv/models/no-model.smv")
                            
                            
    def test_semantics_error(self):
        glob.load_from_file(
                            "tests/pynusmv/models/counter-semantics-error.smv")
        with self.assertRaises(NuSMVCannotFlattenError):
            glob.flatten_hierarchy()
    
    def test_variables_ordering(self):
        glob.load_from_file("tests/pynusmv/models/constraints.smv")
        glob.flatten_hierarchy()
        glob.encode_variables(variables_ordering=
                              "tests/pynusmv/models/constraints.ord")
        glob.compute_model()
        fsm = glob.prop_database().master.bddFsm
        
        with open("tests/pynusmv/models/constraints.ord", "r") as f:
            order = f.read().split("\n")
            self.assertListEqual(order,
                                 list(fsm.bddEnc.get_variables_ordering()))
    
    def test_variables_ordering_compute(self):
        glob.load_from_file("tests/pynusmv/models/constraints.smv")
        glob.compute_model(variables_ordering=
                           "tests/pynusmv/models/constraints.ord")
        fsm = glob.prop_database().master.bddFsm
        
        with open("tests/pynusmv/models/constraints.ord", "r") as f:
            order = f.read().split("\n")
            self.assertListEqual(order,
                                 list(fsm.bddEnc.get_variables_ordering()))