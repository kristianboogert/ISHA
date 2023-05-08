from math import degrees, radians, acos, dist, atan2
from time import time
from .HandType import HandType
from .HandPartType import HandPartType
from .HandPart import HandPart

class HandPose:
    def __init__(self):
        self.handPose = []
        self.clear()
    def clear(self):
        self.handPose = []
    def getBodyPose(self):
        return self.handPose
    def createPose(self, poseLandmarks, handTypeString, relevantHandPartTypeStrings):
        self.clear()
        for handPartTypeString in relevantHandPartTypeStrings:
            handPart = HandPart.createFromLandmarks(poseLandmarks, HandType.deserialize(handTypeString), HandPartType.deserialize(handPartTypeString))
            if handPart is not None:
                self.handPose.append({
                    "hand": handTypeString,
                    "hand_part": handPart.getHandPartType(),
                    "origin": handPart.getOriginHandJoint().getPosition(),
                    "heading": handPart.getHeading(),
                    "timestamp": round(time()*1000)
                })
        # store hand rotation as well
        try:
            indexFinger = HandPart.createFromLandmarks(poseLandmarks, HandType.deserialize(handTypeString), HandPartType.deserialize("INDEX_FINGER"))
            ringFinger = HandPart.createFromLandmarks(poseLandmarks, HandType.deserialize(handTypeString), HandPartType.deserialize("RING_FINGER"))
            indexFingerOriginHandJoint = indexFinger.getOriginHandJoint().getPosition()
            ringFingerOriginHandJoint = ringFinger.getOriginHandJoint().getPosition()
            if handTypeString.upper() == "LEFT_HAND":
                delta_y = ringFingerOriginHandJoint["y"]-indexFingerOriginHandJoint["y"]
                delta_x = ringFingerOriginHandJoint["x"]-indexFingerOriginHandJoint["x"]
                xyAngle = degrees(atan2(delta_y, delta_x))
                self.handPose.append({
                    "hand_rotation_xy": xyAngle
                })
            if handTypeString.upper() == "RIGHT_HAND":
                delta_y = indexFingerOriginHandJoint["y"]-ringFingerOriginHandJoint["y"]
                delta_x = indexFingerOriginHandJoint["x"]-ringFingerOriginHandJoint["x"]
                xyAngle = degrees(atan2(delta_y, delta_x))
                self.handPose.append({
                    "hand_rotation_xy": -xyAngle
                })
        except:
            pass
        return self.handPose
    def getHandRotation(self, handPartType):
        return handPartType.getHeading()
    @staticmethod
    def getDiffs(handPose, otherBodyPose):
        diffs = []
        for item in handPose:
            # find the same item in otherBodyPose
            for otherItem in otherBodyPose:
                if item["hand_part"] == otherItem["hand_part"]:
                    diffs.append({
                        "hand_part": item["hand_part"],
                        "origin": {
                            "x": round(otherItem["origin"]["x"] - item["origin"]["x"]),
                            "y": round(otherItem["origin"]["y"] - item["origin"]["y"]),
                            "z": round(otherItem["origin"]["z"] - item["origin"]["z"])
                        },
                        "heading": {
                            "xy": HandPart.getAngleDiff(otherItem["heading"]["xy"], item["heading"]["xy"]),
                            "yz": HandPart.getAngleDiff(otherItem["heading"]["yz"], item["heading"]["yz"]),
                            "xz": HandPart.getAngleDiff(otherItem["heading"]["xz"], item["heading"]["xz"])
                        }
                    })
        return diffs