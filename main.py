import cv2

from hand_tracker import HandTracker


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

                print(hand_type)

        cv2.imshow("Virtual Keyboard & Air Mouse", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()