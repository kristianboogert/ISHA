from time import time

class BodyPoseMetadata:
    def __init__(self, exerciseName, poseTrackerTypeString, impairedSideString):
        self.metadata = None
        self.exerciseName = exerciseName
        self.poseTrackerTypeString = poseTrackerTypeString
        self.impairedSideString = impairedSideString
        self.clear()
    def clear(self):
        self.metadata = {}
        self.metadata.update({"name": self.exerciseName})
        self.metadata.update({"pose_detection_type": self.poseTrackerTypeString})
        self.metadata.update({"impaired_side": self.impairedSideString})
        self.metadata.update({"exercise_parts": [[], []]})
        return self.metadata
    def addPose(self, bodyPartTypeString, plane, angles, score, currentExercisePart, startTime):
        currentTime = int(time()*1000)
        msSinceStart = currentTime - startTime
        poseLandmarks = {
            "body_part": bodyPartTypeString,
            "plane": plane,
            "angles": angles,
            "score": score,
            "ms_since_exercise_start": msSinceStart
        }
        self.metadata["exercise_parts"][currentExercisePart].append(poseLandmarks)
        return self.metadata
    def fixTimeStamps(self):
        try:
            startTime = self.metadata["exercise_parts"][0][0]["ms_since_exercise_start"] # first exercisePart, first exercise
            for exercisePart in range(len(self.metadata["exercise_parts"])):
                for pose in range(len(self.metadata["exercise_parts"][exercisePart])):
                    fixedTime = self.metadata["exercise_parts"][exercisePart][pose]["ms_since_exercise_start"] - startTime
                    self.metadata["exercise_parts"][exercisePart][pose]["ms_since_exercise_start"] = fixedTime
        except:
            pass
        return self.metadata
    def getMetadata(self):
        self.fixTimeStamps()
        return self.metadata