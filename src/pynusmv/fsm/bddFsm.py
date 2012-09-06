from ..nusmv.fsm.bdd import bdd as bddFsm
from ..nusmv.enc.bdd import bdd as bddEnc
from ..nusmv.cmd import cmd as nscmd
from ..nusmv.trans.bdd import bdd as nsbddtrans

from ..enc.enc import BddEnc
from ..dd.bdd import BDD
from ..dd.state import State
from ..dd.inputs import Inputs
from ..utils.pointerwrapper import PointerWrapper
from ..trans.trans import BddTrans

class BddFsm(PointerWrapper):
    """
    Python class for BddFsm structure.
    
    The BddFsm class contains a pointer to a BddFsm in NuSMV and provides a set
    of operations on this FSM.
    
    BddFsm do not have to be freed.
    """
    
        
    @property
    def bddEnc(self):
        """The BDD encoding of this FSM."""
        return BddEnc(bddFsm.BddFsm_get_bdd_encoding(self._ptr))
        
    
    @property
    def init(self):
        """The BDD of initial states of this FSM."""
        return BDD(bddFsm.BddFsm_get_init(self._ptr), self.bddEnc.DDmanager,
                   freeit = True)
                   
                   
    @property
    def trans(self):
        """The transition relation of this FSM."""
        # Do not free the trans, this FSM is the owner of it
        return BddTrans(bddFsm.BddFsm_get_trans(self._ptr),
                        self.bddEnc,
                        self.bddEnc.DDmanager,
                        freeit = False)
        
    @trans.setter
    def trans(self, new_trans):
        """Set this FSM transition to new_trans."""
        # Copy the transition such that this FSM is the owner
        new_trans_ptr = nsbddtrans.BddTrans_copy(new_trans._ptr)
        # Get old trans
        old_trans_ptr = bddFsm.BddFsm_get_trans(self._ptr)
        # Set the new trans
        self._ptr.trans = new_trans_ptr
        # Free old trans
        nsbddtrans.BddTrans_free(old_trans_ptr)
        
                   
    @property
    def state_constraints(self):
        """The BDD of states satisfying the invariants of the FSM."""
        return BDD(bddFsm.BddFsm_get_state_constraints(self._ptr),
                   self.bddEnc.DDmanager, freeit = True)
                   
                   
    @property
    def inputs_constraints(self):
        """The BDD of inputs satisfying the invariants of the FSM."""
        return BDD(bddFsm.BddFsm_get_input_constraints(self._ptr),
                   self.bddEnc.DDmanager, freeit = True)
                   
                   
    def pre(self, states, inputs = None):
        """
        Return the pre-image of states in this FSM.
        
        If inputs is not None, it is used as constraints to get pre-states
        that are reachable through these inputs.
        """
        if inputs is None:
            return BDD(bddFsm.BddFsm_get_backward_image(self._ptr, states._ptr),
                       self.bddEnc.DDmanager, freeit = True)
        else:
            return BDD(bddFsm.BddFsm_get_constrained_backward_image(
                            self._ptr, states._ptr, inputs._ptr),
                       self.bddEnc.DDmanager, freeit = True)
        
        
    def post(self, states, inputs = None):
        """
        Return the post-image of states in this FSM.
        
        If inputs is not None, it is used as constraints to get post-states
        that are reachable through these inputs.
        """
        if inputs is None:
            return BDD(bddFsm.BddFsm_get_forward_image(self._ptr, states._ptr),
                       self.bddEnc.DDmanager, freeit = True)
        else:
            return BDD(bddFsm.BddFsm_get_constrained_forward_image(
                            self._ptr, states._ptr, inputs._ptr),
                       self.bddEnc.DDmanager, freeit = True)
        
        
    def pick_one_state(self, bdd):
        """Return a BDD representing a state of bdd."""
        state = bddEnc.BddEnc_pick_one_state(self.bddEnc._ptr, bdd._ptr)
        return State(state, self, freeit = True)

    
    def pick_one_inputs(self, bdd):
        """Return a BDD representing a possible inputs of bdd."""
        inputs = bddEnc.BddEnc_pick_one_input(self.bddEnc._ptr, bdd._ptr)
        return Inputs(inputs, self, freeit = True)
        
    
    def get_inputs_between_states(self, current, next):
        """
        Return the BDD representing the possible inputs
        between current and next.
        """
        inputs = bddFsm.BddFsm_states_to_states_get_inputs(self._ptr,
                                                           current._ptr,
                                                           next._ptr)
        return Inputs(inputs, self, freeit = True)
        
        
    # ==========================================================================
    # ===== Static methods =====================================================
    # ==========================================================================
    
    def from_filename(filepath):
        """
        Return the FSM corresponding to the model in filepath.
        """
        from ..glob import glob
        glob.load_from_file(filepath)
        glob.compute_model()
        propDb = glob.prop_database()
        return propDb.master.bddFsm
        # TODO Remove this and use glob module instead