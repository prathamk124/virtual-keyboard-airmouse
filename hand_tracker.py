import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils
    def detect_hands(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        hands = []

        if results.multi_hand_landmarks:

            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                h, w, _ = frame.shape

                lm_list = []

                for idx, lm in enumerate(hand_landmarks.landmark):

                    x = int(lm.x * w)
                    y = int(lm.y * h)

                    lm_list.append((x, y))

                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                    cv2.putText(
                        frame,
                        str(idx),
                        (x + 5, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4,
                        (255, 0, 0),
                        1
                    )

                hands.append({
                    "type": handedness.classification[0].label,
                    "lmList": lm_list
                })

        return frame, hands