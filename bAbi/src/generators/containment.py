from itertools import product
from math import hypot
from .base import BaseGenerator
from dataclasses import dataclass
from typing import List


class ContainmentGenerator(BaseGenerator):

    reasoning_type = "containment"

    agents = {'a student', 'the child'}.union(BaseGenerator.names)

    in_rels = {'in', 'inside'}#, 'contained by'}
    # contains_phrases = {'contains'}#, 'is holding'}
    out_rels = {'out of','outside'}#, 'not contained by'}

    fits_in_phrases = {'can fit in', 'can contain in'}
    cannot_fit_in_phrases = {'cannot fit in', 'cannot contain in'}#, 'can\'t fit in'}
    # can_contain_phrases = {'can fit', 'fits'}
    # cannot_contain_phrases = {'cannot contain'}#, 'cannot hold'}

    sm_objects = {'eraser', 'pen', 'ruler'}
    sm_containers = {'pencil case', 'small box'}

    med_objects = {'oven', 'computer', 'pillow'}
    med_containers = {'cabinet', 'suitcase', 'box'}

    lg_objects = {'person', 'refrigirator', 'bookshelf'}
    lg_containers = {'apartment', 'garage', 'warehouse'}

    plural_objects = {'the oranges', 'some baseballs'}
    containers = {'the basket', 'the trolly', 'the car'}

    place_into_verb = {'put', 'moved', 'transported'}

    
    def gen_two_hop_is_in(self):

        for smaller_objs, smaller_conts, larger_conts \
                in [(self.sm_objects, self.sm_containers, self.med_containers),
                    (self.med_objects, self.med_containers, self.lg_containers),
                    (self.sm_objects, self.sm_containers, self.lg_containers),
                    (self.sm_objects, self.med_containers, self.lg_containers)]:

            for sm_obj, sm_cont, med_cont \
                    in product(smaller_objs, smaller_conts, larger_conts):
                
                for in_rel_1, in_rel_2 \
                        in product(self.in_rels, self.in_rels):
                
                    # 0. The X_obj is IN the Y_cont. The Y_cont is IN the Z_cont.
                    premise = f"The {sm_obj} is {in_rel_1} the {sm_cont}. The {sm_cont} is {in_rel_2} the {med_cont}."

                    for in_rel_3 in self.in_rels:
                        # 1. The X_obj is in the Z_cont. True
                        hypothesis = f"The {sm_obj} is {in_rel_3} the {med_cont}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )
                    
                    # Have logic error
                    # for in_rel_4 in self.in_rels:
                    #     # 1. The Z_cont is in the X_obj. False
                    #     hypothesis = f"The {med_cont} is {in_rel_4} the {sm_obj}."
                    #     yield ( premise, hypothesis, self.CONTRADICTION, 1 )
                    
                    for out_rel_1 in self.out_rels:
                        # 1. The Z_cont is in the X_obj. False
                        hypothesis = f"The {sm_obj} is {out_rel_1} the {med_cont}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )
                
                    # Have logic error
                    # for out_rel_2 in self.out_rels:
                    #     # 1. The Z_cont is in the X_obj. False
                    #     hypothesis = f"The {med_cont} is {out_rel_2} the {sm_obj}."
                    #     yield ( premise, hypothesis, self.ENTAILMENT, 0 )
                    
                    # for contains_phrase in self.contains_phrases:
                    #     # 2. The Z_cont CONTAINS the X_obj. True
                    #     hypothesis = f"The {med_cont} {contains_phrase} the {sm_obj}."
                    #     yield ( premise, hypothesis, self.ENTAILMENT, 0 )

                    # for fits_in_phrase in self.fits_in_phrases:
                    #     # 3. The X_obj CAN_FIT_IN the Z_cont. True
                    #     hypothesis = f"The {sm_obj} {fits_in_phrase} the {med_cont}."
                    #     yield ( premise, hypothesis, self.ENTAILMENT, 0 )

                    # for cannot_fits_in_phrase in self.cannot_fit_in_phrases:
                    #     # 4. The X_obj CANNOT_FIT_IN the Z_cont. False
                    #     hypothesis = f"The {sm_obj} {cannot_fits_in_phrase} the {med_cont}."
                    #     yield ( premise, hypothesis, self.CONTRADICTION, 1 )
                    
                    # for cannot_contains_phrase in self.can_contain_phrases:
                    #     # 5. The Z_cont CANNOT_CONTAIN_IN the X_obj. False
                    #     hypothesis = f"The {med_cont} {cannot_contains_phrase} the {sm_obj}."
                    #     yield ( premise, hypothesis, self.CONTRADICTION, 1 )
    def gen_two_hop_not_in(self):

        for smaller_objs, smaller_conts, larger_conts \
                in [(self.sm_objects, self.sm_containers, self.med_containers),
                    (self.med_objects, self.med_containers, self.lg_containers),
                    (self.sm_objects, self.sm_containers, self.lg_containers),
                    (self.sm_objects, self.med_containers, self.lg_containers)]:

            for sm_obj, sm_cont, med_cont \
                    in product(smaller_objs, smaller_conts, larger_conts):
                
                for out_rels_1, out_rels_2 \
                        in product(self.out_rels, self.out_rels):
                
                    # 0. The X_obj is OUT the Y_cont. The Y_cont is OUT the Z_cont.
                    premise = f"The {sm_obj} is {out_rels_1} the {sm_cont}. The {sm_cont} is {out_rels_2} the {med_cont}."

                    for in_rel_2 in self.in_rels:
                        # 1. The X_obj is in the Z_cont. Neutral
                        hypothesis = f"The {sm_obj} is {in_rel_2} the {med_cont}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )
                    
                    for out_rel_1 in self.out_rels:
                        # 1. The X_obj is out the Z_cont. Neutral
                        hypothesis = f"The {sm_obj} is {out_rel_1} the {med_cont}."
                        yield ( premise, hypothesis, self.NEUTRAL, 0 )
                

                for out_rels_1, in_rels_3 \
                        in product(self.out_rels, self.in_rels):
                
                    # 0. The X_obj is OUT the Y_cont. The Y_cont is OUT the Z_cont.
                    premise = f"The {sm_obj} is {out_rels_1} the {sm_cont}. The {sm_cont} is {in_rels_3} the {med_cont}."

                    for in_rel_4 in self.in_rels:
                        # 1. The X_obj is in the Z_cont. Neutral
                        hypothesis = f"The {sm_obj} is {in_rel_4} the {med_cont}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )
                    
                    for out_rel_1 in self.out_rels:
                        # 1. The X_obj is out the Z_cont. Neutral
                        hypothesis = f"The {sm_obj} is {out_rel_1} the {med_cont}."
                        yield ( premise, hypothesis, self.NEUTRAL, 0 )


    def gen_two_hop_fit_in(self):

        for smaller_objs, smaller_conts, larger_conts \
                in [(self.sm_objects, self.sm_containers, self.med_containers),
                    (self.med_objects, self.med_containers, self.lg_containers),
                    (self.sm_objects, self.sm_containers, self.lg_containers),
                    (self.sm_objects, self.med_containers, self.lg_containers)]:

            for sm_obj, sm_cont, med_cont \
                    in product(smaller_objs, smaller_conts, larger_conts):
                
                for fit_in_rel_1, fit_in_rel_2 \
                        in product(self.fits_in_phrases, self.fits_in_phrases):
                
                    # 0. The X_obj is IN the Y_cont. The Y_cont is IN the Z_cont.
                    premise = f"The {sm_obj} {fit_in_rel_1} the {sm_cont}. The {sm_cont} {fit_in_rel_2} the {med_cont}."

                    for fit_in_rel_3 in self.fits_in_phrases:
                        # 1. The X_obj is in the Z_cont. True
                        hypothesis = f"The {sm_obj} {fit_in_rel_3} the {med_cont}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )
                    
                    for cannot_fit_in_rel_1 in self.cannot_fit_in_phrases:
                        # 1. The Z_cont is in the X_obj. False
                        hypothesis = f"The {sm_obj} {cannot_fit_in_rel_1} the {med_cont}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

    def gen_two_hop_not_fit_in(self):

        for larger_objs, larger_conts, smaller_conts \
                in [(self.lg_objects, self.med_containers, self.sm_containers)]:

            for lg_obj, med_cont, sm_cont \
                    in product(larger_objs, larger_conts, smaller_conts):
                
                for cannot_fit_1, cannot_fit_2 \
                        in product(self.cannot_fit_in_phrases, self.cannot_fit_in_phrases):
                
                    # 0. The X_obj CANNOT_FIT_IN the Y_cont. The Y_cont CANNOT_FIT_IN the Z_cont.
                    premise = f"The {lg_obj} {cannot_fit_1} the {med_cont}. The {med_cont} {cannot_fit_2} the {sm_cont}."

                    for in_rel_3 in self.in_rels:
                        # 0. The X_obj is in the Z_cont. False
                        hypothesis = f"The {lg_obj} is {in_rel_3} the {sm_cont}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

                    for contains_phrase in self.fits_in_phrases:
                        # 0. The Z_cont CAN_CONTAIN the X_obj. False
                        hypothesis = f"The {sm_cont} {contains_phrase} the {lg_obj}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )

                    for cannot_contains_phrase in self.cannot_fit_in_phrases:
                        # 0. The Z_cont CANNOT_CONTAIN the X_obj. True
                        hypothesis = f"The {sm_cont} {cannot_contains_phrase} the {lg_obj}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )


    def gen_two_hop_compare_in_1(self):
        
        for smaller_objs, small_objs, container \
            in [(self.sm_objects, self.med_objects, self.med_containers),
                (self.sm_objects, self.med_objects, self.lg_containers),
                (self.sm_objects, self.lg_objects, self.lg_containers),
                (self.med_objects, self.lg_objects, self.lg_containers)]:
            
            for smer_obj, sm_obj, cont \
                    in product(smaller_objs, small_objs, container):
                
                for in_rel_2 in self.in_rels:
                
                    # 0. X_obj smaller than Y_obj. Y_obj CAN_FIT_IN Z_cont
                    premise = f"The {smer_obj} is smaller than the {sm_obj}. The {sm_obj} {in_rel_2} the {cont}."
                    
                    for in_rel_3 in self.in_rels:
                        # 1. The X_obj is in the Z_cont. Neutral
                        hypothesis = f"The {smer_obj} is {in_rel_3} the {cont}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )


    def gen_two_hop_compare_fit_in_1(self):
        
        for smaller_objs, small_objs, container \
            in [(self.sm_objects, self.med_objects, self.med_containers),
                (self.sm_objects, self.med_objects, self.lg_containers),
                (self.sm_objects, self.lg_objects, self.lg_containers),
                (self.med_objects, self.lg_objects, self.lg_containers)]:
            
            for smer_obj, sm_obj, cont \
                    in product(smaller_objs, small_objs, container):
                
                for fit_in_rel in self.fits_in_phrases:
                
                    # 0. X_obj smaller than Y_obj. Y_obj CAN_FIT_IN Z_cont
                    premise = f"The {smer_obj} is smaller than the {sm_obj}. The {sm_obj} {fit_in_rel} the {cont}."

                    for fit_in_rel_3 in self.fits_in_phrases:
                        # 1. The X_obj FITS_IN in the Z_cont. True
                        hypothesis = f"The {smer_obj} {fit_in_rel_3} the {cont}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )
                    
                    for cannot_fit_in_rel_1 in self.cannot_fit_in_phrases:
                        # 1. The X_obj CANNOT_FIT_IN the Z_cont. False
                        hypothesis = f"The {smer_obj} {cannot_fit_in_rel_1} the {cont}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )
            
    def gen_two_hop_compare_fit_in_2(self):
            
            for smaller_objs, small_objs, container \
                in [(self.sm_objects, self.med_objects, self.sm_containers),
                    (self.sm_objects, self.lg_objects, self.sm_containers),
                    (self.sm_objects, self.lg_objects, self.med_containers),
                    (self.med_objects, self.lg_objects, self.med_containers)]:
                
                for smer_obj, sm_obj, cont \
                        in product(smaller_objs, small_objs, container):
                    
                    for cannot_fit_in_rel in self.cannot_fit_in_phrases:
                    
                        # 0. X_obj smaller than Y_obj. Y_obj CANNOT_FIT_IN Z_cont
                        premise = f"The {smer_obj} is smaller than the {sm_obj}. The {sm_obj} {cannot_fit_in_rel} the {cont}."

                        for fit_in_rel_3 in self.fits_in_phrases:
                            # 1. The X_obj FITS_IN in the Z_cont. Neutral
                            hypothesis = f"The {smer_obj} {fit_in_rel_3} the {cont}."
                            yield ( premise, hypothesis, self.NEUTRAL, 0 )
                        
                        for cannot_fit_in_rel_1 in self.cannot_fit_in_phrases:
                            # 1. The X_obj CANNOT_FIT_IN the Z_cont. Neutral
                            hypothesis = f"The {smer_obj} {cannot_fit_in_rel_1} the {cont}."
                            yield ( premise, hypothesis, self.NEUTRAL, 1 )
                


    def gen_two_hop_compare_fit_in_3(self):
        
        for small_objs, smaller_objs, container \
            in [(self.lg_objects, self.med_objects, self.sm_containers)]:
            
            for sm_obj, smer_obj, cont \
                    in product(small_objs, smaller_objs, container):
                
                for cannot_fit_in_rel in self.cannot_fit_in_phrases:
                
                    # 0. X_obj larger than Y_obj. Y_obj CANNOT_FIT_IN Z_cont
                    premise = f"The {sm_obj} is larger than the {smer_obj}. The {smer_obj} {cannot_fit_in_rel} the {cont}."

                    for fit_in_rel_3 in self.fits_in_phrases:
                        # 1. The X_obj FITS_IN in the Z_cont
                        hypothesis = f"The {sm_obj} {fit_in_rel_3} the {cont}."
                        yield ( premise, hypothesis, self.CONTRADICTION, 1 )
                    
                    for cannot_fit_in_rel_1 in self.cannot_fit_in_phrases:
                        # 1. The X_obj is in the Z_cont. False
                        hypothesis = f"The {sm_obj} {cannot_fit_in_rel_1} the {cont}."
                        yield ( premise, hypothesis, self.ENTAILMENT, 0 )
    

    def gen_two_hop_compare_fit_in_4(self):
        
        for small_objs, smaller_objs, container \
            in [(self.med_objects, self.sm_objects, self.med_containers),
                (self.lg_objects, self.sm_objects, self.lg_containers),
                (self.lg_objects, self.med_objects, self.lg_containers)]:
            
            for sm_obj, smer_obj, cont \
                    in product(small_objs, smaller_objs, container):
                
                for fit_in_rel in self.fits_in_phrases:
                
                    # 0. X_obj larger than Y_obj. Y_obj CAN_FIT_IN Z_cont
                    premise = f"The {sm_obj} is larger than the {smer_obj}. The {smer_obj} {fit_in_rel} the {cont}."

                    for fit_in_rel_3 in self.fits_in_phrases:
                        # 1. The X_obj FITS_IN in the Z_cont
                        hypothesis = f"The {sm_obj} {fit_in_rel_3} the {cont}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )
                    
                    for cannot_fit_in_rel_1 in self.cannot_fit_in_phrases:
                        # 1. The X_obj is in the Z_cont. False
                        hypothesis = f"The {sm_obj} {cannot_fit_in_rel_1} the {cont}."
                        yield ( premise, hypothesis, self.NEUTRAL, 2 )
   

