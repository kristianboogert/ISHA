import json

from .PoseDetectionType import PoseDetectionType
from .BodyPartDescriptionType import BodyPartDescriptionType
from .ImpairedSideType import ImpairedSideType

class ExerciseCreator:
    def createExercise(exerciseDescription, impairedSideType):
        data_in = json.loads(exerciseDescription)
        # Deserialize pose type entry in exerciseDescription
        # Deserialize body parts in exerciseDescription
        for body_part in data_in["body_parts"]:
            body_part["body_part"] = BodyPartDescriptionType.deserialize(body_part["body_part"])
        # Create output dict
        data_out = {}
        # Add exercise name to out
        data_out.update({"name": data_in["name"]})
        data_out.update({"pose_detection_type": data_in["pose_detection_type"].upper()})
        data_out.update({"parts": [[], []]})
        if impairedSideType == ImpairedSideType.LEFT:
            print("Impaired side is left, making sure the user does right body parts first")
            impairedSideString = ImpairedSideType.serialize(ImpairedSideType.LEFT)
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
        elif impairedSideType == ImpairedSideType.RIGHT:
            print("Impaired side is right, making sure the user does left body parts first")
            impairedSideString = ImpairedSideType.serialize(ImpairedSideType.RIGHT)
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