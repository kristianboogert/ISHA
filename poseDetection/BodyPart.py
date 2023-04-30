from math import atan2, degrees
from .BodyPartType import *
from .BodyJointType import *
from .BodyJoint import BodyJoint

class BodyPart:
    def __init__(self, bodyPartTypeString, originBodyJoint, targetBodyJoint):
        self.bodyPartType = BodyPartType.deserialize(bodyPartTypeString)
        self.originBodyJoint = originBodyJoint
        self.heading = None
        if originBodyJoint is not None and targetBodyJoint is not None:
            self.heading = BodyPart._calculateHeading(originBodyJoint, targetBodyJoint)
    @staticmethod
    def createFromLandmarks(poseLandmarks, bodyPartTypeString, landmarkVisibilityThreshold=0.75):
        originBodyJointType, targetBodyJointType = BodyPart._findBodyJointTypes(bodyPartTypeString)
        # find both joints in landmarks
        try:
            originBodyJointLandmark = poseLandmarks.pose_landmarks.landmark[originBodyJointType]
            targetBodyJointLandmark = poseLandmarks.pose_landmarks.landmark[targetBodyJointType]
            originBodyJoint = BodyJoint.createFromLandmark(BodyJointType.serialize(originBodyJointType), originBodyJointLandmark)
            targetBodyJoint = BodyJoint.createFromLandmark(BodyJointType.serialize(targetBodyJointType), targetBodyJointLandmark)
            if originBodyJointLandmark.visibility > landmarkVisibilityThreshold and targetBodyJointLandmark.visibility > landmarkVisibilityThreshold:
                return BodyPart(bodyPartTypeString, originBodyJoint, targetBodyJoint)
        except:
            return None
    def getBodyPartType(self):
        return self.bodyPartType
    def getBodyPartTypeString(self):
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
    def _findBodyJointTypes(bodyPartTypeString):
        if bodyPartTypeString.upper() == "LEFT_SHOULDER":
            return BodyJointType.deserialize("LEFT_SHOULDER"), BodyJointType.deserialize("RIGHT_SHOULDER")
        if bodyPartTypeString.upper() == "RIGHT_SHOULDER":
            return BodyJointType.deserialize("RIGHT_SHOULDER"), BodyJointType.deserialize("LEFT_SHOULDER")
        if bodyPartTypeString.upper() == "LEFT_UPPER_ARM":
            return BodyJointType.deserialize("LEFT_ELBOW"), BodyJointType.deserialize("LEFT_SHOULDER")
        if bodyPartTypeString.upper() == "RIGHT_UPPER_ARM":
            return BodyJointType.deserialize("RIGHT_SHOULDER"), BodyJointType.deserialize("RIGHT_ELBOW")
        if bodyPartTypeString.upper() == "LEFT_FOREARM":
            return BodyJointType.deserialize("LEFT_WRIST"), BodyJointType.deserialize("LEFT_ELBOW")
        if bodyPartTypeString.upper() == "RIGHT_FOREARM":
            return BodyJointType.deserialize("RIGHT_ELBOW"), BodyJointType.deserialize("RIGHT_WRIST")
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
        # if the left side is calculated, make sure to correct some angles
        if "LEFT" in originBodyJoint.getBodyJointType().upper():
            xyAngle*=-1
            yzAngle+=180
        # return angles
        return {
            "xy": xyAngle,
            "yz": yzAngle,
            "xz": xzAngle
        }
    @staticmethod
    def getAngleDiff(angle1, angle2):
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
