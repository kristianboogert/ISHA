from .BodyJointType import *

class BodyJoint:
    def __init__(self, bodyJointTypeString, position):
        self.bodyJointType = None
        self.position = None
        self.setBodyJointType(bodyJointTypeString)
        self.setPosition(position)
    def getBodyJointType(self):
        return BodyJointType.serialize(self.bodyJointType)
    def setBodyJointType(self, bodyJointTypeString):
        self.bodyJointType = BodyJointType.deserialize(bodyJointTypeString)
    def getPosition(self):
        return self.position
    def setPosition(self, position):
        self.position = position
    @staticmethod
    def createFromLandmark(bodyJointTypeString, landmark, visibilityThreshold=0.9):
        if landmark.visibility >= visibilityThreshold:
            x, y, z = landmark.x, landmark.y, landmark.z
            return BodyJoint(bodyJointTypeString, {"x": x, "y": y, "z": z})
        return None
