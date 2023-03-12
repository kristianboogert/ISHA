import cv2 
from mediapipe import mp

class HandDetection:
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.3):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=static_image_mode, max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence)
        self.draw = mp.solutions.drawing_utils

    def draw(self, color_frame, results):

        return color_frame

    def process(self, color_frame):
        results = self.hands.process(cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for hand, hand_landmarks in enumerate(results.multi_hand_landmarks):
                self.draw.draw_landmarks(image=color_frame, landmark_list=hand_landmarks, connections=self.mp_hands.HAND_CONNECTIONS)
                # for i in range(2):
                    # print(f'{self.mp_hands.HandLandmark(i).name}:')
                    # print(f'{hand_landmarks.landmark[self.mp_hands.HandLandmark(i).value]}')
        return results, color_frame