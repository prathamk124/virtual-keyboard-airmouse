import cv2
import time

from config import (
    CAMERA_INDEX,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    FRAME_MARGIN,
)

from hand_tracker import HandTracker
from mouse_controller import MouseController
from gesture_detector import GestureDetector
from gesture_manager import GestureManager
from mouse_action_manager import MouseActionManager
from scroll_manager import ScrollManager


def main():

    # ----------------------------------
    # Camera
    # ----------------------------------

    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    cap.set(cv2.CAP_PROP_FPS, 60)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    # ----------------------------------
    # Initialize Modules
    # ----------------------------------

    tracker = HandTracker()
    mouse = MouseController()
    gesture_detector = GestureDetector()
    gesture_manager = GestureManager()
    action_manager = MouseActionManager()
    scroll = ScrollManager()
    previous_time = time.time()
    fps = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        h, w, _ = frame.shape

        # ----------------------------------
        # Interaction Area
        # ----------------------------------

        cv2.rectangle(
            frame,
            (FRAME_MARGIN, FRAME_MARGIN),
            (w - FRAME_MARGIN, h - FRAME_MARGIN),
            (255, 0, 255),
            2,
        )

        # ----------------------------------
        # Detect Hands
        # ----------------------------------

        frame, hands = tracker.detect_hands(frame)

        if hands:

            # Select largest RIGHT hand

            right_hands = [
                hand
                for hand in hands
                if hand["type"] == "Right"
            ]

            if right_hands:

                hand = max(
                    right_hands,
                    key=lambda h: h["area"]
                )

                # -----------------------------
                # Cursor
                # -----------------------------

                index_x, index_y = hand["lmList"][8]

                screen_x = (
                    (index_x - FRAME_MARGIN)
                    * mouse.screen_width
                    / (w - 2 * FRAME_MARGIN)
                )

                screen_y = (
                    (index_y - FRAME_MARGIN)
                    * mouse.screen_height
                    / (h - 2 * FRAME_MARGIN)
                )

                screen_x = max(
                    0,
                    min(mouse.screen_width, screen_x)
                )

                screen_y = max(
                    0,
                    min(mouse.screen_height, screen_y)
                )

                mouse.move_mouse(
                    screen_x,
                    screen_y,
                )

                # -----------------------------
                # Detect Gestures
                # -----------------------------

                index_pinch = gesture_detector.is_index_pinch(hand)

                middle_pinch = gesture_detector.is_middle_pinch(hand)

                ring_pinch = gesture_detector.is_ring_pinch(hand)
                pinky_pinch = gesture_detector.is_pinky_pinch(hand)

                status = "MOVE"

            # -----------------------------
            # Scroll Mode
            # -----------------------------

            if pinky_pinch:

                if not scroll.active:

                    scroll.start(index_y)

                scroll.update(index_y)

                status = "SCROLL"

            # -----------------------------
            # Exit Scroll
            # -----------------------------

            else:

                if scroll.active:

                    scroll.stop()

                # Double Click

                if middle_pinch:

                    if action_manager.allow_double_click():

                        mouse.double_click()

                        status = "DOUBLE CLICK"

                # ----------------------------------
                # Right Click
                # ----------------------------------

                elif ring_pinch:

                    if action_manager.allow_right_click():

                        mouse.right_click()

                        status = "RIGHT CLICK"

                # ----------------------------------
                # Left Click + Drag
                # ----------------------------------

                else:

                    action = gesture_manager.update(
                        index_pinch
                    )

                    if action == "CLICK":

                        mouse.left_click()

                        status = "LEFT CLICK"

                    elif action == "START_DRAG":

                        mouse.start_drag()

                        status = "START DRAG"

                    elif action == "DRAG":

                        status = "DRAGGING"

                    elif action == "STOP_DRAG":

                        mouse.stop_drag()

                        status = "STOP DRAG"

                # ----------------------------------
                # Draw Status
                # ----------------------------------

                cv2.putText(
                    frame,
                    status,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2,
                )
        current_time = time.time()

        current_fps = 1 / (current_time - previous_time)

        previous_time = current_time

        # Smooth the FPS display
        fps = (fps * 0.9) + (current_fps * 0.1)

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2,
        )

        cv2.imshow(
            "Virtual Keyboard & Air Mouse", 
            frame,
        )

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()