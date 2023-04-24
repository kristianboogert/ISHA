import json
from enum import IntEnum

class BodyJointType(IntEnum):
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

    @staticmethod
    def serialize(bodyJoint):
        if bodyJoint == BodyJointType.LEFT_SHOULDER:
            return "LEFT_SHOULDER"
        if bodyJoint == BodyJointType.RIGHT_SHOULDER:
            return "RIGHT_SHOULDER"
        if bodyJoint == BodyJointType.LEFT_ELBOW:
            return "LEFT_ELBOW"
        if bodyJoint == BodyJointType.RIGHT_ELBOW:
            return "RIGHT_ELBOW"
        if bodyJoint == BodyJointType.LEFT_WRIST:
            return "LEFT_WRIST"
        if bodyJoint == BodyJointType.RIGHT_WRIST:
            return "RIGHT_WRIST"
    @staticmethod
    def deserialize(bodyJointString):
        if bodyJointString.upper() == "LEFT_SHOULDER":
            return BodyJointType.LEFT_SHOULDER
        if bodyJointString.upper() == "RIGHT_SHOULDER":
            return BodyJointType.RIGHT_SHOULDER
        if bodyJointString.upper() == "LEFT_ELBOW":
            return BodyJointType.LEFT_ELBOW
        if bodyJointString.upper() == "RIGHT_ELBOW":
            return BodyJointType.RIGHT_ELBOW
        if bodyJointString.upper() == "LEFT_WRIST":
            return BodyJointType.LEFT_WRIST
        if bodyJointString.upper() == "RIGHT_WRIST":
            return BodyJointType.RIGHT_WRIST
