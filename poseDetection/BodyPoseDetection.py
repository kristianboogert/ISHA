import mediapipe
import math
import cv2

from .BodyPart import *

# TODO: remove body pose jitter!
class BodyPoseDetection:
    ###
    # Public
    ###
    def __init__(self, displayPose=False, visibilityThreshold=0.9):
        self.displayPose = displayPose
        self.visibilityThreshold = visibilityThreshold
        self.mpPose = mediapipe.solutions.pose
        self.pose = self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.draw = mediapipe.solutions.drawing_utils
        self.poseData = None
    def getPose(self, cameraColorFrame):
        cameraColorFrame = cv2.cvtColor(cameraColorFrame, cv2.COLOR_BGR2RGB)
        cameraColorFrame.flags.writeable = False
        self.poseData = self.pose.process(cameraColorFrame)
        cameraColorFrame.flags.writeable = True
        cameraColorFrame = cv2.cvtColor(cameraColorFrame, cv2.COLOR_RGB2BGR)
        return self.poseData
    def drawPose(self, cameraColorFrame, poseData=None):
        if poseData is not None:
            self.draw.draw_landmarks(cameraColorFrame, poseData.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
            return cameraColorFrame
    def getPoseLandmark(self, limb, poseData):
        try:
            return poseData.pose_landmarks.landmark[limb]
        except:
            return None
    def getDirectionVector(self, landmark1, landmark2, visibilityThreshold=0.75):
        if landmark1.visibility > visibilityThreshold and landmark2.visibility > visibilityThreshold:
            return {
                "x": landmark1.x - landmark2.x,
                "y": landmark1.y - landmark2.y,
                "z": landmark1.z - landmark2.z
            }
        return None
    def getDirectionVectorForBodyParts(self, bodyPart, poseData, originBodyPart=None):
        if poseData.pose_landmarks is None:
            return None
        landmarks = poseData.pose_landmarks.landmark
        return self.getDirectionVector(landmarks[bodyPart], landmarks[originBodyPart])
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
            leftShoulderDirectionVector = self.getDirectionVectorForBodyParts(BodyPart.LEFT_SHOULDER, poseData, originBodyPart=BodyPart.RIGHT_SHOULDER)
            leftShoulderAngles = self.getAnglesFromDirectionVector(leftShoulderDirectionVector)
            leftShoulderAngles["xy"] = -leftShoulderAngles["xy"]
            leftShoulderAngles["yz"] = -leftShoulderAngles["yz"]
            leftShoulderAngles["xz"] = -leftShoulderAngles["xz"]
            return leftShoulderAngles
        if bodyPart == BodyPart.RIGHT_SHOULDER:
            rightShoulderDirectionVector = self.getDirectionVectorForBodyParts(BodyPart.LEFT_SHOULDER, poseData, originBodyPart=BodyPart.RIGHT_SHOULDER)
            rightShoulderAngles = self.getAnglesFromDirectionVector(rightShoulderDirectionVector)
            return rightShoulderAngles
        if bodyPart == BodyPart.LEFT_ELBOW:
            leftShoulderAngles = self.getAnglesForBodyPart(BodyPart.LEFT_SHOULDER, poseData)
            leftElbowDirectionVector = self.getDirectionVectorForBodyParts(BodyPart.LEFT_ELBOW, poseData, originBodyPart=BodyPart.LEFT_SHOULDER)
            leftElbowAngles = self.getAnglesFromDirectionVector(leftElbowDirectionVector)
            leftElbowAngles["xy"] = -(leftShoulderAngles["xy"]+leftElbowAngles["xy"])
            leftElbowAngles["yz"] = -(leftShoulderAngles["yz"]+leftElbowAngles["yz"])
            leftElbowAngles["xz"] = -(leftShoulderAngles["xz"]+leftElbowAngles["xz"])
            return leftElbowAngles
        if bodyPart == BodyPart.RIGHT_ELBOW:
            rightShoulderAngles = self.getAnglesForBodyPart(BodyPart.RIGHT_SHOULDER, poseData)
            rightElbowDirectionVector = self.getDirectionVectorForBodyParts(BodyPart.RIGHT_SHOULDER, poseData, originBodyPart=BodyPart.RIGHT_ELBOW)
            rightElbowAngles = self.getAnglesFromDirectionVector(rightElbowDirectionVector)
            try:
                rightElbowAngles["xy"] = -(rightShoulderAngles["xy"]-rightElbowAngles["xy"])
                rightElbowAngles["yz"] = -(rightShoulderAngles["yz"]-rightElbowAngles["yz"])
                rightElbowAngles["xz"] = -(rightShoulderAngles["xz"]-rightElbowAngles["xz"])
                return rightElbowAngles
            except:
                return None
        if bodyPart == BodyPart.LEFT_WRIST:
            leftShoulderAngles = self.getAnglesForBodyPart(BodyPart.LEFT_SHOULDER, poseData)
            leftElbowAngles = self.getAnglesForBodyPart(BodyPart.LEFT_ELBOW, poseData)
            leftWristDirectionVector = self.getDirectionVectorForBodyParts(BodyPart.LEFT_WRIST, poseData, originBodyPart=BodyPart.LEFT_ELBOW)
            leftWristAngles = self.getAnglesFromDirectionVector(leftWristDirectionVector)
            leftWristAngles["xy"] = leftWristAngles["xy"]-leftElbowAngles["xy"]+leftShoulderAngles["xy"]
            leftWristAngles["yz"] = leftWristAngles["yz"]-leftElbowAngles["yz"]+leftShoulderAngles["yz"]
            leftWristAngles["xz"] = leftWristAngles["xz"]-leftElbowAngles["xz"]+leftShoulderAngles["xz"]
            return leftWristAngles
        if bodyPart == BodyPart.RIGHT_WRIST:
            rightShoulderAngles = self.getAnglesForBodyPart(BodyPart.RIGHT_SHOULDER, poseData)
            rightElbowAngles = self.getAnglesForBodyPart(BodyPart.RIGHT_ELBOW, poseData)
            rightWristDirectionVector = self.getDirectionVectorForBodyParts(BodyPart.RIGHT_ELBOW, poseData, originBodyPart=BodyPart.RIGHT_WRIST)
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