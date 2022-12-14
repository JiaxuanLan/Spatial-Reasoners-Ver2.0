from itertools import product
from .base import BaseGenerator


class DistanceGenerator(BaseGenerator):

    reasoning_type = 'distance'

    objects = {'baseball', 'chair', 'desk', 'bottle', 'pond'}
    touching = {'touching', 'pyhsically contact with', 'adjoin'}
    nearby = {'close to', 'nearby', 'next to'}


    def gen_touching_positive(self):
        """
        Template:
            P: The OBJ_1 is TOUCH_RELATION the OBJ_2.
            H1: The OBJ_2 is TOUCH_RELATION of the OBJ_1.
            H2: The OBJ_1 is NEAR_RELATION of the OBJ_2.
            H3: The OBJ_2 is NEAR_RELATION of the OBJ_1.

        Example:
            P: The ball is touching the cup.
            H1: The cup is touching the ball.
            H2: The ball is near the cup.
            H3: The cup is near the ball.
        """
        for obj_1, touch_rel, near_rel, obj_2 in product(self.objects, self.touching, self.nearby, self.objects):
            if obj_1 != obj_2:
                premise = f"The {obj_1} is {touch_rel} the {obj_2}."
                yield ( premise, f"The {obj_2} is {touch_rel} the {obj_1}.", self.ENTAILMENT, 0 )
                yield ( premise, f"The {obj_1} is {near_rel} the {obj_2}.", self.ENTAILMENT, 1 )
                yield ( premise, f"The {obj_2} is {near_rel} the {obj_1}.", self.ENTAILMENT, 2 )


    def gen_nearby_neutral(self):
        """
        Template:
            P: The OBJ_1 is NEAR_RELATION of the OBJ_2.
            H1: The OBJ_1 is TOUCH_RELATION the OBJ_2.
            H2: The OBJ_2 is TOUCH_RELATION of the OBJ_1.

        Example:
            P: The ball is close to the cup.
            H1: The ball is touching the cup.
            H2: The cup is touching the ball.
        """
        for obj_1, touch_rel, near_rel, obj_2 in product(self.objects, self.touching, self.nearby, self.objects):
            if obj_1 != obj_2:
                premise = f"The {obj_1} is {near_rel} the {obj_2}."
                yield ( premise, f"The {obj_1} is {touch_rel} the {obj_2}.", self.NEUTRAL, 0 )
                yield ( premise, f"The {obj_2} is {touch_rel} the {obj_1}.", self.NEUTRAL, 1 )


    def gen_touching_negative(self):
        """
        Template:
            P: The OBJ_1 is TOUCH_RELATION the OBJ_2.
            H1: The OBJ_2 is TOUCH_RELATION of the OBJ_1.
            H2: The OBJ_1 is NEAR_RELATION of the OBJ_2.
            H3: The OBJ_2 is NEAR_RELATION of the OBJ_1.

        Example:
            P: The ball is touching the cup.
            H1: The cup is not touching the ball.
            H2: The ball is not near the cup.
            H3: The cup is not near the ball.
        """
        for obj_1, touch_rel, near_rel, obj_2 in product(self.objects, self.touching, self.nearby, self.objects):
            if obj_1 != obj_2:
                premise = f"The {obj_1} is {touch_rel} the {obj_2}."
                yield ( premise, f"The {obj_2} is not {touch_rel} the {obj_1}.", self.CONTRADICTION, 0 )
                yield ( premise, f"The {obj_1} is not {near_rel} the {obj_2}.", self.CONTRADICTION, 1 )
                yield ( premise, f"The {obj_2} is not {near_rel} the {obj_1}.", self.CONTRADICTION, 2 )


    def gen_not_touching_neutral(self):
        """
        Template:
            P: The OBJ_1 is not TOUCH_RELATION the OBJ_2.
            H1: The OBJ_1 is NEAR_RELATION of the OBJ_2.
            H2: The OBJ_1 is not NEAR_RELATION of the OBJ_2.
            H3: The OBJ_2 is NEAR_RELATION of the OBJ_1.
            H3: The OBJ_2 is not NEAR_RELATION of the OBJ_1.

        Example:
            P: The ball is not touching the cup.
            H1: The ball is near the cup.
            H2: The ball is not near the cup.
            H3: The cup is near the ball.
            H4: The cup is not near the ball.
        """
        for obj_1, touch_rel, near_rel, obj_2 in product(self.objects, self.touching, self.nearby, self.objects):
            if obj_1 != obj_2:
                premise = f"The {obj_1} is not {touch_rel} the {obj_2}."
                hypothesis_1 = f"The {obj_1} is {near_rel} the {obj_2}."
                hypothesis_2 = f"The {obj_1} is not {near_rel} the {obj_2}."
                hypothesis_3 = f"The {obj_2} is {near_rel} the {obj_1}."
                hypothesis_4 = f"The {obj_2} is not {near_rel} the {obj_1}."
                yield ( premise, hypothesis_1, self.NEUTRAL, 0 )
                yield ( premise, hypothesis_2, self.NEUTRAL, 1 )
                yield ( premise, hypothesis_3, self.NEUTRAL, 2 )
                yield ( premise, hypothesis_4, self.NEUTRAL, 3 )

    def gen_far_positive(self):
        """
        Template:
            P: The OBJ_1 is far from the OBJ_2.
            H1: The OBJ_2 is far from the OBJ_1.
            H2: The OBJ_1 is not close to the OBJ_2.
            H3: The OBJ_2 is not close to the OBJ_1.

        Example:
            P: The cup is far from the table.
            H1: The table is far from the cup.
            H2: The cup is not close to the table.
            H3: The table is not close to the cup.
        """
        for obj_1, obj_2 in product(self.objects, self.objects):
            if obj_1 != obj_2:
                premise = f"The {obj_1} is far from the {obj_2}."
                hypothesis_1 = f"The {obj_2} is far from the {obj_1}."
                yield ( premise, hypothesis_1, self.ENTAILMENT, 0 )
                for near_rel in self.nearby:
                    hypothesis_2 = f"The {obj_1} is not {near_rel} the {obj_2}."
                    hypothesis_3 = f"The {obj_2} is not {near_rel} the {obj_1}."
                    yield ( premise, hypothesis_2, self.ENTAILMENT, 1 )
                    yield ( premise, hypothesis_3, self.ENTAILMENT, 2 )

    def gen_far_negative(self):
        """
        Template:
            P: The OBJ_1 is far from the OBJ_2.
            H1: The OBJ_2 is far from the OBJ_1.
            H2: The OBJ_1 is not close to the OBJ_2.
            H3: The OBJ_2 is not close to the OBJ_1.

        Example:
            P: The cup is far from the table.
            H1: The table is far from the cup.
            H2: The cup is not close to the table.
            H3: The table is not close to the cup.
        """
        for obj_1, obj_2 in product(self.objects, self.objects):
            if obj_1 != obj_2:
                premise = f"The {obj_1} is far from the {obj_2}."
                for near_rel in self.nearby:
                    hypothesis_1 = f"The {obj_1} is {near_rel} the {obj_2}."
                    hypothesis_2 = f"The {obj_2} is {near_rel} the {obj_1}."
                    yield ( premise, hypothesis_1, self.CONTRADICTION, 0 )
                    yield ( premise, hypothesis_2, self.CONTRADICTION, 1 )

                for touch_rel in self.touching:
                    hypothesis_3 = f"The {obj_1} is {touch_rel} the {obj_2}."
                    hypothesis_4 = f"The {obj_2} is {touch_rel} the {obj_1}."
                    yield ( premise, hypothesis_3, self.CONTRADICTION, 2 )
                    yield ( premise, hypothesis_4, self.CONTRADICTION, 3 )

    def gen_transitivity_negative(self):
        """
        Template:
            P: The OBJ_1 is TOUCH_RELATION_1 the OBJ_2 and OBJ_2 is TOUCH_RELATION_2 OBJ_3.
            H: The OBJ_1 is TOUCH_RELATION_3 OBJ_3.

        Example:
            P: The ball is not touching the cup.
        """
        for obj_1, obj_2, obj_3, touch_rel_1, touch_rel_2, touch_rel_3 \
            in product(self.objects, self.objects, self.objects, self.touching, self.touching, self.touching):
            
            if obj_1 != obj_2 and obj_1 != obj_3 and obj_2 != obj_3:
                premise = f"The {obj_1} is {touch_rel_1} the {obj_2} and the {obj_2} is {touch_rel_2} the {obj_3}."
                hypothesis = f"The {obj_1} is {touch_rel_3} the {obj_3}."
                yield ( premise, hypothesis, self.CONTRADICTION, 0 )