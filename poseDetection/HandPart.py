from math import atan2, degrees
from .HandType import HandType
from .HandPartType import HandPartType
from .HandJoint import HandJoint
from .HandJointType import HandJointType

class HandPart:
    def __init__(self, originHandJoint, targetHandJoint, handPartType):
        self.handType = originHandJoint.getHandType()
        self.handPartType = handPartType
        self.originHandJoint = originHandJoint
        self.targetHandJoint = targetHandJoint
        self.heading = HandPart._calculateHeading(originHandJoint, targetHandJoint)
    @staticmethod
    def createFromLandmarks(handPoseData, handType, handPartType):
        try:
            originHandJointType, targetHandJointType = HandPart._findHandJointTypes(handType)
            originHandJoint = HandJoint.createFromLandmarks(handType, originHandJointType, handPoseData)
            targetHandJoint = HandJoint.createFromLandmarks(handType, targetHandJointType, handPoseData)
            return HandPart(originHandJoint, targetHandJoint, handPartType)
        except:
            return None
    def getHandType(self):
        return self.handType
    def getHandPartType(self):
        return self.handPartType
    def getOriginHandJoint(self):
        return self.originHandJoint
    def getTargetHandJoint(self):
        return self.originHandJoint
    def getHeading(self):
        return self.heading
    @staticmethod
    def _findHandJointTypes(handPartType):
        if handPartType == HandPartType.PINKY_BASE:
            return HandJointType.PINKY_MCP, HandJointType.PINKY_PIP
        if handPartType == HandPartType.PINKY_TIP:
            return HandJointType.PINKY_DIP, HandJointType.PINKY_TIP
    @staticmethod
    def _calculateHeading(originHandJoint, targetHandJoint):
        # make sure we're looking at the same hand first
        if originHandJoint.getHandType() == targetHandJoint.getHandType():
            # get direction vector between the two joints
            directionVector = {}
            directionVector.update({"x": originHandJoint.getPosition()["x"] - targetHandJoint.getPosition()["x"]})
            directionVector.update({"y": originHandJoint.getPosition()["y"] - targetHandJoint.getPosition()["y"]})
            directionVector.update({"z": originHandJoint.getPosition()["z"] - targetHandJoint.getPosition()["z"]})
            # calculate angles based on the directionVector
            x, y, z = directionVector["x"], directionVector["y"], directionVector["z"]
            xyAngle = degrees(atan2(y,x))
            yzAngle = degrees(atan2(z,y))
            xzAngle = degrees(atan2(z,x))
            # if the left side is calculated, make sure to correct some angles
            if originHandJoint.getHandJointType() == HandType.LEFT_HAND:
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