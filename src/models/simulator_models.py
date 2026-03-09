from pydantic import BaseModel
from typing import List, Dict


class TransitionAction(BaseModel):
    """
    Used in storing transition states.
    This class encodes the write-behavior for the machine.
    It should be stored in a dict where the key is the read behavior with the format:
    'current_state,read_symbol'
    """
    write_symbol: str
    move_direction: str
    next_state: str

class TuringMachine(BaseModel):
    """
    The initial configuration of the Turing Machine.

    transitions should be a list with [state,read_char] as the lookup key

    alphabet should not include the blank symbol.

    blank_symbol should only be included if the user wants the UI to default to a symbol other than "_".
    """
    states: List[str]  # list of state names
    initial_state: str  # the name of the initial state
    accept_states: List[str]  # the names of the accept states
    reject_states: List[str]  # the names of the reject states
    transitions: Dict[str, TransitionAction]  # [key: "state,read_char", value: TransitionAction
    alphabet: List[str]  # all symbols the machine should read other than the blank symbol
    blank_symbol: str = "_"

class Tape(BaseModel):
    """
    fill_symbol is to be used if you want the edges of your input to be filled with symbols other than blanks.
    For example, if you wanted an infinite amount of '0' on the edges of your tape, fill_symbol should be set to '0'.
    """
    tape_contents: List[str]
    start_head_position: int
    fill_symbol: str

