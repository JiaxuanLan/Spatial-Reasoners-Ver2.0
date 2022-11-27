from itertools import product
from .base import BaseGenerator


class OrientationGenerator(BaseGenerator):

    reasoning_type = 'orientation'

    objects = {'plate', 'apple', 'phone', 'computer'}
    locations = {'restaurant', 'gym', 'library', 'bar'}
    cardinals = {'north', 'south', 'east', 'west'}
    above_phrases = {'above', 'on top of'}
    below_phrases = {'below', 'underneath'}
    front_phrases = {'front', 'in front of'}
    back_phrases = {'behind', 'in back of'}
    left_phrases = {'left of', 'on the left side of'}#'to the left of', 'on the left side of'}
    right_phrases = {'right of', 'on the right side of'}#'to the right of', 'on the right side of'}
    # non_above_phrases = below_phrases.union(left_phrases).union(right_phrases).union(front_phrases).union(back_phrases)
    # non_below_phrases = above_phrases.union(left_phrases).union(right_phrases).union(front_phrases).union(back_phrases)
    # non_front_phrases = front_phrases.union(left_phrases).union(right_phrases).union(above_phrases).union(below_phrases)
    # non_back_phrases = back_phrases.union(left_phrases).union(right_phrases).union(above_phrases).union(below_phrases)
    # non_left_phrases = right_phrases.union(above_phrases).union(below_phrases).union(front_phrases).union(back_phrases)
    # non_right_phrases = left_phrases.union(above_phrases).union(below_phrases).union(front_phrases).union(back_phrases)
    
    non_above_phrases = below_phrases
    non_below_phrases = above_phrases
    non_front_phrases = front_phrases
    non_back_phrases = back_phrases
    non_left_phrases = right_phrases
    non_right_phrases = left_phrases

    invalid_direction = ['eastwest', 'westeast', 'southnorth', 'northsouth']
    wrong_direction = ['eastnorth', 'eastsouth', 'westnorth', 'westsouth']

    all_cardinals = ['north', 'south', 'east', 'west', 'northwest', 'northeast', 'southwest', 'southeast']


    def gen_cardinals_one_hop(self):
        """
        Generates positive textual entailment pairs relating to orientation of the form:
            P: The LOC_1 is CARDINAL_DIR_1 of the LOC_2 and LOC_2 is CARDINAL_DIR_2 of the LOC_3.
            H: The LOC_3 is CARD of the LOC_1.

        For example:
            P: The gym is north of the library and the library is north of the restaurant.
            H: The restaurant is south of gym.
        """
        for loc_1, cardinal_1, loc_2, cardinal_2, loc_3 in product(self.locations, self.cardinals, self.locations, self.cardinals, self.locations):
            if loc_1 != loc_2 and loc_2 != loc_3 and loc_1 != loc_3: # location shouldn't be same as others
                # Case when cardinal are the same, eg north and north
                if cardinal_1 == cardinal_2:
                    # Generate premise for the case
                    premise = f"The {loc_1} is {cardinal_1} of the {loc_2} and the {loc_2} is {cardinal_2} of the {loc_3}"

                    # Generate entailment cases
                    hypothesis_1 = f"The {loc_1} is {cardinal_1} of the {loc_3}."
                    hypothesis_2 = f"The {loc_3} is {self.opposite_cardinal(cardinal_1)} of the {loc_1}."

                    yield (premise, hypothesis_1, self.ENTAILMENT, 0)
                    yield (premise, hypothesis_2, self.ENTAILMENT, 0)

                    # Generate contradiction casees
                    for cardinal_3,  cardinal_4 in product(self.non_opposite_cardinals(self.opposite_cardinal(cardinal_1)), self.non_opposite_cardinals(self.opposite_cardinal(cardinal_2))):
                        if cardinal_3 == cardinal_4:
                            yield (premise, f"The {loc_1} is {cardinal_3} of the {loc_3}.", self.CONTRADICTION, 1)
                            yield (premise, f"The {loc_3} is {self.opposite_cardinal(cardinal_3)} of the {loc_1}.", self.CONTRADICTION, 1)
                        else:
                            # Eliminate cases such as eastwest
                            if cardinal_3 + cardinal_4 in self.invalid_direction:
                                continue
                            # Switch cardinal of cases like eastsouth
                            elif cardinal_3 + cardinal_4 in self.wrong_direction:
                                yield (premise, f"The {loc_1} is {cardinal_4}" + f"{cardinal_3} of the {loc_3}.", self.CONTRADICTION, 1)
                                yield (premise, f"The {loc_3} is {self.opposite_cardinal(cardinal_4)}" + f"{self.opposite_cardinal(cardinal_3)} of the {loc_1}.", self.CONTRADICTION, 1)
                # Case when cardinal are different, eg north and east, and are not opposite direction, eg north and south, which can cause conflict.  
                if cardinal_1 != cardinal_2 and cardinal_1 != self.opposite_cardinal(cardinal_2):
                    # Initialize lists that saves the correct position
                    loc_1_to_loc_3 = []
                    loc_3_to_loc_1 = []
                    # Generate premise for the case
                    premise = f"The {loc_1} is {cardinal_1} of the {loc_2} and the {loc_2} is {cardinal_2} of the {loc_3}"
                    
                    # Generate entailment cases
                    hypothesis_3 = f"The {loc_1} is {cardinal_1} of the {loc_3}."
                    hypothesis_4 = f"The {loc_3} is {self.opposite_cardinal(cardinal_2)} of the {loc_1}."

                    # Save the correct position in list
                    loc_1_to_loc_3.append(cardinal_1)
                    loc_3_to_loc_1.append(self.opposite_cardinal(cardinal_2))

                    hypothesis_6 = f"The {loc_3} is {self.opposite_cardinal(cardinal_1)} of the {loc_1}."
                    hypothesis_7 = f"The {loc_1} is {cardinal_2} of the {loc_3}."

                    loc_1_to_loc_3.append(self.opposite_cardinal(cardinal_1))
                    loc_3_to_loc_1.append(cardinal_2)

                    # case when i.e. The gym is north of the library and the library is east of the restaurant.
                    # the gym is north of restaurant is neutral

                    # yield (premise, hypothesis_3, self.NEUTRAL, 0)
                    # yield (premise, hypothesis_4, self.NEUTRAL, 0)

                    # yield (premise, hypothesis_6, self.NEUTRAL, 0)
                    # yield (premise, hypothesis_7, self.NEUTRAL, 0)

                    # case when i.e. The gym is north of the library and the library is east of the restaurant.
                    # the gym is north of restaurant is entailment

                    yield (premise, hypothesis_3, self.ENTAILMENT, 0)
                    yield (premise, hypothesis_4, self.ENTAILMENT, 0)

                    yield (premise, hypothesis_6, self.ENTAILMENT, 0)
                    yield (premise, hypothesis_7, self.ENTAILMENT, 0)

                    # Switch cardinal of cases like eastsouth
                    if cardinal_1 + cardinal_2 in self.wrong_direction:
                        hypothesis_5 = f"The {loc_1} is {cardinal_2}" + f"{cardinal_1} of the {loc_3}."
                        hypothesis_8 = f"The {loc_3} is {self.opposite_cardinal(cardinal_2)}" + f"{self.opposite_cardinal(cardinal_1)} of the {loc_1}."
                        
                        loc_1_to_loc_3.append(cardinal_2 + cardinal_1)
                        loc_3_to_loc_1.append(cardinal_2)
                    else:
                        hypothesis_5 = f"The {loc_1} is {cardinal_1}" + f"{cardinal_2} of the {loc_3}."
                        hypothesis_8 = f"The {loc_3} is {self.opposite_cardinal(cardinal_1)}" + f"{self.opposite_cardinal(cardinal_2)} of the {loc_1}."
                        
                        loc_1_to_loc_3.append(self.opposite_cardinal(cardinal_1))
                        loc_3_to_loc_1.append(cardinal_2)
                    
                    yield (premise, hypothesis_5, self.ENTAILMENT, 0)
                    yield (premise, hypothesis_8, self.ENTAILMENT, 0)

                    # all the wrong directions
                    wrong_1 = list(set(self.all_cardinals) - set(loc_1_to_loc_3))
                    wrong_2 = list(set(self.all_cardinals) - set(loc_3_to_loc_1))

                    # Generate contradiction cases
                    for i in range(len(wrong_1)):
                        yield (premise, f"The {loc_1} is {wrong_1[i]} of the {loc_3}.", self.CONTRADICTION, 1)
                        yield (premise, f"The {loc_3} is {wrong_2[i]} of the {loc_1}.", self.CONTRADICTION, 1)

                    # Generate contradiction cases
                    # for cardinal_3,  cardinal_4 in product(self.non_opposite_cardinals(self.opposite_cardinal(cardinal_1)), self.non_opposite_cardinals(self.opposite_cardinal(cardinal_2))):
                    #     if cardinal_3 == cardinal_4:
                    #         yield (premise, f"The {loc_1} is {cardinal_3} of the {loc_3}.", self.CONTRADICTION, 1)
                    #         yield (premise, f"The {loc_3} is {self.opposite_cardinal(cardinal_3)} of the {loc_1}.", self.CONTRADICTION, 1)
                    #     else:
                    #         if cardinal_3 + cardinal_4 in self.invalid_direction:
                    #             yield(1, 1, 1, 1)
                    #         elif cardinal_3 + cardinal_4 in self.wrong_direction:
                    #             yield (premise, f"1. The {loc_1} is {self.opposite_cardinal(cardinal_4)}" + f"{self.opposite_cardinal(cardinal_3)} of the {loc_3}.", self.CONTRADICTION, 1)
                    #             yield (premise, f"2. The {loc_3} is {self.opposite_cardinal(cardinal_4)}" + f"{self.opposite_cardinal(cardinal_3)} of the {loc_1}.", self.CONTRADICTION, 1)

                    
    def gen_left_right_one_hop(self):
        for dir_rels in [self.left_phrases, self.right_phrases]:
            for obj_1, dir_1, obj_2, dir_2, obj_3 in product(self.objects, dir_rels, self.objects, dir_rels, self.objects):
                if obj_1 != obj_2 and obj_2 != obj_3 and obj_1 != obj_3:
                    premise = f"The {obj_1} is {dir_1} the {obj_2} and {obj_2} is {dir_2} the {obj_3}."
                    for rev_dir_1, rev_dir_2 in product(self.opposite_directions(dir_1), self.opposite_directions(dir_2)):
                        if rev_dir_1 != rev_dir_2:
                            yield (premise, f"The {obj_1} is {rev_dir_1} the {obj_3}.", self.CONTRADICTION, 1)
                            yield (premise, f"The {obj_3} is {rev_dir_2} the {obj_1}.", self.ENTAILMENT, 0)
                    
                    for non_rev_dir_1, non_rev_dir_2 in product(self.non_opposite_directions(dir_1), self.non_opposite_directions(dir_2)):
                        yield (premise, f"The {obj_1} is {non_rev_dir_1} the {obj_3}.", self.ENTAILMENT, 0)
                        yield (premise, f"The {obj_3} is {non_rev_dir_2} the {obj_1}.", self.CONTRADICTION, 1)

    


    def gen_above_below_one_hop(self):
        for dir_rels in [self.above_phrases, self.below_phrases]:
            for obj_1, dir_1, obj_2, dir_2, obj_3 in product(self.objects, dir_rels, self.objects, dir_rels, self.objects):
                if obj_1 != obj_2 and obj_2 != obj_3 and obj_1 != obj_3:
                    premise = f"The {obj_1} is {dir_1} the {obj_2} and {obj_2} is {dir_2} the {obj_3}."
                    for rev_dir_1, rev_dir_2 in product(self.opposite_directions(dir_1), self.opposite_directions(dir_2)):
                        yield (premise, f"The {obj_1} is {rev_dir_1} the {obj_3}.", self.CONTRADICTION, 1)
                        yield (premise, f"The {obj_3} is {rev_dir_2} the {obj_1}.", self.ENTAILMENT, 0)
                    
                    for non_rev_dir_1, non_rev_dir_2 in product(self.non_opposite_directions(dir_1), self.non_opposite_directions(dir_2)):
                        yield (premise, f"The {obj_1} is {non_rev_dir_1} the {obj_3}.", self.ENTAILMENT, 0)
                        yield (premise, f"The {obj_3} is {non_rev_dir_2} the {obj_1}.", self.CONTRADICTION, 1)
 

    def gen_front_back_one_hop(self):
        for dir_rels in [self.front_phrases, self.back_phrases]:
            for obj_1, dir_1, obj_2, dir_2, obj_3 in product(self.objects, dir_rels, self.objects, dir_rels, self.objects):
                if obj_1 != obj_2 and obj_2 != obj_3 and obj_1 != obj_3:
                    premise = f"The {obj_1} is {dir_1} the {obj_2} and {obj_2} is {dir_2} the {obj_3}."
                    for rev_dir_1, rev_dir_2 in product(self.opposite_directions(dir_1), self.opposite_directions(dir_2)):
                        yield (premise, f"The {obj_1} is {rev_dir_1} the {obj_3}.", self.CONTRADICTION, 1)
                        yield (premise, f"The {obj_3} is {rev_dir_2} the {obj_1}.", self.ENTAILMENT, 0)
                    
                    for non_rev_dir_1, non_rev_dir_2 in product(self.non_opposite_directions(dir_1), self.non_opposite_directions(dir_2)):
                        yield (premise, f"The {obj_1} is {non_rev_dir_1} the {obj_3}.", self.ENTAILMENT, 0)
                        yield (premise, f"The {obj_3} is {non_rev_dir_2} the {obj_1}.", self.CONTRADICTION, 1)
 




    # def gen_left_right_one_hop(self):
    #     for dir_rels in [self.left_phrases, self.right_phrases]:
    #         for obj_1, obj_2, dir in product(self.objects, self.objects, dir_rels):
    #             if obj_1 != obj_2:
    #                 premise = f"The {obj_1} is {dir} the {obj_2}."

    #                 for rev_dir in self.opposite_directions(dir):
    #                     yield ( premise, f"The {obj_2} is {rev_dir} the {obj_1}.", self.ENTAILMENT, 0 )
                    
    #                 for non_rev_dir in self.non_opposite_directions(dir):
    #                     yield ( premise, f"The {obj_2} is {non_rev_dir} the {obj_1}.", self.CONTRADICTION, 1 )

    # def gen_above_below_one_hop(self):
    #     for dir_rels in [self.above_phrases, self.below_phrases]:
    #         for obj_1, obj_2, dir in product(self.objects, self.objects, dir_rels):
    #             if obj_1 != obj_2:
    #                 premise = f"The {obj_1} is {dir} the {obj_2}."

    #                 for rev_dir in self.opposite_directions(dir):
    #                     yield ( premise, f"The {obj_2} is {rev_dir} the {obj_1}.", self.ENTAILMENT, 0 )
                    
    #                 for non_rev_dir in self.non_opposite_directions(dir):
    #                     yield ( premise, f"The {obj_2} is {non_rev_dir} the {obj_1}.", self.CONTRADICTION, 1 )

    # def gen_front_back_one_hop(self):
    #     for dir_rels in [self.front_phrases, self.back_phrases]:
    #         for obj_1, obj_2, dir in product(self.objects, self.objects, dir_rels):
    #             if obj_1 != obj_2:
    #                 premise = f"The {obj_1} is {dir} the {obj_2}."

    #                 for rev_dir in self.opposite_directions(dir):
    #                     yield ( premise, f"The {obj_2} is {rev_dir} the {obj_1}.", self.ENTAILMENT, 0 )
                    
    #                 for non_rev_dir in self.non_opposite_directions(dir):
    #                     yield ( premise, f"The {obj_2} is {non_rev_dir} the {obj_1}.", self.CONTRADICTION, 1 )
    

    def opposite_directions(self, dir):
        if dir in self.above_phrases:
            return self.below_phrases
        elif dir in self.below_phrases:
            return self.above_phrases
        elif dir in self.left_phrases:
            return self.right_phrases
        elif dir in self.right_phrases:
            return self.left_phrases
        elif dir in self.front_phrases:
            return self.back_phrases
        elif dir in self.back_phrases:
            return self.front_phrases
        else:
            return set()
    
    def non_opposite_directions(self, dir):
        if dir in self.above_phrases:
            return self.non_below_phrases
        elif dir in self.below_phrases:
            return self.non_above_phrases
        elif dir in self.left_phrases:
            return self.non_right_phrases
        elif dir in self.right_phrases:
            return self.non_left_phrases
        elif dir in self.front_phrases:
            return self.non_back_phrases
        elif dir in self.back_phrases:
            return self.non_front_phrases
        else:
            return set()

    def opposite_cardinal(self, dir):
        if dir == 'north': return 'south'
        elif dir == 'south': return 'north'
        elif dir == 'east': return 'west'
        elif dir == 'west': return 'east'
        elif dir == 'northeast': return 'southwest'
        elif dir == 'southeast': return 'northwest'
        elif dir == 'northwest': return 'southeast'
        elif dir == 'southwest': return 'northeast'

    def non_opposite_cardinals(self, cardinal):
        opposite_cardinal = self.opposite_cardinal(cardinal)
        return self.cardinals.difference({ opposite_cardinal })