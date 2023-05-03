from enum import IntEnum

class BodyPartDescriptionType(IntEnum):
    SHOULDER = 0,     # LEFT/RIGHT_SHOULDER in poseDetection.BodyPart
    UPPER_ARM = 2,    # LEFT/RIGHT_UPPER_ARM in poseDetection.BodyPart
    FOREARM = 4,      # LEFT/RIGHT_WRIST in poseDetection.BodyPart
    @staticmethod
    def serialize(bodyPartDescriptionType):
        if bodyPartDescriptionType.upper() == BodyPartDescriptionType.SHOULDER:
            return "SHOULDER"
        if bodyPartDescriptionType.upper() == BodyPartDescriptionType.UPPER_ARM:
            return "UPPER_ARM"
        if bodyPartDescriptionType.upper() == BodyPartDescriptionType.FOREARM:
            return "FOREARM"
    @staticmethod
    def deserialize(bodyPartDescriptionTypeString):
        if bodyPartDescriptionTypeString.upper() == "SHOULDER":
            return BodyPartDescriptionType.SHOULDER
        if bodyPartDescriptionTypeString.upper() == "UPPER_ARM":
            return BodyPartDescriptionType.UPPER_ARM
        if bodyPartDescriptionTypeString.upper() == "FOREARM":
            return BodyPartDescriptionType.FOREARM