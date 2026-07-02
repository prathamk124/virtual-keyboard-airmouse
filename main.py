import cv2
import pyautogui

from hand_tracker import HandTracker
from mouse_controller import MouseController
tracker = HandTracker()
mouse = MouseController()

def main():

    cap = cv2.VideoCapture(0)

    tracker = HandTracker()

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        frame, hands = tracker.detect_hands(frame)

        if hands:

            for hand in hands:

                hand_type = hand["type"]

                if hand["type"] == "Right":

                    index_x, index_y = hand["lmList"][8]

                    screen_x = index_x * mouse.screen_width / frame.shape[1]
                    screen_y = index_y * mouse.screen_height / frame.shape[0]

                    mouse.move_mouse(screen_x, screen_y)

        cv2.imshow("Virtual Keyboard & Air Mouse", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()