from enum import IntEnum

class BodyPartType(IntEnum):
    LEFT_SHOULDER = 0,
    RIGHT_SHOULDER = 1,
    LEFT_UPPER_ARM = 2,
    RIGHT_UPPER_ARM = 3,
    LEFT_FOREARM = 4,
    RIGHT_FOREARM = 5

    @staticmethod
    def serialize(bodyPartType):
        if bodyPartType == BodyPartType.LEFT_SHOULDER:
            return "LEFT_SHOULDER"
        if bodyPartType == BodyPartType.RIGHT_SHOULDER:
            return "RIGHT_SHOULDER"
        if bodyPartType == BodyPartType.LEFT_UPPER_ARM:
            return "LEFT_UPPER_ARM"
        if bodyPartType == BodyPartType.RIGHT_UPPER_ARM:
            return "RIGHT_UPPER_ARM"
        if bodyPartType == BodyPartType.LEFT_FOREARM:
            return "LEFT_FOREARM"
        if bodyPartType == BodyPartType.RIGHT_FOREARM:
            return "RIGHT_FOREARM"

    @staticmethod
    def deserialize(bodyPartTypeString):
        if bodyPartTypeString.upper() == "LEFT_SHOULDER":
            return BodyPartType.LEFT_SHOULDER
        if bodyPartTypeString.upper() == "RIGHT_SHOULDER":
            return BodyPartType.RIGHT_SHOULDER
        if bodyPartTypeString.upper() == "LEFT_UPPER_ARM":
            return BodyPartType.LEFT_UPPER_ARM
        if bodyPartTypeString.upper() == "RIGHT_UPPER_ARM":
            return BodyPartType.RIGHT_UPPER_ARM
        if bodyPartTypeString.upper() == "LEFT_FOREARM":
            return BodyPartType.LEFT_FOREARM
        if bodyPartTypeString.upper() == "RIGHT_FOREARM":
            return BodyPartType.RIGHT_FOREARM