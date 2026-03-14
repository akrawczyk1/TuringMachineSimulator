from enum import Enum

from src.models.simulator_models import TransitionAction, TuringMachine, Tape

class StepStatus(Enum):
    CONTINUE = "continue"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class Simulator:
    def __init__(self, machine: TuringMachine, tape: Tape):
        self.NUM_MAX_STEPS = 1000

        self.states = machine.states
        self.current_state = machine.initial_state
        self.accept_states = machine.accept_states
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

    def check_tape_alphabet(self) -> bool:
        tape_alphabet = set(self.tape_contents)
        tape_alphabet.add(self.fill_symbol)

        return tape_alphabet <= set(self.machine_alphabet)

    def craft_lookup_key(self, current_symbol: str) -> str:
        lookup_key = self.current_state + "," + current_symbol
        return lookup_key

    def step(self) -> StepStatus:
        """
        Returns:
            StepStatus.REJECT if no transition function or other error
            StepStatus.ACCEPT if we end in an accept state
            StepStatus.CONTINUE if we should keep running
        :return:
        """

        if self.current_state in self.accept_states:
            return StepStatus.ACCEPTED

        # Read symbol at current location
        current_symbol = self.tape_contents[self.head_position]

        # Look up the appropriate transition function
        lookup_key = self.craft_lookup_key(current_symbol)
        try:
            transition_action = self.transitions.get(lookup_key)
        except KeyError:
            return StepStatus.REJECTED

        # Write to tape according to current transition function
        try:
            self.tape_contents[self.head_position]
        except IndexError:
            if len(self.tape_contents) <= self.head_position:
                self.tape_contents.append(self.blank_symbol)
            else:
                self.tape_contents.insert(0, self.blank_symbol)
                self.head_position = 0
        finally:
            self.tape_contents[self.head_position] = transition_action.write_symbol

        # Move head according to transition function:
        if transition_action.move_direction.upper() == 'R':
            self.head_position += 1
        elif transition_action.move_direction.upper() == 'L':
            self.head_position -= 1
        else:
            raise RuntimeError(f"Head movement must be 'R' or 'L', got {transition_action.move_direction} instead.")

        # Update the current state
        self.current_state = transition_action.next_state
        return StepStatus.CONTINUE
