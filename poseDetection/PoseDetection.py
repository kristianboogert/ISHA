import mediapipe
import math
import cv2

from .BodyPart import *

class PoseDetection:
    ###
    # Public
    ###
    def __init__(self, display_pose=False, visibility_threshold=0.9):
        self.display_pose = display_pose
        self.visibility_threshold = visibility_threshold
        # Define pose detection model
        self.mpPose = mediapipe.solutions.pose
        self.pose = self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        # Define hand detection model
        self.mpHands = mediapipe.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
        # Define mediapipe drawing util
        self.draw = mediapipe.solutions.drawing_utils
        # Keep track of pose data
        self.poseData = None
        self.handData = None
    def getPose(self, cameraFrame):
        # Get the pose data from mediapipe
        cameraFrame = cv2.cvtColor(cameraFrame, cv2.COLOR_BGR2RGB)
        cameraFrame.flags.writeable = False
        self.poseData = self.pose.process(cameraFrame)
        self.handData = self.hands.process(cameraFrame)
        cameraFrame.flags.writeable = True
        cameraFrame = cv2.cvtColor(cameraFrame, cv2.COLOR_RGB2BGR)
        # If required, display the data
        if self.display_pose:
            self.draw.draw_landmarks(cameraFrame, self.poseData.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
            if self.handData.multi_hand_landmarks:
                for hand, hand_landmarks in enumerate(self.handData.multi_hand_landmarks):
                    self.draw.draw_landmarks(image=cameraFrame, landmark_list=hand_landmarks, connections=self.mpHands.HAND_CONNECTIONS)
        return (self.poseData, self.handData, cameraFrame)
    def getPoseLandmark(self, poseData, limb):
        try:
            return poseData.pose_landmarks.landmark[limb]
        except:
            None
    def getDirectionVectorForBodypart(self, bodyPart, poseData, originBodyPart=None):
        if poseData.pose_landmarks is None:
            return None
        landmarks = poseData.pose_landmarks.landmark
        return self._getDirectionVector(landmarks[bodyPart], landmarks[originBodyPart])
    def _getDirectionVector(self, landmark_1, landmark_2, visibility_threshold=0.75):
        if landmark_1.visibility > visibility_threshold and landmark_2.visibility > visibility_threshold:
            return {
                "x": landmark_1.x - landmark_2.x,
                "y": landmark_1.y - landmark_2.y,
                "z": landmark_1.z - landmark_2.z
            }
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
    def getAnglesForBodyPart(self, bodyPart, poseData):
        if bodyPart == BodyPart.LEFT_SHOULDER:
            leftShoulderDirectionVector = self.getDirectionVectorForBodypart(BodyPart.LEFT_SHOULDER, poseData, originBodyPart=BodyPart.RIGHT_SHOULDER)
            leftShoulderAngles = self.getAnglesFromDirectionVector(leftShoulderDirectionVector)
            leftShoulderAngles["xy"] = -leftShoulderAngles["xy"]
            leftShoulderAngles["yz"] = -leftShoulderAngles["yz"]
            leftShoulderAngles["xz"] = -leftShoulderAngles["xz"]
            return leftShoulderAngles
        if bodyPart == BodyPart.RIGHT_SHOULDER:
            rightShoulderDirectionVector = self.getDirectionVectorForBodypart(BodyPart.LEFT_SHOULDER, poseData, originBodyPart=BodyPart.RIGHT_SHOULDER)
            rightShoulderAngles = self.getAnglesFromDirectionVector(rightShoulderDirectionVector)
            return rightShoulderAngles
        if bodyPart == BodyPart.LEFT_ELBOW:
            leftShoulderAngles = self.getAnglesForBodyPart(BodyPart.LEFT_SHOULDER, poseData)
            leftElbowDirectionVector = self.getDirectionVectorForBodypart(BodyPart.LEFT_ELBOW, poseData, originBodyPart=BodyPart.LEFT_SHOULDER)
            leftElbowAngles = self.getAnglesFromDirectionVector(leftElbowDirectionVector)
            leftElbowAngles["xy"] = -(leftShoulderAngles["xy"]+leftElbowAngles["xy"])
            leftElbowAngles["yz"] = -(leftShoulderAngles["yz"]+leftElbowAngles["yz"])
            leftElbowAngles["xz"] = -(leftShoulderAngles["xz"]+leftElbowAngles["xz"])
            return leftElbowAngles
        if bodyPart == BodyPart.RIGHT_ELBOW:
            rightShoulderAngles = self.getAnglesForBodyPart(BodyPart.RIGHT_SHOULDER, poseData)
            rightElbowDirectionVector = self.getDirectionVectorForBodypart(BodyPart.RIGHT_SHOULDER, poseData, originBodyPart=BodyPart.RIGHT_ELBOW)
            rightElbowAngles = self.getAnglesFromDirectionVector(rightElbowDirectionVector)
            rightElbowAngles["xy"] = -(rightShoulderAngles["xy"]-rightElbowAngles["xy"])
            rightElbowAngles["yz"] = -(rightShoulderAngles["yz"]-rightElbowAngles["yz"])
            rightElbowAngles["xz"] = -(rightShoulderAngles["xz"]-rightElbowAngles["xz"])
            return rightElbowAngles
        if bodyPart == BodyPart.LEFT_WRIST:
            leftShoulderAngles = self.getAnglesForBodyPart(BodyPart.LEFT_SHOULDER, poseData)
            leftElbowAngles = self.getAnglesForBodyPart(BodyPart.LEFT_ELBOW, poseData)
            leftWristDirectionVector = self.getDirectionVectorForBodypart(BodyPart.LEFT_WRIST, poseData, originBodyPart=BodyPart.LEFT_ELBOW)
            leftWristAngles = self.getAnglesFromDirectionVector(leftWristDirectionVector)
            leftWristAngles["xy"] = leftWristAngles["xy"]-leftElbowAngles["xy"]+leftShoulderAngles["xy"]
            leftWristAngles["yz"] = leftWristAngles["yz"]-leftElbowAngles["yz"]+leftShoulderAngles["yz"]
            leftWristAngles["xz"] = leftWristAngles["xz"]-leftElbowAngles["xz"]+leftShoulderAngles["xz"]
            return leftWristAngles
        if bodyPart == BodyPart.RIGHT_WRIST:
            rightShoulderAngles = self.getAnglesForBodyPart(BodyPart.RIGHT_SHOULDER, poseData)
            rightElbowAngles = self.getAnglesForBodyPart(BodyPart.RIGHT_ELBOW, poseData)
            rightWristDirectionVector = self.getDirectionVectorForBodypart(BodyPart.RIGHT_ELBOW, poseData, originBodyPart=BodyPart.RIGHT_WRIST)
            rightWristAngles = self.getAnglesFromDirectionVector(rightWristDirectionVector)
            rightWristAngles["xy"] = rightWristAngles["xy"]-rightElbowAngles["xy"]-rightShoulderAngles["xy"]
            rightWristAngles["yz"] = rightWristAngles["yz"]-rightElbowAngles["yz"]-rightShoulderAngles["yz"]
            rightWristAngles["xz"] = rightWristAngles["xz"]-rightElbowAngles["xz"]-rightShoulderAngles["xz"]
            return rightWristAngles
    def isSittingUp(self, poseData, threshold=10):
        try:
            leftShoulderAngles = self.getAnglesForBodyPart(BodyPart.LEFT_SHOULDER, poseData)
            if abs(leftShoulderAngles["xy"]) <= threshold:
                return True
            return False
        except:
            return None
    def isTPosing(self, poseData, xyThreshold=15, xzThreshold=20):
        leftElbowAngles = self.getAnglesForBodyPart(BodyPart.LEFT_ELBOW, poseData)
        rightElbowAngles = self.getAnglesForBodyPart(BodyPart.RIGHT_ELBOW, poseData)
        leftWristAngles = self.getAnglesForBodyPart(BodyPart.LEFT_WRIST, poseData)
        rightWristAngles = self.getAnglesForBodyPart(BodyPart.RIGHT_WRIST, poseData)
        try:
            if abs(leftElbowAngles["xy"]) <= xyThreshold and \
               abs(rightElbowAngles["xy"]) <= xyThreshold and \
               abs(leftWristAngles["xy"]) <= xyThreshold and \
               abs(rightWristAngles["xy"]) <= xyThreshold and \
               abs(leftElbowAngles["xz"]) <= xzThreshold and \
               abs(rightElbowAngles["xz"]) <= xzThreshold:
                return True
            return False
        except:
            return None