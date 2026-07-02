import pyautogui

from config import SMOOTHENING


class MouseController:

    def __init__(self):

        self.screen_width, self.screen_height = pyautogui.size()

        pyautogui.FAILSAFE = False

        self.prev_x = 0
        self.prev_y = 0

        self.click_ready = True

    def move_mouse(self, target_x, target_y):

        current_x = self.prev_x + (target_x - self.prev_x) / SMOOTHENING
        current_y = self.prev_y + (target_y - self.prev_y) / SMOOTHENING

        pyautogui.moveTo(current_x, current_y)

        self.prev_x = current_x
        self.prev_y = current_y

    def left_click(self):

        pyautogui.click()