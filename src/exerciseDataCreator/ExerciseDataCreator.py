import json
import sys

from .PoseDetectionType import PoseDetectionType
from .BodyPartDescriptionType import BodyPartDescriptionType
from .ImpairedSideType import ImpairedSideType
sys.path.append("..")
from poseDetection.HandType import HandType
from poseDetection.HandPartType import HandPartType

class ExerciseDataCreator:
    def createBodyExerciseData(exerciseDescription, impairedSideType):
        data_in = json.loads(exerciseDescription)
        # Deserialize body part in exerciseDescription
        for body_part in data_in["body_parts"]:
            body_part["body_part"] = BodyPartDescriptionType.deserialize(body_part["body_part"])
        data_out = {}
        data_out.update({"name": data_in["name"]})
        data_out.update({"pose_detection_type": data_in["pose_detection_type"]})
        data_out.update({"parts": [[], []]})
        if impairedSideType == ImpairedSideType.LEFT:
            print("Impaired side is left, making sure the user does right body side first")
            impairedSideString = ImpairedSideType.serialize(ImpairedSideType.LEFT)
            data_out.update({"impaired_side": impairedSideString})
            data_out.update({"pose_detection_type": data_in["pose_detection_type"]})
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
        elif impairedSideType == ImpairedSideType.RIGHT:
            print("Impaired side is right, making sure the user does left body side first")
            impairedSideString = ImpairedSideType.serialize(ImpairedSideType.RIGHT)
            data_out.update({"impaired_side": impairedSideString})
            for body_part in range(len(data_in["body_parts"])):
                data_out["parts"][0].append({
                    "body_part": int(data_in["body_parts"][body_part]["body_part"]),
                    "angles": data_in["body_parts"][body_part]["angles"]
                })
            for body_part in range(len(data_in["body_parts"])):
                data_out["parts"][1].append({
                    "body_part": int(data_in["body_parts"][body_part]["body_part"])+1,
                    "angles": data_in["body_parts"][body_part]["angles"]
                })
        # Return JSON data (from data_out dict)
        return json.dumps(data_out, indent=4)

    def createHandRotationExerciseData(exerciseDescription, impairedSideType):
        data_in = json.loads(exerciseDescription)
        data_out = {}
        data_out.update({"name": data_in["name"]})
        data_out.update({"pose_detection_type": data_in["pose_detection_type"]})
        data_out.update({"parts": []})
        if impairedSideType == ImpairedSideType.LEFT:
            data_out["parts"].append({
                "hand": HandType.RIGHT_HAND,
                "angles": data_in["angles"]
            })
            data_out["parts"].append({
                "hand": HandType.LEFT_HAND,
                "angles": data_in["angles"]
            })
        if impairedSideType == ImpairedSideType.RIGHT:
            data_out["parts"].append({
                "hand": HandType.LEFT_HAND,
                "angles": data_in["angles"]
            })
            data_out["parts"].append({
                "hand": HandType.RIGHT_HAND,
                "angles": data_in["angles"]
            })
        return json.dumps(data_out, indent=4)
    def createHandExerciseData(exerciseDescription, impairedSideType):
        data_in = json.loads(exerciseDescription)
        data_out = {}
        data_out.update({"name": data_in["name"]})
        data_out.update({"pose_detection_type": data_in["pose_detection_type"]})
        data_out.update({"parts": [[], []]})
        if impairedSideType == ImpairedSideType.LEFT:
            print("Impaired side is left, making sure the user moves right hand first")
            for hand_part in range(len(data_in["hand_parts"])):
                data_out["parts"][0].append({
                    "hand": HandType.RIGHT_HAND,
                    "hand_part": HandPartType.deserialize(data_in["hand_parts"][hand_part]["hand_part"]),
                    "angles": data_in["hand_parts"][hand_part]["angles"]
                })
            for hand_part in range(len(data_in["hand_parts"])):
                data_out["parts"][1].append({
                    "hand": HandType.LEFT_HAND,
                    "hand_part": HandPartType.deserialize(data_in["hand_parts"][hand_part]["hand_part"]),
                    "angles": data_in["hand_parts"][hand_part]["angles"]
                })
        if impairedSideType == ImpairedSideType.RIGHT:
            print("Impaired side is left, making sure the user moves left hand first")
            for hand_part in range(len(data_in["hand_parts"])):
                data_out["parts"][0].append({
                    "hand": HandType.LEFT_HAND,
                    "hand_part": HandPartType.deserialize(data_in["hand_parts"][hand_part]["hand_part"]),
                    "angles": data_in["hand_parts"][hand_part]["angles"]
                })
            for hand_part in range(len(data_in["hand_parts"])):
                data_out["parts"][1].append({
                    "hand": HandType.RIGHT_HAND,
                    "hand_part": HandPartType.deserialize(data_in["hand_parts"][hand_part]["hand_part"]),
                    "angles": data_in["hand_parts"][hand_part]["angles"]
                })
        return json.dumps(data_out, indent=4)

    def createExerciseData(exerciseDescription, impairedSideType):
        data_in = json.loads(exerciseDescription)
        if data_in["pose_detection_type"].upper() == "BODY_POSE":
            return ExerciseDataCreator.createBodyExerciseData(exerciseDescription, impairedSideType)
        if data_in["pose_detection_type"].upper() == "HAND_ROTATION":
            return ExerciseDataCreator.createHandRotationExerciseData(exerciseDescription, impairedSideType)
        if data_in["pose_detection_type"].upper() == "HAND_POSE":
            return ExerciseDataCreator.createHandExerciseData(exerciseDescription, impairedSideType)
        return None