import mediapipe
import math
import cv2

from .BodyPart import *
from .BodyJoint import *

# TODO: FUGL-MEYER MOET BIJGEWERKT WORDEN: ONDER ANDERE MOET ER PER OEFENING-PART EEN NEUTRALPOSE KOMEN!

# TODO: IMPLEMENTEER EEN USER_HAS_MOVED()-ACHTIGE FUNCTIE, BODYPARTS VERGELIJKEN GAAT NU GOED GENOEG!
# TODO: FIX DE FUGL MEYER CLASS ZODAT HIJ MET DE NIEUWE POSE DETECTIE KAN OMGAAN!!!!!!!!!!!!!!!!!!!!!
# TODO: ZORG ERVOOR DAT ER EEN COMPARE() FUNCTIE KOMT IN DE BODYPOSE CLASS! DOEL: ZONDER VEEL MOEITE TWEE BODY PARTS VERGELIJKEN!!!!!! EEN BODYPART CLASS HEEFT AL EEN WERKENDE COMPARE() FUNCTIE!!!!!
# TODO: FIX DE EXCEL EXPORTER ZODAT HIJ MET EEN NIEUWE BODY POSE OVERWEG KAN! DOEL: DIEPTE TESTEN!!!!
# TODO: DOE ALLE HAND DETECTIE OOK HERSCHRIJVEN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class BodyPoseDetection:
    ###
    # Public
    ###
    def __init__(self, displayPose=False, visibilityThreshold=0.9):
        self.displayPose = displayPose
        self.visibilityThreshold = visibilityThreshold
        self.mpPose = mediapipe.solutions.pose
        self.pose = self.mpPose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6, model_complexity=0)
        # self.draw = mediapipe.solutions.drawing_utils # disabled, since the pi 4 does not like this
        self.poseData = None
    def getPose(self, cameraFrame):
        cameraFrame = cv2.cvtColor(cameraFrame, cv2.COLOR_BGR2RGB)
        cameraFrame.flags.writeable = False
        self.poseData = self.pose.process(cameraFrame)
        cameraFrame.flags.writeable = True
        cameraFrame = cv2.cvtColor(cameraFrame, cv2.COLOR_RGB2BGR)
        return self.poseData
    def _getPoseLandmark(self, limb, poseData):
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
    def drawPose(self, cameraFrame, poseData=None):
        if poseData is not None:
            # self.draw.draw_landmarks(cameraFrame, poseData.pose_landmarks, self.mpPose.POSE_CONNECTIONS) # disabled, since the pi 4 does not like this
            return cameraFrame
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
    def isBodyPartVisible(self, bodyPartType, poseLandmarks, landmarkVisibilityThreshold=0.85):
        # If a body part can be created from a given set of landmarks, it is considered visible
        bodyPartTypeString = BodyPartType.serialize(bodyPartType)
        bodyPart = BodyPart.createFromLandmarks(poseLandmarks, bodyPartTypeString, landmarkVisibilityThreshold=landmarkVisibilityThreshold)
        return (bodyPart is not None)
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
    def getAnglesForBodyPart(self, bodyPartType, poseLandmarks):
        bodyPartTypeString = BodyPartType.serialize(bodyPartType)
        bodyPart = BodyPart.createFromLandmarks(poseLandmarks, bodyPartTypeString)
        return bodyPart.getHeading()





















    # def isSittingUp(self, poseData, threshold=10):
    #     try:
    #         leftShoulderAngles = self.getAnglesForBodyPart(BodyJoint.LEFT_SHOULDER, poseData)
    #         if abs(leftShoulderAngles["xy"]) <= threshold:
    #             return True
    #         return False
    #     except:
    #         return None
    # def isTPosing(self, poseData, xyThreshold=15, xzThreshold=20):
    #     leftElbowAngles = self.getAnglesForBodyPart(BodyJoint.LEFT_ELBOW, poseData)
    #     rightElbowAngles = self.getAnglesForBodyPart(BodyJoint.RIGHT_ELBOW, poseData)
    #     leftWristAngles = self.getAnglesForBodyPart(BodyJoint.LEFT_WRIST, poseData)
    #     rightWristAngles = self.getAnglesForBodyPart(BodyJoint.RIGHT_WRIST, poseData)
    #     try:
    #         if abs(leftElbowAngles["xy"]) <= xyThreshold and \
    #            abs(rightElbowAngles["xy"]) <= xyThreshold and \
    #            abs(leftWristAngles["xy"]) <= xyThreshold and \
    #            abs(rightWristAngles["xy"]) <= xyThreshold and \
    #            abs(leftElbowAngles["xz"]) <= xzThreshold and \
    #            abs(rightElbowAngles["xz"]) <= xzThreshold:
    #             return True
    #         return False
    #     except:
    #         return None
