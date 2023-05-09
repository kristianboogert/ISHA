from enum import IntEnum

class PoseDetectionType(IntEnum):
    BODY_POSE = 0,
    HAND_POSE = 1
    @staticmethod
    def serialize(poseDetectionType):
        if poseDetectionType.upper() == PoseDetectionType.BODY_POSE:
            return "BODY_POSE"
        if poseDetectionType.upper() == PoseDetectionType.HAND_POSE:
            return "HAND_POSE"
    @staticmethod
    def deserialize(self, poseDetectionTypeString):
        if poseDetectionTypeString.upper() == "BODY_POSE":
            return self.BODY_POSE
        if poseDetectionTypeString.upper() == "HAND_POSE":
            return self.HAND_POSE