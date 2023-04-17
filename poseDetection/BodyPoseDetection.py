import mediapipe
import math
import cv2

from .BodyPart import *
from .BodyJoint import *

# TODO: remove body pose jitter!
class BodyPoseDetection:
    ###
    # Public
    ###
    def __init__(self, displayPose=False, visibilityThreshold=0.9):
        self.displayPose = displayPose
        self.visibilityThreshold = visibilityThreshold
        self.mpPose = mediapipe.solutions.pose
        self.pose = self.mpPose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6, model_complexity=0)
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
    def getDirectionVectorForBodyJoints(self, bodyPart, poseData, originBodyJoint=None):
        if poseData.pose_landmarks is None:
            return None
        landmarks = poseData.pose_landmarks.landmark
        return self.getDirectionVector(landmarks[bodyPart], landmarks[originBodyJoint])
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
    def isBodyPartVisible(self, bodyPart, poseData, visibilityThreshold=0.85):
        if bodyPart == BodyPart.LEFT_SHOULDER:
            bodyJoint = self.getPoseLandmark(BodyJoint.LEFT_SHOULDER, poseData)
            return (bodyJoint is not None and bodyJoint.visibility > visibilityThreshold)
        if bodyPart == BodyPart.LEFT_UPPER_ARM:
            shoulderBodyJoint = self.getPoseLandmark(BodyJoint.LEFT_SHOULDER, poseData)
            elbowBodyJoint = self.getPoseLandmark(BodyJoint.LEFT_ELBOW, poseData)
            return (shoulderBodyJoint is not None and shoulderBodyJoint.visibility > visibilityThreshold) and \
                   (elbowBodyJoint is not None and elbowBodyJoint.visibility > visibilityThreshold)
        if bodyPart == BodyPart.LEFT_FOREARM:
            elbowBodyJoint = self.getPoseLandmark(BodyJoint.LEFT_ELBOW, poseData)
            wristBodyJoint = self.getPoseLandmark(BodyJoint.LEFT_SHOULDER, poseData)
            return (elbowBodyJoint is not None and elbowBodyJoint.visibility > visibilityThreshold) and \
                   (wristBodyJoint is not None and wristBodyJoint.visibility > visibilityThreshold)
        if bodyPart == BodyPart.RIGHT_SHOULDER:
            bodyJoint = self.getPoseLandmark(BodyJoint.RIGHT_SHOULDER, poseData)
            return (bodyJoint is not None and bodyJoint.visibility > visibilityThreshold)
        if bodyPart == BodyPart.RIGHT_UPPER_ARM:
            shoulderBodyJoint = self.getPoseLandmark(BodyJoint.RIGHT_SHOULDER, poseData)
            elbowBodyJoint = self.getPoseLandmark(BodyJoint.RIGHT_ELBOW, poseData)
            return (shoulderBodyJoint is not None and shoulderBodyJoint.visibility > visibilityThreshold) and \
                   (elbowBodyJoint is not None and elbowBodyJoint.visibility > visibilityThreshold)
        if bodyPart == BodyPart.RIGHT_FOREARM:
            elbowBodyJoint = self.getPoseLandmark(BodyJoint.RIGHT_ELBOW, poseData)
            wristBodyJoint = self.getPoseLandmark(BodyJoint.RIGHT_SHOULDER, poseData)
            return (elbowBodyJoint is not None and elbowBodyJoint.visibility > visibilityThreshold) and \
                   (wristBodyJoint is not None and wristBodyJoint.visibility > visibilityThreshold)
    def getAnglesForBodyJoint(self, bodyJoint, poseData, originBodyJoint=None):
        # if a certain origin is specified, use that origin,
        # otherwise, use a predefined origin
        if originBodyJoint is not None:
            directionVector = self.getDirectionVectorForBodyJoints(bodyJoint, poseData, originBodyJoint)
            angles = self.getAnglesFromDirectionVector(directionVector)
            return angles
        if bodyJoint == BodyJoint.LEFT_SHOULDER:
            leftShoulderDirectionVector = self.getDirectionVectorForBodyJoints(BodyJoint.LEFT_SHOULDER, poseData, originBodyJoint=BodyJoint.RIGHT_SHOULDER)
            leftShoulderAngles = self.getAnglesFromDirectionVector(leftShoulderDirectionVector)
            # leftShoulderAngles["xy"] = -leftShoulderAngles["xy"]
            # leftShoulderAngles["yz"] = -leftShoulderAngles["yz"]
            # leftShoulderAngles["xz"] = -leftShoulderAngles["xz"]
            return leftShoulderAngles
        if bodyJoint == BodyJoint.RIGHT_SHOULDER:
            rightShoulderDirectionVector = self.getDirectionVectorForBodyJoints(BodyJoint.LEFT_SHOULDER, poseData, originBodyJoint=BodyJoint.RIGHT_SHOULDER)
            rightShoulderAngles = self.getAnglesFromDirectionVector(rightShoulderDirectionVector)
            return rightShoulderAngles
        if bodyJoint == BodyJoint.LEFT_ELBOW:
            leftShoulderAngles = self.getAnglesForBodyJoint(BodyJoint.LEFT_SHOULDER, poseData)
            leftElbowDirectionVector = self.getDirectionVectorForBodyJoints(BodyJoint.LEFT_ELBOW, poseData, originBodyJoint=BodyJoint.LEFT_SHOULDER)
            leftElbowAngles = self.getAnglesFromDirectionVector(leftElbowDirectionVector)
            try:
                leftElbowAngles["xy"] = -(leftShoulderAngles["xy"]+leftElbowAngles["xy"])
                leftElbowAngles["yz"] = -(leftShoulderAngles["yz"]+leftElbowAngles["yz"])
                leftElbowAngles["xz"] = -(leftShoulderAngles["xz"]+leftElbowAngles["xz"])
                return leftElbowAngles
            except:
                return None
        if bodyJoint == BodyJoint.RIGHT_ELBOW:
            rightShoulderAngles = self.getAnglesForBodyJoint(BodyJoint.RIGHT_SHOULDER, poseData)
            rightElbowDirectionVector = self.getDirectionVectorForBodyJoints(BodyJoint.RIGHT_SHOULDER, poseData, originBodyJoint=BodyJoint.RIGHT_ELBOW)
            rightElbowAngles = self.getAnglesFromDirectionVector(rightElbowDirectionVector)
            try:
                rightElbowAngles["xy"] = -(rightShoulderAngles["xy"]-rightElbowAngles["xy"])
                rightElbowAngles["yz"] = -(rightShoulderAngles["yz"]-rightElbowAngles["yz"])
                rightElbowAngles["xz"] = -(rightShoulderAngles["xz"]-rightElbowAngles["xz"])
                return rightElbowAngles
            except:
                return None
        if bodyJoint == BodyJoint.LEFT_WRIST:
            leftShoulderAngles = self.getAnglesForBodyJoint(BodyJoint.LEFT_SHOULDER, poseData)
            leftElbowAngles = self.getAnglesForBodyJoint(BodyJoint.LEFT_ELBOW, poseData)
            leftWristDirectionVector = self.getDirectionVectorForBodyJoints(BodyJoint.LEFT_WRIST, poseData, originBodyJoint=BodyJoint.LEFT_ELBOW)
            leftWristAngles = self.getAnglesFromDirectionVector(leftWristDirectionVector)
            try:
                leftWristAngles["xy"] = -(leftWristAngles["xy"]-leftElbowAngles["xy"]+leftShoulderAngles["xy"])
                leftWristAngles["yz"] = -(leftWristAngles["yz"]-leftElbowAngles["yz"]+leftShoulderAngles["yz"])
                leftWristAngles["xz"] = -(leftWristAngles["xz"]-leftElbowAngles["xz"]+leftShoulderAngles["xz"])
                return leftWristAngles
            except:
                return None
        if bodyJoint == BodyJoint.RIGHT_WRIST:
            rightShoulderAngles = self.getAnglesForBodyJoint(BodyJoint.RIGHT_SHOULDER, poseData)
            rightElbowAngles = self.getAnglesForBodyJoint(BodyJoint.RIGHT_ELBOW, poseData)
            rightWristDirectionVector = self.getDirectionVectorForBodyJoints(BodyJoint.RIGHT_ELBOW, poseData, originBodyJoint=BodyJoint.RIGHT_WRIST)
            rightWristAngles = self.getAnglesFromDirectionVector(rightWristDirectionVector)
            try:
                rightWristAngles["xy"] = rightWristAngles["xy"]-rightElbowAngles["xy"]-rightShoulderAngles["xy"]
                rightWristAngles["yz"] = rightWristAngles["yz"]-rightElbowAngles["yz"]-rightShoulderAngles["yz"]
                rightWristAngles["xz"] = rightWristAngles["xz"]-rightElbowAngles["xz"]-rightShoulderAngles["xz"]
                return rightWristAngles
            except:
                return None

    # converter function that takes a body part and returns the right angles using
    # the getAnglesForBodyJoint function. this function is needed, because exerciseScorer.FuglMeyer only knows
    # body parts, but mediapipe only provides body joints.
    def getAnglesForBodyPart(self, bodyPart, poseData):
        if bodyPart == BodyPart.LEFT_SHOULDER:
            return self.getAnglesForBodyJoint(BodyJoint.LEFT_SHOULDER, poseData)
        if bodyPart == BodyPart.RIGHT_SHOULDER:
            return self.getAnglesForBodyJoint(BodyJoint.RIGHT_SHOULDER, poseData)
        if bodyPart == BodyPart.LEFT_UPPER_ARM:
            return self.getAnglesForBodyJoint(BodyJoint.LEFT_ELBOW, poseData)
        if bodyPart == BodyPart.RIGHT_UPPER_ARM:
            return self.getAnglesForBodyJoint(BodyJoint.RIGHT_ELBOW, poseData)
        if bodyPart == BodyPart.LEFT_FOREARM:
            return self.getAnglesForBodyJoint(BodyJoint.LEFT_WRIST, poseData)
        if bodyPart == BodyPart.RIGHT_FOREARM:
            return self.getAnglesForBodyJoint(BodyJoint.RIGHT_WRIST, poseData)

    def getHeightAnglesForBodyPart(self, bodyPart, poseData):
        if bodyPart == BodyPart.LEFT_FOREARM:
            return self.getAnglesForBodyJoint(BodyJoint.LEFT_WRIST, poseData, BodyJoint.LEFT_SHOULDER)
        if bodyPart == BodyPart.RIGHT_FOREARM:
            return self.getAnglesForBodyJoint(BodyJoint.RIGHT_WRIST, poseData, BodyJoint.RIGHT_SHOULDER)
        return None # the bodypart is not relevent for this project,
                    # or should not be checked, like the upper arm.

    def isSittingUp(self, poseData, threshold=10):
        try:
            leftShoulderAngles = self.getAnglesForBodyPart(BodyJoint.LEFT_SHOULDER, poseData)
            if abs(leftShoulderAngles["xy"]) <= threshold:
                return True
            return False
        except:
            return None
    def isTPosing(self, poseData, xyThreshold=15, xzThreshold=20):
        leftElbowAngles = self.getAnglesForBodyPart(BodyJoint.LEFT_ELBOW, poseData)
        rightElbowAngles = self.getAnglesForBodyPart(BodyJoint.RIGHT_ELBOW, poseData)
        leftWristAngles = self.getAnglesForBodyPart(BodyJoint.LEFT_WRIST, poseData)
        rightWristAngles = self.getAnglesForBodyPart(BodyJoint.RIGHT_WRIST, poseData)
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
