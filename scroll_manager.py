import pyautogui


class ScrollManager:

    def __init__(self):

        self.active = False

        self.previous_y = None

        self.threshold = 12

        self.scroll_speed = 35

    def start(self, current_y):

        self.active = True

        self.previous_y = current_y

    def stop(self):

        self.active = False

        self.previous_y = None

    def update(self, current_y):

        if self.previous_y is None:

            self.previous_y = current_y

            return

        difference = current_y - self.previous_y

        if abs(difference) > self.threshold:

            pyautogui.scroll(

                int(-difference * self.scroll_speed)

            )

            self.previous_y = current_y