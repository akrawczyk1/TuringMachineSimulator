from src.models.simulator_models import *

class Simulator:
    def __init__(self, machine: TuringMachine, tape: Tape):
        self.states = machine.states
        self.initial_state = machine.initial_state
        self.accept_states = machine.accept_states
        self.reject_states = machine.reject_states
        self.transitions = machine.transitions
        self.alphabet = machine.alphabet
        self.blank_symbol = machine.blank_symbol

        self.tape_contents = tape.tape_contents
        self.head_position = tape.start_head_position
        self.fill_symbol = tape.fill_symbol




