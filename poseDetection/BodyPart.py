from enum import IntEnum

class BodyPart(IntEnum):
    LEFT_SHOULDER = 0,
    RIGHT_SHOULDER = 1,
    LEFT_UPPER_ARM = 2,
    RIGHT_UPPER_ARM = 3,
    LEFT_FOREARM = 4,
    RIGHT_FOREARM = 5

    def serialize(self, bodyPart):
        if bodyPart == self.LEFT_SHOULDER:
            return "LEFT_SHOULDER"
        if bodyPart == self.RIGHT_SHOULDER:
            return "RIGHT_SHOULDER"
        if bodyPart == self.LEFT_UPPER_ARM:
            return "LEFT_UPPER_ARM"
        if bodyPart == self.RIGHT_UPPER_ARM:
            return "RIGHT_UPPER_ARM"
        if bodyPart == self.LEFT_FOREARM:
            return "LEFT_FOREARM"
        if bodyPart == self.RIGHT_FOREARM:
            return "RIGHT_FOREARM"

