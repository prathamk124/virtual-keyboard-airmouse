import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )

        self.drawer = mp.solutions.drawing_utils

    def detect_hands(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        detected_hands = []

        if results.multi_hand_landmarks:

            for landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness,
            ):

                self.drawer.draw_landmarks(
                    frame,
                    landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                )

                h, w, _ = frame.shape

                lm_list = []

                xs = []
                ys = []

                for lm in landmarks.landmark:

                    x = int(lm.x * w)
                    y = int(lm.y * h)

                    xs.append(x)
                    ys.append(y)

                    lm_list.append((x, y))

                bbox = (
                    min(xs),
                    min(ys),
                    max(xs),
                    max(ys),
                )

                area = (
                    (bbox[2] - bbox[0])
                    * (bbox[3] - bbox[1])
                )

                detected_hands.append({

                    "type": handedness.classification[0].label,

                    "lmList": lm_list,

                    "bbox": bbox,

                    "area": area,

                })

        return frame, detected_hands