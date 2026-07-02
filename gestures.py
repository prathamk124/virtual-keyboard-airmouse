import math

from config import PINCH_THRESHOLD


class GestureDetector:

    def is_pinching(self, hand):

        thumb_x, thumb_y = hand["lmList"][4]

        index_x, index_y = hand["lmList"][8]

        distance = math.hypot(
            index_x - thumb_x,
            index_y - thumb_y
        )

        return distance < PINCH_THRESHOLD