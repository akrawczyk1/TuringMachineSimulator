from enum import Enum

from src.models.simulator_models import TransitionAction, TuringMachine, Tape

class StepStatus(Enum):
    CONTINUE = "continue"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    OVER_MAX_STEPS = f"over maximum allowable steps"

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

        if self.fill_symbol is None:
            self.fill_symbol = self.blank_symbol

        if not self.check_tape_alphabet():
            raise RuntimeError(
                "The tape alphabet is not a subset of the machine alphabet."
            )

        self.check_head_in_bounds()

    def check_tape_alphabet(self) -> bool:
        tape_alphabet = set(self.tape_contents)
        if self.fill_symbol != self.blank_symbol:
            tape_alphabet.add(self.fill_symbol)

        return tape_alphabet <= set(self.machine_alphabet)

    def craft_lookup_key(self, current_symbol: str) -> str:
        lookup_key = self.current_state + "," + current_symbol
        return lookup_key

    def check_head_in_bounds(self):
        if 0 <= self.head_position < len(self.tape_contents):
            pass
        elif self.head_position < 0:
            self.head_position = 0
            self.tape_contents.insert(0, self.fill_symbol)
        elif self.head_position >= len(self.tape_contents):
            self.tape_contents.append(self.fill_symbol)

    def run(self) -> StepStatus:
        step_count = 0
        while step_count < self.NUM_MAX_STEPS:

            step_status = self.step()
            step_count += 1

            if step_status == StepStatus.CONTINUE:
                continue
            else:
                return step_status

        return StepStatus.OVER_MAX_STEPS
    def step(self) -> StepStatus:
        """
        Returns:
            StepStatus.REJECT if no transition function or other error\n
            StepStatus.ACCEPT if we end in an accept state\n
            StepStatus.CONTINUE if we should keep running\n
        :return:
        """

        # This step exists in case the initial state is an accept state
        if self.current_state in self.accept_states:
            return StepStatus.ACCEPTED

        # Read symbol at current location
        current_symbol = self.tape_contents[self.head_position]

        # Look up the appropriate transition function
        lookup_key = self.craft_lookup_key(current_symbol)
        transition_action = self.transitions.get(lookup_key)
        if transition_action is None:
            return StepStatus.REJECTED

        # Write to tape according to current transition function

        self.tape_contents[self.head_position] = transition_action.write_symbol

        # Move head according to transition function:
        if transition_action.move_direction.upper() == 'R':
            self.head_position += 1
        elif transition_action.move_direction.upper() == 'L':
            self.head_position -= 1
        else:
            raise RuntimeError(f"Head movement must be 'R' or 'L', got {transition_action.move_direction} instead.")

        self.check_head_in_bounds()
        # Update the current state
        self.current_state = transition_action.next_state
        if self.current_state in self.accept_states:
            return StepStatus.ACCEPTED
        else:
            return StepStatus.CONTINUE
