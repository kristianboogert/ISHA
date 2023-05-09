import mediapipe
import math
import cv2

from .HandType import *
from .HandJointType import *

# TODO: Functions only work if both hands are visible!
class HandPoseDetection:
    def __init__(self):
        self.mpHands = mediapipe.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
    def getPose(self, cameraColorFrame):
        cameraColorFrame = cv2.cvtColor(cameraColorFrame, cv2.COLOR_BGR2RGB)
        cameraColorFrame.flags.writeable = False
        handPoseData = self.hands.process(cameraColorFrame)
        cameraColorFrame.flags.writeable = True
        cameraColorFrame = cv2.cvtColor(cameraColorFrame, cv2.COLOR_RGB2BGR)
        return handPoseData
    def getHandJointLandmark(self, handType, handJointType, handPoseData):
        try:
            return handPoseData.multi_hand_landmarks[int(handType)].landmark[int(handJointType)]
        except:
            return None
    # def drawPose(self, cameraColorFrame, handPoseData):
    #     if handPoseData is not None:
    #         if handPoseData.multi_hand_landmarks:
    #             for hand, hand_landmarks in enumerate(handPoseData.multi_hand_landmarks):
    #                 self.draw.draw_landmarks(image=cameraColorFrame, landmark_list=hand_landmarks, connections=self.mpHands.HAND_CONNECTIONS)
    #         return cameraColorFrame

    # def getDirectionVector(self, landmark1, landmark2):
    #     try:
    #         return {
    #             "x": landmark1.x - landmark2.x,
    #             "y": landmark1.y - landmark2.y,
    #             "z": landmark1.z - landmark2.z
    #         }
    #     except:
    #         return None
    # def getDirectionVectorForHandParts(self, hand, handPart, originHandPart, handPoseData):
    #     landmark1 = self.getHandLandmark(hand, handPart, handPoseData)
    #     landmark2 = self.getHandLandmark(hand, originHandPart, handPoseData)
    #     print("landmark1:", landmark1)
    #     print("landmark2:", landmark2)
    #     return self.getDirectionVector(landmark1, landmark2)

    #     # if handPoseData.multi_hand_landmarks is None:
    #     #     return None
    #     # landmarks = handPoseData.multi_hand_landmarks
    #     # return self.getDirectionVector(landmarks[HandPart], landmarks[originHandPart])
    # def getAnglesFromDirectionVector(self, directionVector):
    #     if directionVector is None:
    #         return None
    #     x, y, z = directionVector["x"], directionVector["y"], directionVector["z"]
    #     xyAngle = math.degrees(math.atan2(y,x))
    #     yzAngle = math.degrees(math.atan2(z,y))
    #     xzAngle = math.degrees(math.atan2(z,x))
    #     return {
    #         "xy": xyAngle,
    #         "yz": yzAngle,
    #         "xz": xzAngle
    #     }
    # def getHandRotation(self, hand, handPoseData):
    #     index_finger_mcp = self.getHandLandmark(hand, HandPart.INDEX_FINGER_MCP, handPoseData)
    #     ring_finger_mcp = self.getHandLandmark(hand, HandPart.RING_FINGER_MCP, handPoseData)
    #     if hand == Hand.LEFT_HAND:
    #         knuckle_rotation_vector = self.getDirectionVector(index_finger_mcp, ring_finger_mcp)
    #     else:
    #         knuckle_rotation_vector = self.getDirectionVector(ring_finger_mcp, index_finger_mcp)
    #     knuckle_rotation_vector_angles = self.getAnglesFromDirectionVector(knuckle_rotation_vector)
    #     try:
    #         if hand == Hand.RIGHT_HAND:
    #             knuckle_rotation_vector_angles["xy"] = -knuckle_rotation_vector_angles["xy"]
    #         return knuckle_rotation_vector_angles["xy"]
    #     except:
    #         return None
    # # TODO: just like with poseDetection, correct the angle of a set of joints based on other joint angles!
    # def getAnglesFromHandParts(self, hand, handPart, originHandPart, handPoseData):
    #         landmark1 = self.getHandLandmark(hand, handPart, handPoseData)
    #         landmark2 = self.getHandLandmark(hand, originHandPart, handPoseData)
    #         directionVector = self.getDirectionVector(landmark1, landmark2)
    #         angles = self.getAnglesFromDirectionVector(directionVector)
    #         return angles
    # def getAngleDifference(self, handPartAngles, originHandPartAngles):
    #     try:
    #         return {
    #             "xy": handPartAngles["xy"] - originHandPartAngles["xy"],
    #             "yz": handPartAngles["yz"] - originHandPartAngles["yz"],
    #             "xz": handPartAngles["xz"] - originHandPartAngles["xz"],
    #         }
    #     except:
    #         return None
    # def getAnglesForHandPart(self, hand, handPart, handPoseData):
    #     if handPart == HandPart.WRIST:
    #         return self.getAnglesFromHandParts(hand, HandPart.WRIST, HandPart.THUMB_MCP, handPoseData)
    #     if handPart == HandPart.THUMB_CMC:
    #         return self.getAnglesFromHandParts(hand, HandPart.THUMB_CMC, HandPart.WRIST, handPoseData)
    #     if handPart == HandPart.THUMB_MCP:
    #         return self.getAnglesFromHandParts(hand, HandPart.THUMB_MCP, HandPart.THUMB_CMC, handPoseData)
    #     if handPart == HandPart.THUMB_IP:
    #         return self.getAnglesFromHandParts(hand, HandPart.THUMB_CMC, HandPart.THUMB_IP, handPoseData)
    #     if handPart == HandPart.THUMB_TIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.THUMB_IP, HandPart.THUMB_TIP, handPoseData)
    #     if handPart == HandPart.INDEX_FINGER_MCP:
    #         return self.getAnglesFromHandParts(hand, HandPart.INDEX_FINGER_MCP, HandPart.WRIST, handPoseData)
    #     if handPart == HandPart.INDEX_FINGER_PIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.INDEX_FINGER_PIP, HandPart.INDEX_FINGER_MCP, handPoseData)
    #     if handPart == HandPart.INDEX_FINGER_DIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.INDEX_FINGER_DIP, HandPart.INDEX_FINGER_PIP, handPoseData)
    #     if handPart == HandPart.INDEX_FINGER_TIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.INDEX_FINGER_TIP, HandPart.INDEX_FINGER_DIP, handPoseData)
    #     if handPart == HandPart.MIDDLE_FINGER_MCP:
    #         return self.getAnglesFromHandParts(hand, HandPart.MIDDLE_FINGER_MCP, HandPart.WRIST, handPoseData)
    #     if handPart == HandPart.MIDDLE_FINGER_PIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.MIDDLE_FINGER_PIP, HandPart.MIDDLE_FINGER_MCP, handPoseData)
    #     if handPart == HandPart.MIDDLE_FINGER_DIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.MIDDLE_FINGER_DIP, HandPart.MIDDLE_FINGER_PIP, handPoseData)
    #     if handPart == HandPart.MIDDLE_FINGER_TIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.MIDDLE_FINGER_TIP, HandPart.MIDDLE_FINGER_DIP, handPoseData)
    #     if handPart == HandPart.RING_FINGER_MCP:
    #         return self.getAnglesFromHandParts(hand, HandPart.RING_FINGER_MCP, HandPart.WRIST, handPoseData)
    #     if handPart == HandPart.RING_FINGER_PIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.RING_FINGER_PIP, HandPart.RING_FINGER_MCP, handPoseData)
    #     if handPart == HandPart.RING_FINGER_DIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.RING_FINGER_DIP, HandPart.RING_FINGER_PIP, handPoseData)
    #     if handPart == HandPart.RING_FINGER_TIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.RING_FINGER_TIP, HandPart.RING_FINGER_DIP, handPoseData)
    #     if handPart == HandPart.PINKY_MCP:
    #         return self.getAnglesFromHandParts(hand, HandPart.PINKY_MCP, HandPart.WRIST, handPoseData)
    #     if handPart == HandPart.PINKY_PIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.PINKY_PIP, HandPart.PINKY_MCP, handPoseData)
    #     if handPart == HandPart.PINKY_DIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.PINKY_DIP, HandPart.PINKY_PIP, handPoseData)
    #     if handPart == HandPart.PINKY_TIP:
    #         return self.getAnglesFromHandParts(hand, HandPart.PINKY_TIP, HandPart.PINKY_DIP, handPoseData)
