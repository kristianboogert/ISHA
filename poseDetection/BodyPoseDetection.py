import mediapipe
import math
import cv2

from .BodyPart import *
from .BodyJoint import *

class BodyPoseDetection:
    ###
    # Public
    ###
    def __init__(self):
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
    def _getPoseLandmark(self, bodyJointType, bodyPoseData):
        try:
            return bodyPoseData.pose_landmarks.landmark[bodyJointType]
        except:
            return None
    @staticmethod
    def isBodyPartVisible(bodyPartType, bodyPoseData, landmarkVisibilityThreshold=0.85):
        # If a body part can be created from a given set of landmarks, it is considered visible
        bodyPartTypeString = BodyPartType.serialize(bodyPartType)
        bodyPart = BodyPart.createFromLandmarks(bodyPoseData, bodyPartTypeString, landmarkVisibilityThreshold=landmarkVisibilityThreshold)
        return (bodyPart is not None)
    @staticmethod
    def getAnglesForBodyPart(bodyPartType, bodyPoseData):
        bodyPartTypeString = BodyPartType.serialize(bodyPartType)
        bodyPart = BodyPart.createFromLandmarks(bodyPoseData, bodyPartTypeString)
        return bodyPart.getHeading()