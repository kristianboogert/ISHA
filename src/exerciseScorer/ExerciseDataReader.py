class ExerciseDataReader:
    @staticmethod
    def getPlaneForBodyPart(exerciseData, exercisePart, bodyPartType):
        for item in exerciseData["parts"][exercisePart]:
            if item["body_part"] == bodyPartType:
                return item["angles"]["plane"]
        return None
    @staticmethod
    def getPlaneForHandPart(exerciseData, exercisePart, handPartType):
        for item in exerciseData["parts"][exercisePart]:
            if item["hand_part"] == handPartType:
                return item["angles"]["plane"]
        return None
    @staticmethod
    def getCorrectBodyPartAngleOffsets(exerciseData, exercisePart, bodyPartType, plane):
        for item in exerciseData["parts"][exercisePart]:
            if item["body_part"] == bodyPartType and item["angles"]["plane"] == plane:
                return [item["angles"]["score_2_min"], item["angles"]["score_2_max"]]
        return None
    @staticmethod
    def getCorrectHandPartAngleOffsets(exerciseData, exercisePart, handPartType):
        for item in exerciseData["parts"][exercisePart]:
            plane = item["angles"]["plane"]
            if item["hand_part"] == handPartType:
                return [item["angles"]["score_2_min"], item["angles"]["score_2_max"]]
        return None