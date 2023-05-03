from enum import IntEnum

class ImpairedSideType(IntEnum):
    LEFT = 0,
    RIGHT = 1
    @staticmethod
    def serialize(impairedSideType):
        if impairedSideType == ImpairedSideTypeType.LEFT:
            return "LEFT"
        if impairedSideType == ImpairedSideTypeType.RIGHT:
            return "RIGHT"