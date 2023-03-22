import mediapipe
from mediapipe.tasks.python.components.containers.landmark import Landmark
import math
import cv2

from .HandPart import *

# TODO: FINISH THIS CLASS
class HandPoseDetection:
    def __init__(self, displayPose=False, visibilityThreshold=0.9):
        self.displayPose = displayPose
        self.visibilityThreshold = visibilityThreshold
        self.mpHands = mediapipe.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
        self.draw = mediapipe.solutions.drawing_utils
    def getPose(self, cameraColorFrame):
        cameraColorFrame = cv2.cvtColor(cameraColorFrame, cv2.COLOR_BGR2RGB)
        cameraColorFrame.flags.writeable = False
        handData = self.hands.process(cameraColorFrame)
        cameraColorFrame.flags.writeable = True
        cameraColorFrame = cv2.cvtColor(cameraColorFrame, cv2.COLOR_RGB2BGR)
        return handData
    def drawPose(self, cameraColorFrame, handData):
        if poseData is not None:
            if handData.multi_hand_landmarks:
                for hand, hand_landmarks in enumerate(handData.multi_hand_landmarks):
                    self.draw.draw_landmarks(image=cameraColorFrame, landmark_list=hand_landmarks, connections=self.mpHands.HAND_CONNECTIONS)
            return cameraColorFrame
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
    # TODO: Function only works if both hands are visible and
    # if the hand is facing the camera!
    def getHandRotation(self, hand, handPoseData):
        index_finger_mcp = self.getHandLandmark(handPoseData, hand, HandPart.INDEX_FINGER_MCP)
        ring_finger_mcp = self.getHandLandmark(handPoseData, hand, HandPart.RING_FINGER_MCP)
        if hand == Hand.LEFT_HAND:
            knuckle_rotation_vector = self.getDirectionVector(index_finger_mcp, ring_finger_mcp)
        else:
            knuckle_rotation_vector = self.getDirectionVector(ring_finger_mcp, index_finger_mcp)
        knuckle_rotation_vector_angles = self.getAnglesFromDirectionVector(knuckle_rotation_vector)
        try:
            if hand == Hand.RIGHT_HAND:
                knuckle_rotation_vector_angles["xy"] = -knuckle_rotation_vector_angles["xy"]
            return knuckle_rotation_vector_angles["xy"]
        except:
            return None