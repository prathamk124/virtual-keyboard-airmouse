import time

from config import (
    DRAG_THRESHOLD,
    LEFT_CLICK_COOLDOWN,
)


class GestureManager:

    def __init__(self):

        self.state = "OPEN"

        self.pinch_start = None

        self.last_click_time = 0

    def update(self, pinching):

        now = time.time()

        # -----------------------
        # OPEN
        # -----------------------
        if self.state == "OPEN":

            if pinching:

                self.state = "PINCH"

                self.pinch_start = now

            return "NONE"

        # -----------------------
        # PINCH
        # -----------------------
        elif self.state == "PINCH":

            if not pinching:

                self.state = "OPEN"

                if now - self.last_click_time > LEFT_CLICK_COOLDOWN:

                    self.last_click_time = now

                    return "CLICK"

                return "NONE"

            if now - self.pinch_start >= DRAG_THRESHOLD:

                self.state = "DRAG"

                return "START_DRAG"

            return "NONE"

        # -----------------------
        # DRAG
        # -----------------------
        elif self.state == "DRAG":

            if pinching:

                return "DRAG"

            self.state = "OPEN"

            return "STOP_DRAG"

        return "NONE"