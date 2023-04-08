import json
from enum import IntEnum


class ImpairedSide(IntEnum):
    LEFT = 0,
    RIGHT = 1

class PoseDetectionType(IntEnum):
    BODY_POSE = 0,
    HAND_POSE = 1

class BodyPartDescription(IntEnum):
    SHOULDER = 0,     # LEFT/RIGHT_SHOULDER in poseDetection.BodyPart
    UPPER_ARM = 2,    # LEFT/RIGHT_UPPER_ARM in poseDetection.BodyPart
    FOREARM = 4,      # LEFT/RIGHT_WRIST in poseDetection.BodyPart

class ExerciseCreator:
    def __init__(self):
        self.none = None
    def createExercise(self, exerciseDescription, impairedSide):
        # Input JSON
        exerciseDescription = '\
        {\
            "name": "Raise arm to side",\
            "pose_detection_type": '+str(int(PoseDetectionType.BODY_POSE))+',\
            "body_parts":\
            [\
                {\
                    "body_part": '+str(int(BodyPartDescription.UPPER_ARM))+',\
                    "angles":\
                    {\
                        "plane": "xy",\
                        "score_1_min_diff": 20,\
                        "score_2_min": 80\
                    }\
                },\
                {\
                    "body_part": '+str(int(BodyPartDescription.FOREARM))+',\
                    "angles":\
                    {\
                        "plane": "xy",\
                        "score_1_min_diff": 20,\
                        "score_2_min": 80\
                    }\
                }\
            ]\
        }\
        '
        data_in = json.loads(exerciseDescription)
        # Output dict
        data_out = {}
        # Add exercise name to out
        data_out.update({"name": data_in["name"]})
        data_out.update({"body_parts": []})
        if impairedSide == ImpairedSide.LEFT:
            print("Impaired side is left, making sure the user does right body parts first")
            for body_part in range(len(data_in["body_parts"])):
                data_out["body_parts"].append({
                    "body_part": int(data_in["body_parts"][body_part]["body_part"])+1,
                    "angles": data_in["body_parts"][body_part]["angles"]
                })
            for body_part in range(len(data_in["body_parts"])):
                data_out["body_parts"].append({
                    "body_part": int(data_in["body_parts"][body_part]["body_part"]),
                    "angles": data_in["body_parts"][body_part]["angles"]
                })
        elif impairedSide == ImpairedSide.RIGHT:
            print("Impaired side is right, making sure the user does left body parts first")
            for body_part in range(len(data_in["body_parts"])):
                data_out["body_parts"].append({
                    "body_part": int(data_in["body_parts"][body_part]["body_part"])+0,
                    "angles": data_in["body_parts"][body_part]["angles"]
                })
            for body_part in range(len(data_in["body_parts"])):
                data_out["body_parts"].append({
                    "body_part": int(data_in["body_parts"][body_part]["body_part"])+1,
                    "angles": data_in["body_parts"][body_part]["angles"]
                })
        return json.dumps(data_out)




