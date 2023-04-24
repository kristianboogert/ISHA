from math import degrees, radians, acos, dist

#class Pose bestaat uit meerdere BodyParts
#class BodyPart kan niet zonder BodyJoint

class Pose:
    def __init__(self, poseType):
        self.bodyPoseType = poseType
        self.bodyPose = {}
        self.clear()
    def clear(self):
        self.bodyPose = {}
        self.bodyPose.update({"pose_type": self.bodyPoseType})
        self.bodyPose.update({"body_parts": []})
    def addBodyPart(self, bodyPart):
        self.bodyPose["body_parts"].append(bodyPart)
    def getBodyPart(self, bodyPartTypeString):
        for bodyPart in self.bodyPose:
            if bodyPart.getBodyPartType() == bodyPartTypeString:
                return bodyPart
    # def createPose(self, poseDetectionData): # TODO!!!!!!!!!!!!!!












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
