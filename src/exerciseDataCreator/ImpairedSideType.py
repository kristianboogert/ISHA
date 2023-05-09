from enum import IntEnum

class ImpairedSideType(IntEnum):
    LEFT = 0,
    RIGHT = 1
    @staticmethod
    def serialize(impairedSideType):
        if impairedSideType == ImpairedSideType.LEFT:
            return "LEFT"
        if impairedSideType == ImpairedSideType.RIGHT:
            return "RIGHT"