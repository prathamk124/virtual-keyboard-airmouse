import cv2

from hand_tracker import HandTracker
from mouse_controller import MouseController
from config import FRAME_MARGIN
from gestures import GestureDetector


def main():

    # Open webcam
    cap = cv2.VideoCapture(0)

    # Optional: Increase camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Initialize classes
    tracker = HandTracker()
    mouse = MouseController()
    gesture = GestureDetector()

    while True:

        success, frame = cap.read()

        if not success:
            break

        # Mirror the frame
        frame = cv2.flip(frame, 1)

        # Draw interaction box
        cv2.rectangle(
            frame,
            (FRAME_MARGIN, FRAME_MARGIN),
            (
                frame.shape[1] - FRAME_MARGIN,
                frame.shape[0] - FRAME_MARGIN,
            ),
            (255, 0, 255),
            2,
        )

        # Detect hands
        frame, hands = tracker.detect_hands(frame)

        if hands:

            for hand in hands:

                # Only use the right hand
                if hand["type"] == "Right":

                    # Index fingertip (Landmark 8)
                    index_x, index_y = hand["lmList"][8]

                    # Map camera coordinates to screen coordinates
                    screen_x = (
                        (index_x - FRAME_MARGIN)
                        * mouse.screen_width
                        / (frame.shape[1] - 2 * FRAME_MARGIN)
                    )

                    screen_y = (
                        (index_y - FRAME_MARGIN)
                        * mouse.screen_height
                        / (frame.shape[0] - 2 * FRAME_MARGIN)
                    )

                    # Keep cursor inside screen
                    screen_x = max(0, min(mouse.screen_width, screen_x))
                    screen_y = max(0, min(mouse.screen_height, screen_y))

                    # Move mouse
                    mouse.move_mouse(screen_x, screen_y)
                    if gesture.is_pinching(hand):

                        cv2.putText(
                            frame,
                            "CLICK",
                            (30, 60),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0,255,0),
                            3,
                        )

                        if mouse.click_ready:

                            mouse.left_click()

                            mouse.click_ready = False

                    else:

                        mouse.click_ready = True
        cv2.imshow("Virtual Keyboard & Air Mouse", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()