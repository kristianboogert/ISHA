class ExerciseDataReader:
    @staticmethod
    def getPlaneForBodyPart(exerciseData, exercisePart, bodyPartType):
        for item in exerciseData["parts"][exercisePart]:
            print(item)
            if item["body_part"] == bodyPartType:
                return item["angles"]["plane"]
        return None
    @staticmethod
    def getCorrectAngleOffsets(exerciseData, exercisePart, bodyPartType):
        for item in exerciseData["parts"][exercisePart]:
            print(item)
            plane = item["angles"]["plane"]
            if item["body_part"] == bodyPartType:
                return [item["angles"]["score_2_min"], item["angles"]["score_2_max"]]
        return None