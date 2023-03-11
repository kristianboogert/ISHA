import mediapipe
import math
from enum import IntEnum
import cv2

class BodyPart(IntEnum):
    NOSE = 0,
    LEFT_EYE_INNER = 1,
    LEFT_EYE = 2,
    LEFT_EYE_OUTER = 3,
    RIGHT_EYE_INNER = 4,
    RIGHT_EYE = 5,
    RIGHT_EYE_OUTER = 6,
    LEFT_EAR = 7,
    RIGHT_EAR = 8,
    MOUTH_LEFT = 9,
    MOUTH_RIGHT = 10,
    LEFT_SHOULDER = 11,
    RIGHT_SHOULDER = 12,
    LEFT_ELBOW = 13,
    RIGHT_ELBOW = 14,
    LEFT_WRIST = 15,
    RIGHT_WRIST = 16,
    LEFT_PINKY = 17,
    RIGHT_PINKY = 18,
    LEFT_INDEX = 19,
    RIGHT_INDEX = 20,
    LEFT_THUMB = 21,
    RIGHT_THUMB = 22,
    LEFT_HIP = 23,
    RIGHT_HIP = 24,
    LEFT_KNEE = 25,
    RIGHT_KNEE = 26,
    LEFT_ANKLE = 27,
    RIGHT_ANKLE = 28,
    LEFT_HEEL = 29,
    RIGHT_HEEL = 30,
    LEFT_FOOT_INDEX = 31,
    RIGHT_FOOT_INDEX = 32

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
            leftShoulderDirectionVector = self.getDirectionVectorForBodypart(bodyPart, poseData, originBodyPart=BodyPart.RIGHT_SHOULDER)
            leftShoulderAngles = self.getAnglesFromDirectionVector(leftShoulderDirectionVector)
            leftShoulderAngles["xy"] = -leftShoulderAngles["xy"]
            return leftShoulderAngles
        if bodyPart == BodyPart.RIGHT_SHOULDER:
            rightShoulderDirectionVector = self.getDirectionVectorForBodypart(BodyPart.LEFT_SHOULDER, poseData, originBodyPart=bodyPart)
            rightShoulderAngles = self.getAnglesFromDirectionVector(rightShoulderDirectionVector)
            return rightShoulderAngles
        if bodyPart == BodyPart.LEFT_ELBOW:
            leftShoulderAngles = self.getAnglesForBodyPart(BodyPart.LEFT_SHOULDER, poseData)
            leftElbowDirectionVector = self.getDirectionVectorForBodypart(bodyPart, poseData, originBodyPart=BodyPart.LEFT_SHOULDER)
            leftElbowAngles = self.getAnglesFromDirectionVector(leftElbowDirectionVector)
            leftElbowAngles["xy"] = leftShoulderAngles["xy"]+leftElbowAngles["xy"]
            return leftElbowAngles
        if bodyPart == BodyPart.RIGHT_ELBOW:
            rightShoulderAngles = self.getAnglesForBodyPart(BodyPart.RIGHT_SHOULDER, poseData)
            rightElbowDirectionVector = self.getDirectionVectorForBodypart(bodyPart, poseData, originBodyPart=BodyPart.RIGHT_SHOULDER)
            rightElbowAngles = self.getAnglesFromDirectionVector(rightElbowDirectionVector)
            rightElbowAngles["xy"] = self.correctAngle(rightElbowAngles["xy"])
            rightElbowAngles["xy"] = -(rightShoulderAngles["xy"] - rightElbowAngles["xy"])
            return rightElbowAngles
        if bodyPart == BodyPart.LEFT_WRIST:
            leftElbowAngles = self.getAnglesForBodyPart(BodyPart.LEFT_ELBOW, poseData)
            leftWristDirectionVector = self.getDirectionVectorForBodypart(bodyPart, poseData, originBodyPart=BodyPart.LEFT_ELBOW)
            leftWristAngles = self.getAnglesFromDirectionVector(leftWristDirectionVector)
            leftWristAngles["xy"] = -(leftElbowAngles["xy"]+leftWristAngles["xy"])
            return leftWristAngles
        if bodyPart == BodyPart.RIGHT_WRIST:
            rightElbowAngles = self.getAnglesForBodyPart(BodyPart.RIGHT_ELBOW, poseData)
            print("RIGHT ELBOW:", rightElbowAngles["xy"])
            rightWristDirectionVector = self.getDirectionVectorForBodypart(bodyPart, poseData, originBodyPart=BodyPart.RIGHT_ELBOW)
            rightWristAngles = self.getAnglesFromDirectionVector(rightWristDirectionVector)
            rightWristAngles["xy"] = self.correctAngle(rightWristAngles["xy"])
            rightWristAngles["xy"] = rightWristAngles["xy"]-rightElbowAngles["xy"]
            return rightWristAngles
    def correctAngle(self, angle):
        if angle <= 180 and angle >= 0:
            return -(180-angle)
        if angle >= -180:
            return 180+angle
    def isSittingUp(self, poseData, threshold=10):
        try:
            leftShoulderAngles = self.getAnglesForBodyPart(BodyPart.LEFT_SHOULDER, poseData)
            if abs(leftShoulderAngles["xy"]) <= threshold:
                return True
            return False
        except:
            return None
    def isTPosing(self, poseData, threshold=10):
        try:
            leftWristAngles = self.getAnglesForBodyPart(BodyPart.LEFT_WRIST, poseData)
            rightwristAngles = self.getAnglesForBodyPart(BodyPart.RIGHT_WRIST, poseData)
            if abs(leftWristAngles["xy"]) <= threshold and abs(rightWristAngles["xy"]) <= threshold:
                return True
            return False
        except:
            return None