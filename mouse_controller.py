import pyautogui

from config import SMOOTHENING


class MouseController:

    def __init__(self):

        self.screen_width, self.screen_height = pyautogui.size()

        pyautogui.FAILSAFE = False

        self.prev_x = 0
        self.prev_y = 0

    def move_mouse(self, x, y):
        if abs(x - self.prev_x) < 2 and abs(y - self.prev_y) < 2:
            return

        current_x = self.prev_x + (x - self.prev_x) / SMOOTHENING

        current_y = self.prev_y + (y - self.prev_y) / SMOOTHENING

        pyautogui.moveTo(current_x, current_y)

        self.prev_x = current_x
        self.prev_y = current_y

    def left_click(self):

        pyautogui.click()

    def double_click(self):

        pyautogui.doubleClick()

    def right_click(self):

        pyautogui.rightClick()

    def start_drag(self):

        pyautogui.mouseDown()

    def stop_drag(self):

        pyautogui.mouseUp()