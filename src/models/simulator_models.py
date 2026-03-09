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
    states: List[str]  # list of state names
    initial_state: str
    accept_states: List[str]
    reject_states: List[str]
    transitions: Dict[str, TransitionAction]
    alphabet: List[str]
    blank_symbol: str

class Tape(BaseModel):
    tape_contents: List[str]
    start_head_position: int
    fill_symbol: str

