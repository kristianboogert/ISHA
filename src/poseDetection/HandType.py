from enum import IntEnum

class HandType(IntEnum):
    LEFT_HAND = 0,
    RIGHT_HAND = 1

    @staticmethod
    def deserialize(handTypeString):
        if handTypeString.upper() == "LEFT_HAND":
            return HandType.LEFT_HAND
        if handTypeString.upper() == "RIGHT_HAND":
            return HandType.RIGHT_HAND
    
    @staticmethod
    def serialize(handType):
        if handType == HandType.LEFT_HAND:
            return "LEFT_HAND"
        if handType == HandType.RIGHT_HAND:
            return "RIGHT_HAND"