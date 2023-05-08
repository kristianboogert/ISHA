from enum import IntEnum

class HandPartType(IntEnum):
    PINKY_BASE = 0,
    PINKY_TIP = 1,
    RING_FINGER_BASE = 2,
    RING_FINGER_TIP = 3,
    MIDDLE_FINGER_BASE = 4,
    MIDDLE_FINGER_TIP = 5,
    INDEX_FINGER_BASE = 6,
    INDEX_FINGER_TIP = 7,
    THUMB_BASE = 8,
    THUMB_TIP = 9

    @staticmethod
    def deserialize(handPartTypeString):
        if handPartTypeString.upper() == "PINKY_BASE" or handPartTypeString.upper() == "PINKY":
            return HandPartType.PINKY_BASE
        if handPartTypeString.upper() == "RING_FINGER_BASE" or handPartTypeString.upper() == "RING_FINGER":
            return HandPartType.RING_FINGER_BASE
        if handPartTypeString.upper() == "MIDDLE_FINGER_BASE" or handPartTypeString.upper() == "MIDDLE_FINGER":
            return HandPartType.MIDDLE_FINGER_BASE
        if handPartTypeString.upper() == "INDEX_FINGER_BASE" or handPartTypeString.upper() == "INDEX_FINGER":
            return HandPartType.INDEX_FINGER_BASE
        if handPartTypeString.upper() == "THUMB_BASE" or handPartTypeString.upper() == "THUMB":
            return HandPartType.THUMB_BASE
        if handPartTypeString.upper() == "PINKY_TIP":
            return HandPartType.PINKY_TIP
        if handPartTypeString.upper() == "RING_FINGER_TIP":
            return HandPartType.RING_FINGER_TIP
        if handPartTypeString.upper() == "MIDDLE_FINGER_TIP":
            return HandPartType.MIDDLE_FINGER_TIP
        if handPartTypeString.upper() == "INDEX_FINGER_TIP":
            return HandPartType.INDEX_FINGER_TIP
        if handPartTypeString.upper() == "THUMB_TIP":
            return HandPartType.THUMB_TIP