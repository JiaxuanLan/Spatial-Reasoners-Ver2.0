from itertools import product
from .base import BaseGenerator



class MotionGenerator(BaseGenerator):

    reasoning_type = 'motion'

    movement_jerund = {'running', 'hiking', 'cycling'}
    in_motion_phrase = {'moving', 'in motion'}

    stationary_jerund = {'standing', 'sitting', 'sleeping'}
    not_in_motion_phrase = {'not moving', 'not in motion'}

    neutral_jerund = {'thinking', 'meditating','daydreaming'}


    def gen_two_motion_two_hop_jerund(self):
        """
            P: AGENT is MOTION
            H1: AGENT is MOTION_PHRASE (E)
            H2: AGENT is NON_MOTON_PHRASE (C)
        """
        # A and B in motion
        for motion_1, motion_2 in product(self.movement_jerund, self.movement_jerund):
            for name_1, name_2 in product(self.names,self.names):
                if name_1 != name_2:
                    premise = f"{name_1} is {motion_1} and {name_2} is {motion_2}."

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_1} is {motion_phrase}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_1} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_2} is {motion_phrase}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_2} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

        # A in motion B not in motion
        for motion_3, stationary_4 in product(self.movement_jerund, self.stationary_jerund):
            for name_3, name_4 in product(self.names,self.names):
                if name_3 != name_4:
                    premise = f"{name_3} is {motion_3} and {name_4} is {stationary_4}."

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_3} is {motion_phrase}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_3} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_4} is {motion_phrase}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_4} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )

        # A not in motion B in motion
        for stationary_5, motion_6 in product(self.stationary_jerund, self.movement_jerund):
            for name_5, name_6 in product(self.names,self.names):
                if name_5 != name_6:
                    premise = f"{name_5} is {stationary_5} and {name_6} is {motion_6}."

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_5} is {motion_phrase}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_5} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_6} is {motion_phrase}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_6} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )
            
        # A not in motion B not in motion
        for stationary_7, stationary_8 in product(self.stationary_jerund, self.stationary_jerund):
            for name_7, name_8 in product(self.names,self.names):
                if name_7 != name_8:
                    premise = f"{name_7} is {stationary_7} and {name_8} is {stationary_8}."

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_7} is {motion_phrase}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_7} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_8} is {motion_phrase}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_8} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )

        # A in motion and B neutral
        for motion_9, neutral_10 in product(self.movement_jerund, self.neutral_jerund):
            for name_9, name_10 in product(self.names,self.names):
                if name_9 != name_10:
                    premise = f"{name_9} is {motion_9} and {name_10} is {neutral_10}."

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_9} is {motion_phrase}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_9} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_10} is {motion_phrase}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_10} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )


        # A not in motion and B neutral
        for stationary_11, neutral_12 in product(self.stationary_jerund, self.neutral_jerund):
            for name_11, name_12 in product(self.names,self.names):
                if name_11 != name_12:
                    premise = f"{name_11} is {stationary_11} and {name_12} is {neutral_12}."

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_11} is {motion_phrase}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_11} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_12} is {motion_phrase}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_12} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )

        # A neutral and B in motion
        for neutral_13, motion_14 in product(self.neutral_jerund, self.movement_jerund):
            for name_13, name_14 in product(self.names,self.names):
                if name_13 != name_14:
                    premise = f"{name_13} is {neutral_13} and {name_14} is {motion_14}."

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_13} is {motion_phrase}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_13} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_14} is {motion_phrase}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_14} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

        # A neutral and B not in motion
        for neutral_15, stationary_16 in product(self.neutral_jerund, self.movement_jerund):
            for name_15, name_16 in product(self.names,self.names):
                if name_15 != name_16:
                    premise = f"{name_15} is {neutral_15} and {name_16} is {stationary_16}."

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_15} is {motion_phrase}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_15} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_16} is {motion_phrase}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_16} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )

        # A neutral and B neutral
        for neutral_17, neutral_18 in product(self.neutral_jerund, self.movement_jerund):
            for name_17, name_18 in product(self.names,self.names):
                if name_17 != name_18:
                    premise = f"{name_17} is {neutral_17} and {name_18} is {neutral_18}."

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_17} is {motion_phrase}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_17} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )

                    for motion_phrase in self.in_motion_phrase:
                        hypothesis = f"{name_18} is {motion_phrase}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )

                    for non_motion_phrase in self.not_in_motion_phrase:
                        hypothesis = f"{name_18} is {non_motion_phrase}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )