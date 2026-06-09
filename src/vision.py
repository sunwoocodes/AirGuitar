import cv2
import mediapipe as mp

class VisionController:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            model_complexity=0,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils

    def count_fingers(self, hand_landmarks, handedness):

        fingers = []

        # 엄지

        thumb_tip = hand_landmarks.landmark[4]
        thumb_ip = hand_landmarks.landmark[3]

        if handedness == "Right":
            fingers.append(thumb_tip.x < thumb_ip.x)
        else:
            fingers.append(thumb_tip.x > thumb_ip.x)

        # 나머지 손가락

        tips = [8, 12, 16, 20]

        for tip in tips:

            fingers.append(

                hand_landmarks.landmark[tip].y
                <
                hand_landmarks.landmark[tip - 2].y
            )

        return fingers

    def recognize_gesture(self, fingers):

        thumb, index, middle, ring, pinky = fingers

        total = sum(fingers)

        if total == 0:
            return "FIST"

        if index and middle and not ring and not pinky:
            return "V_SIGN"

        if index and middle and ring and not pinky:
            return "THREE"

        if total == 5:
            return "OPEN_HAND"

        if thumb and total == 1:
            return "THUMB_UP"

        return "UNKNOWN"

    def process_frame(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        strum_y = None
        gesture_name = "UNKNOWN"

        if results.multi_hand_landmarks and results.multi_handedness:

            hand_data = []

            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):

                label = handedness.classification[0].label

                hand_data.append((label, hand_landmarks))

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

            for label, hand_landmarks in hand_data:

                # 왼손 = 코드 선택
                if label == "Left":

                    fingers = self.count_fingers(
                        hand_landmarks,
                        label
                    )

                    gesture_name = self.recognize_gesture(
                        fingers
                    )

                # 오른손 = 줄 튕김
                elif label == "Right":

                    strum_y = hand_landmarks.landmark[8].y

        return frame, strum_y, gesture_name