from src.models.simulator_models import TransitionAction, TuringMachine, Tape

class Simulator:
    def __init__(self, machine: TuringMachine, tape: Tape):
        self.NUM_MAX_STEPS = 1000

        self.states = machine.states
        self.current_state = machine.initial_state
        self.accept_states = machine.accept_states
        self.reject_states = machine.reject_states
        self.transitions = machine.transitions
        self.machine_alphabet = machine.alphabet
        self.blank_symbol = machine.blank_symbol

        self.tape_contents = tape.tape_contents
        self.head_position = tape.start_head_position
        self.fill_symbol = tape.fill_symbol

        self.in_accept_state = False
        self.in_reject_state = False

        if self.fill_symbol is None:
            self.fill_symbol = self.blank_symbol

        if not self.check_tape_alphabet():
            raise RuntimeError(
                "The tape alphabet is not a subset of the machine alphabet."
            )

        self.set_accept_reject_state()

    def check_tape_alphabet(self) -> bool:
        tape_alphabet = set(self.tape_contents)
        tape_alphabet.add(self.fill_symbol)

        return tape_alphabet <= set(self.machine_alphabet)

    def craft_lookup_key(self, current_symbol: str) -> str:
        lookup_key = self.current_state + "," + current_symbol
        return lookup_key

    def set_accept_reject_state(self):
        self.in_accept_state = self.current_state in self.accept_states
        self.in_reject_state = self.current_state in self.reject_states

    def step(self):
        # Read symbol at current location
        current_symbol = self.tape_contents[self.head_position]

        # Look up the appropriate transition function
        lookup_key = self.craft_lookup_key(current_symbol)
        transition_action = self.transitions.get(lookup_key)

        # Write to tape according to current transition function
        self.tape_contents[self.head_position] = transition_action.write_symbol

        # Move head according to transition function:
        if transition_action.move_direction.upper() == 'R':
            self.head_position += 1
        elif transition_action.move_direction.upper() == 'L':
            self.head_position -= 1
        else:
            pass

        # Update the current state
        self.current_state = transition_action.next_state
        self.set_accept_reject_state()





