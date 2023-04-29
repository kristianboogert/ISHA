from math import degrees, radians, acos, dist
from time import time
from .BodyPart import BodyPart

#class Pose bestaat uit meerdere BodyParts
#class BodyPart kan niet zonder BodyJoint

class BodyPose:
    def __init__(self):
        self.bodyPose = []
        self.clear()
    def clear(self):
        self.bodyPose = []
    def getBodyPose(self):
        return self.bodyPose
    def createPose(self, poseLandmarks, relevantBodyPartTypeStrings):
        self.clear()
        for bodyPartTypeString in relevantBodyPartTypeStrings:
            bodyPart = BodyPart.createFromLandmarks(poseLandmarks, bodyPartTypeString)
            if bodyPart is not None:
                self.bodyPose.append({
                    "body_part": bodyPart.getBodyPartType(),
                    "origin": bodyPart.getOriginBodyJoint().getPosition(),
                    "heading": bodyPart.getHeading(),
                    "timestamp": round(time()*1000)
                })
        return self.bodyPose












    # def get(self):
    #     return self.bodyPose
    # def setPosition(self, limb, position):
    #     # add limb to bodypose if not already set
    #     if not limb in self.bodyPose:
    #         self.bodyPose.update({limb: {}})
    #     self.bodyPose[limb].update({"position": position})
    # def getPosition(self, limb):
    #     try:
    #         return self.bodyPose[limb]["position"]
    #     except:
    #         return None
    # def setAngle(self, limb, angle):
    #     if not limb in self.bodyPose:
    #         self.bodyPose.update({limb: {}})
    #     self.bodyPose[limb].update({"angle": angle})
    # def getAngle(self, limb):
    #     try:
    #         return self.bodyPose[limb]["angle"]
    #     except:
    #         return None
