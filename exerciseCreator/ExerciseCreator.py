import json
from enum import IntEnum


class ImpairedSide(IntEnum):
    LEFT = 0,
    RIGHT = 1
    def serialize(self, impairedSide):
        if impairedSide == self.LEFT:
            return "LEFT"
        if impairedSide == self.RIGHT:
            return "RIGHT"

class PoseDetectionType(IntEnum):
    BODY_POSE = 0,
    HAND_POSE = 1
    def serialize(self, poseDetectionType):
        if poseDetectionType.upper() == self.BODY_POSE:
            return "BODY_POSE"
        if poseDetectionType.upper() == self.HAND_POSE:
            return "HAND_POSE"
    def deserialize(self, poseDetectionTypeString):
        if poseDetectionTypeString.upper() == "BODY_POSE":
            return self.BODY_POSE
        if poseDetectionTypeString.upper() == "HAND_POSE":
            return self.HAND_POSE

class BodyPartDescription(IntEnum):
    SHOULDER = 0,     # LEFT/RIGHT_SHOULDER in poseDetection.BodyPart
    UPPER_ARM = 2,    # LEFT/RIGHT_UPPER_ARM in poseDetection.BodyPart
    FOREARM = 4,      # LEFT/RIGHT_WRIST in poseDetection.BodyPart
    def serialize(self, bodyPart):
        if bodyPart.upper() == self.SHOULDER:
            return "SHOULDER"
        if bodyPart.upper() == self.UPPER_ARM:
            return "UPPER_ARM"
        if bodyPart.upper() == self.FOREARM:
            return "FOREARM"
    def deserialize(self, bodyPartString):
        if bodyPartString.upper() == "SHOULDER":
            return self.SHOULDER
        if bodyPartString.upper() == "UPPER_ARM":
            return self.UPPER_ARM
        if bodyPartString.upper() == "FOREARM":
            return self.FOREARM

class ExerciseCreator:
    def __init__(self):
        self.none = None
    def createExercise(self, exerciseDescription, impairedSide):
        data_in = json.loads(exerciseDescription)
        # Deserialize pose type entry in exerciseDescription
        poseDetectionType = PoseDetectionType(0) # Only used for deserializing a string value
        poseDetectionTypeString = poseDetectionType.deserialize(data_in["pose_detection_type"])
        # Deserialize body parts in exerciseDescription
        bodyPart = BodyPartDescription(0) # Only used for deserializing a string value
        for body_part in data_in["body_parts"]:
            body_part["body_part"] = bodyPart.deserialize(body_part["body_part"])
        # Create output dict
        data_out = {}
        # Add exercise name to out
        data_out.update({"name": data_in["name"]})
        data_out.update({"pose_detection_type": poseDetectionTypeString})
        data_out.update({"parts": [[], []]})
        if impairedSide == ImpairedSide.LEFT:
            print("Impaired side is left, making sure the user does right body parts first")
            tmp = ImpairedSide(0)
            impairedSideString = tmp.serialize(ImpairedSide.LEFT)
            data_out.update({"impaired_side": impairedSideString})
            for body_part in range(len(data_in["body_parts"])):
                data_out["parts"][0].append({
                    "body_part": int(data_in["body_parts"][body_part]["body_part"])+1,
                    "angles": data_in["body_parts"][body_part]["angles"]
                })
            for body_part in range(len(data_in["body_parts"])):
                data_out["parts"][1].append({
                    "body_part": int(data_in["body_parts"][body_part]["body_part"]),
                    "angles": data_in["body_parts"][body_part]["angles"]
                })
        elif impairedSide == ImpairedSide.RIGHT:
            print("Impaired side is right, making sure the user does left body parts first")
            tmp = ImpairedSide(0)
            impairedSideString = tmp.serialize(ImpairedSide.RIGHT)
            data_out.update({"impaired_side": impairedSideString})
            for body_part in range(len(data_in["body_parts"])):
                data_out["parts"][0].append({
                    "body_part": int(data_in["body_parts"][body_part]["body_part"])+0,
                    "angles": data_in["body_parts"][body_part]["angles"]
                })
            for body_part in range(len(data_in["body_parts"])):
                data_out["parts"][1].append({
                    "body_part": int(data_in["body_parts"][body_part]["body_part"])+1,
                    "angles": data_in["body_parts"][body_part]["angles"]
                })
        # Return JSON data (from data_out dict)
        return json.dumps(data_out, indent=4)



                # {\
                #     "body_part": '+str(int(BodyPartDescription.FOREARM))+',\
                #     "angles":\
                #     {\
                #         "plane": "xy",\
                #         "score_1_min_diff": 20,\
                #         "score_2_min": 80\
                #     }\
                # }\


