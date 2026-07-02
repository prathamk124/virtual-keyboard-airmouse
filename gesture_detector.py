import math

from config import PINCH_THRESHOLD


class GestureDetector:

    def distance(self, p1, p2):

        return math.hypot(

            p1[0] - p2[0],

            p1[1] - p2[1]

        )

    def thumb_index(self, hand):

        return self.distance(

            hand["lmList"][4],

            hand["lmList"][8]

        )

    def thumb_middle(self, hand):

        return self.distance(

            hand["lmList"][4],

            hand["lmList"][12]

        )

    def thumb_ring(self, hand):

        return self.distance(

            hand["lmList"][4],

            hand["lmList"][16]

        )

    def is_index_pinch(self, hand):

        return self.thumb_index(hand) < PINCH_THRESHOLD

    def is_middle_pinch(self, hand):

        return self.thumb_middle(hand) < PINCH_THRESHOLD

    def is_ring_pinch(self, hand):

        return self.thumb_ring(hand) < PINCH_THRESHOLD
    def thumb_pinky(self, hand):

        return self.distance(

            hand["lmList"][4],

            hand["lmList"][20]

        )
    def is_pinky_pinch(self, hand):

        return self.thumb_pinky(hand) < PINCH_THRESHOLD    
