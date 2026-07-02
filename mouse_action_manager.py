import time

from config import (
    DOUBLE_CLICK_COOLDOWN,
    RIGHT_CLICK_COOLDOWN,
)


class MouseActionManager:

    def __init__(self):

        self.last_double_click = 0

        self.last_right_click = 0

    def allow_double_click(self):

        now = time.time()

        if now - self.last_double_click > DOUBLE_CLICK_COOLDOWN:

            self.last_double_click = now

            return True

        return False

    def allow_right_click(self):

        now = time.time()

        if now - self.last_right_click > RIGHT_CLICK_COOLDOWN:

            self.last_right_click = now

            return True

        return False