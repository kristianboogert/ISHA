import mediapipe
import math
import cv2

class HandPoseDetection:
    def __init__(self, displayPose=False, visibilityThreshold=0.9):
        self.displayPose = displayPose
        self.visibilityThreshold = visibilityThreshold
        self.mpHands = mediapipe.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
        self.draw = mediapipe.solutions.drawing_utils
        self.handData = None
    def getPose(self, cameraColorFrame):
        cameraColorFrame = cv2.cvtColor(cameraColorFrame, cv2.COLOR_BGR2RGB)
        cameraColorFrame.flags.writeable = False
        self.handData = self.hands.process(cameraColorFrame)
        cameraColorFrame.flags.writeable = True
        cameraColorFrame = cv2.cvtColor(cameraColorFrame, cv2.COLOR_RGB2BGR)
        if self.displayPose:
            if self.handData.multi_hand_landmarks:
                for hand, hand_landmarks in enumerate(self.handData.multi_hand_landmarks):
                    self.draw.draw_landmarks(image=cameraColorFrame, landmark_list=hand_landmarks, connections=self.mpHands.HAND_CONNECTIONS)
        return (self.handData, cameraColorFrame)
    def getHandLandmark(self, handData, hand, handPart):
        try:
            return handData.multi_hand_landmarks[hand].landmark[handPart]
        except:
            None
    def getDirectionVector(self, landmark1, landmark2):
        try:
            return {
                "x": landmark1.x - landmark2.x,
                "y": landmark1.y - landmark2.y,
                "z": landmark1.z - landmark2.z
            }
        except:
            return None
    def getAnglesFromDirectionVector(self, directionVector):
        if directionVector is None:
            return None
        x, y, z = directionVector["x"], directionVector["y"], directionVector["z"]
        xyAngle = math.degrees(math.atan2(y,x))
        yzAngle = math.degrees(math.atan2(z,y))
        xzAngle = math.degrees(math.atan2(z,x))
        return {
            "xy": xyAngle,
            "yz": yzAngle,
            "xz": xzAngle
        }
    # TODO: FINISH THIS CLASS