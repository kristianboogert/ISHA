from math import atan2, degrees
from .BodyPartType import *

class BodyPart:
    def __init__(self, bodyPartTypeString, originBodyJoint, targetBodyJoint):
        self.bodyPartType = BodyPartType.deserialize(bodyPartTypeString)
        self.originBodyJoint = originBodyJoint
        self.heading = None
        if originBodyJoint is not None and targetBodyJoint is not None:
            self.heading = BodyPart._calculateHeading(originBodyJoint, targetBodyJoint)
    def getBodyPartType(self):
        return BodyPartType.serialize(self.bodyPartType)
    def getOriginBodyJoint(self):
        return self.originBodyJoint
    def getHeading(self):
        return self.heading
    def compare(self, otherBodyPart):
        # define a difference variable, indicating the difference between the two BodyPoses
        difference = {}
        difference.update({"position_diff": None})
        difference.update({"angle_diff": None})
        # make sure both BodyParts share the same originBodyJoint and bodyPartType
        if self.getOriginBodyJoint().getBodyJointType() == otherBodyPart.getOriginBodyJoint().getBodyJointType() and \
           self.getBodyPartType() == otherBodyPart.getBodyPartType():
            # get differnce between BodyParts.OriginBodyJoint.position
            x_diff = self.getOriginBodyJoint().getPosition()["x"] - otherBodyPart.getOriginBodyJoint().getPosition()["x"]
            y_diff = self.getOriginBodyJoint().getPosition()["y"] - otherBodyPart.getOriginBodyJoint().getPosition()["y"]
            z_diff = self.getOriginBodyJoint().getPosition()["z"] - otherBodyPart.getOriginBodyJoint().getPosition()["z"]
            difference.update({"position_diff": {"x": x_diff, "y": y_diff, "z": z_diff}})
            # get difference between BodyParts.heading
            xy_diff = self._getAngleDiff(self.getHeading()["xy"], otherBodyPart.getHeading()["xy"])
            yz_diff = self._getAngleDiff(self.getHeading()["yz"], otherBodyPart.getHeading()["yz"])
            xz_diff = self._getAngleDiff(self.getHeading()["xz"], otherBodyPart.getHeading()["xz"])
            difference.update({"angle_diff": {"xy": xy_diff, "yz": yz_diff, "xz": xz_diff}})
        else:
            print("BodyParts do not match")
        return difference
    @staticmethod
    def _calculateHeading(originBodyJoint, targetBodyJoint):
        # get direction vector between the two joints
        directionVector = {}
        directionVector.update({"x": originBodyJoint.getPosition()["x"] - targetBodyJoint.getPosition()["x"]})
        directionVector.update({"y": originBodyJoint.getPosition()["y"] - targetBodyJoint.getPosition()["y"]})
        directionVector.update({"z": originBodyJoint.getPosition()["z"] - targetBodyJoint.getPosition()["z"]})
        # calculate angles based on the directionVector
        x, y, z = directionVector["x"], directionVector["y"], directionVector["z"]
        xyAngle = degrees(atan2(y,x))
        yzAngle = degrees(atan2(z,y))
        xzAngle = degrees(atan2(z,x))
        # return angles
        return {
            "xy": xyAngle,
            "yz": yzAngle,
            "xz": xzAngle
        }
    def _getAngleDiff(self, angle1, angle2):
        # get difference
        diff = round(angle1-angle2)
        # remove any full rotations from the difference
        while diff > 360:
            diff-=360
        while diff < -360:
            diff+=360
        # make sure the difference is never greater than 180
        if diff > 180:
            diff = -360+diff
        if diff < -180:
            diff = 360+diff
        # return difference
        return diff
