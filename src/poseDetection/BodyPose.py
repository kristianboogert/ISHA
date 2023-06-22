from math import degrees, radians, acos, dist
from time import time
from .BodyPart import BodyPart

class BodyPose:
    def __init__(self):
        self.bodyPose = []
        self.clear()
    def clear(self):
        self.bodyPose = []
    def setBodyPose(self, bodyPose):
        self.bodyPose = bodyPose
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
    @staticmethod
    def getDiffs(bodyPose, otherBodyPose):
        diffs = []
        for item in bodyPose:
            # find the same item in otherBodyPose
            for otherItem in otherBodyPose:
                if item["body_part"] == otherItem["body_part"]:
                    diffs.append({
                        "body_part": item["body_part"],
                        "origin": {
                            "x": round(otherItem["origin"]["x"] - item["origin"]["x"]),
                            "y": round(otherItem["origin"]["y"] - item["origin"]["y"]),
                            "z": round(otherItem["origin"]["z"] - item["origin"]["z"])
                        },
                        "heading": {
                            "xy": BodyPart.getAngleDiff(otherItem["heading"]["xy"], item["heading"]["xy"]),
                            "yz": BodyPart.getAngleDiff(otherItem["heading"]["yz"], item["heading"]["yz"]),
                            "xz": BodyPart.getAngleDiff(otherItem["heading"]["xz"], item["heading"]["xz"])
                        }
                    })
        return diffs
    # @staticmethod
    # # Find how much % a body pose differs from another.
    # # Formula used: |diff/avg|*100
    # def getDiffsPercent(bodyPose, otherBodyPose):
    #     diffs = []
    #     for item in bodyPose:
    #         # find the same item in otherBodyPose
    #         for otherItem in otherBodyPose:
    #             if item["body_part"] == otherItem["body_part"]:
    #                 diffs.append({
    #                     "body_part": item["body_part"],
    #                     "origin": {
    #                         "x": abs((otherItem["origin"]["x"] - item["origin"]["x"]) / (otherItem["origin"]["x"] + item["origin"]["x"]))*100,
    #                         "y": abs((otherItem["origin"]["z"] - item["origin"]["y"]) / (otherItem["origin"]["y"] + item["origin"]["y"]))*100,
    #                         "z": abs((otherItem["origin"]["z"] - item["origin"]["z"]) / (otherItem["origin"]["z"] + item["origin"]["z"]))*100
    #                     },
    #                     "heading": {
    #                         "xy": BodyPart.getAngleDiff(otherItem["heading"]["xy"], item["heading"]["xy"]),
    #                         "yz": BodyPart.getAngleDiff(otherItem["heading"]["yz"], item["heading"]["yz"]),
    #                         "xz": BodyPart.getAngleDiff(otherItem["heading"]["xz"], item["heading"]["xz"])
    #                     }
    #                 })
    #     return diffs
    @staticmethod
    def isPoseSimilar(bodyPoseDiffs):
        for diff in bodyPoseDiffs:
            print(diff["heading"]["xy"])
            print(diff["heading"]["yz"])
            print(diff["heading"]["xz"])
            if diff["heading"]["xy"] > 20 or diff["heading"]["yz"] > 20 or diff["heading"]["xz"] > 20:
                return False
        return True













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
