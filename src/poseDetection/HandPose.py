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
    def getHandPose(self):
        return self.handPose
    def _isHandInView(self, poseLandmarks, handTypeString):
        # track both visibilities, because the landmarks index might be swapped
        leftHandInView = False
        rightHandInView = False
        foundAtIndex = 0
        # Hand pose detection can work without mirrored input frames, but hand pose cannot.
        # therefor, if a user wants to see if the hand is in view, we ask for the opposite hand.
        # another solution would be to mirror the input frame, but this takes more cpu%.
        # also, if there are two hands in view, their index is swapped for whatever reason.
        if poseLandmarks.multi_handedness is not None:
            for hand in poseLandmarks.multi_handedness:
                label = hand.classification[0].label
                index = hand.classification[0].index
                if label == "Left" and handTypeString == "RIGHT_HAND": # this is no mistake
                        return True, foundAtIndex
                if label == "Right" and handTypeString == "LEFT_HAND": # this is also no mistake
                        return True, foundAtIndex
                foundAtIndex+=1
        return False, None
    def createPose(self, poseLandmarks, handTypeString, relevantHandPartTypeStrings):
        self.clear()
        isHandVisible, handLandmarksIndex = self._isHandInView(poseLandmarks, handTypeString)
        if isHandVisible == True:
            for handPartTypeString in relevantHandPartTypeStrings:
                handPart = HandPart.createFromLandmarks(poseLandmarks, HandType.deserialize(handTypeString), HandPartType.deserialize(handPartTypeString), handLandmarksIndex)
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
                indexFinger = HandPart.createFromLandmarks(poseLandmarks, HandType.deserialize(handTypeString), HandPartType.deserialize("INDEX_FINGER"), handLandmarksIndex)
                ringFinger = HandPart.createFromLandmarks(poseLandmarks, HandType.deserialize(handTypeString), HandPartType.deserialize("RING_FINGER"), handLandmarksIndex)
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
    def getDiffs(handPose, otherHandPose):
        diffs = []
        for item in handPose:
            # find the same item in otherHandPose
            for otherItem in otherHandPose:
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