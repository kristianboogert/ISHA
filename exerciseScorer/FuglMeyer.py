# from ..poseDetection.HandPoseDetection import HandPoseDetection
# from ..poseDetection.Camera import Camera

import sys
import json
from time import time
from datetime import datetime
sys.path.append("..")
from poseDetection.HandPoseDetection import *
from poseDetection.HandPart import *
from poseDetection.BodyPart import *

### niet-fugl-meyer oefeningen:
#schuiven arm over tafel  (oefening 22)
#hand omdraaien           (oefening 10: alleen de eerste 3)
#spreiden sluiten vingers (oefening 9: alleen de eerste, voor de leuk ook de tweede)
###

class NeutralPose:
    def __init__(self, bodyPoseDetection):
        self.neutralPose = []
        self.bodyPoseDetection = bodyPoseDetection
    def addToNeutralPose(self, angleData):
        self.neutralPose.append(angleData)
    def createNeutralPose(self, poseData, exerciseData):
        for exercisePart in range(len(exerciseData["parts"])):
            for bodyPart in exerciseData["parts"][exercisePart]:
                directionAngles = self.bodyPoseDetection.getAnglesForBodyPart(bodyPart["body_part"], poseData)
                if directionAngles is None:
                    continue
                heightAngles = self.bodyPoseDetection.getHeightAnglesForBodyPart(bodyPart["body_part"], poseData)
                self.neutralPose.append({
                    "exercise_part": exercisePart,
                    "body_part": bodyPart["body_part"],
                    "direction_angles": directionAngles,
                    "height_angles": heightAngles
                })
        return self.neutralPose
    def getAngleDiffs(self, currentBodyPartAngles, bodyPart):
        # Get neutral angles for body part
        neutralAngles = None
        for item in self.neutralPose:
            print(item["body_part"], bodyPart["body_part"])
            if item["body_part"] == bodyPart["body_part"]:
                neutralAngles = item
                break
        if neutralAngles is None:
            return None
            exit(1)
        # compare angles
        print("ITEM: ", neutralAngles["direction_angles"]["xy"])
        print("CURR: ", currentBodyPartAngles["xy"])
        planes = ["xy", "yz", "xz"]
        diffs = {}
        for plane in planes:
            diffs[plane] = currentBodyPartAngles[plane] - neutralAngles["direction_angles"][plane]
        return diffs

        # xy_diff = item["xy"] - currentBodyPartAngles["xy"]
        # print(xy_diff)


class FuglMeyer:
    def __init__(self):
        self.none = None
    def landmarksAreVisible(self, landmarks, visibilityThreshold=0.85):
        for landmark in landmarks:
            if landmark is None or landmark.visibility < visibilityThreshold:
                return False
        return True
    def metadataCreate(self, exerciseName, poseTrackerTypeString, impairedSideString):
        metadata = {}
        metadata.update({"name": exerciseName})
        metadata.update({"pose_detection_type": poseTrackerTypeString})
        metadata.update({"impaired_side": impairedSideString})
        metadata.update({"exercise_parts": [[], []]})
        return metadata
    def metadataAddPose(self, metadata, currentExercisePart, startTime, pose):
        currentTime = int(time()*1000)
        msSinceStart = currentTime - startTime
        pose.update({"ms_since_exercise_start": msSinceStart})
        metadata["exercise_parts"][currentExercisePart].append(pose)
        return metadata
    def metadataSetScore(self, metadata, currentExercisePart, score):
        metadata["scores"][currentExercisePart] = score
        return metadata
    def metadataFixTimestamps(self, metadata):
        try:
            # fix time in data
            startTime = metadata["exercise_parts"][0][0]["ms_since_exercise_start"] # first exercisePart, first exercise
            for exercisePart in range(len(metadata["exercise_parts"])):
                for pose in range(len(metadata["exercise_parts"][exercisePart])):
                    fixedTime = metadata["exercise_parts"][exercisePart][pose]["ms_since_exercise_start"] - startTime
                    metadata["exercise_parts"][exercisePart][pose]["ms_since_exercise_start"] = fixedTime
        except:
            pass
        return metadata
    def scoreExercisePart(self, camera, bodyPoseDetection, exerciseData, visibilityThreshold=0.85):
        exerciseStarted = False
        exerciseData = json.loads(exerciseData)
        score = [0, 0] # [first part, second part]
        exercisePart = 0
        neutralBodyPose = NeutralPose(bodyPoseDetection) # TODO: FINISH IMPLEMENTNING THIS
        metadata = self.metadataCreate(exerciseData["name"], exerciseData["pose_detection_type"], exerciseData["impaired_side"])
        startTime = int(time()*1000) # in ms
        while True:
            ###
            # Get camera frame
            ###
            frame = camera.getFrame()
            ###
            # Detect body pose (mediapipe)
            ###
            frame_start = time()*1000
            poseData = bodyPoseDetection.getPose(frame)
            frame = bodyPoseDetection.drawPose(frame, poseData)
            frame_end = time()*1000
            FPS = int(1000/(frame_end-frame_start))
            frame = cv2.flip(frame, 1)
            cv2.putText(frame, "FPS: "+str(FPS), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2, cv2.LINE_AA)
            cv2.imshow('body frame', frame)
            if cv2.waitKey(1) == ord('q'):
                exercisePart += 1
                if exercisePart >= 2:
                    break
                else:
                    print("Onto the next side we go!")
            ###
            # Are all relevant joints in frame?
            ###
            user_in_view = True
            for exercise_part in exerciseData["parts"]:
                # check landmark visibility for each body part
                for bodyPart in exercise_part:
                    if not bodyPoseDetection.isBodyPartVisible(bodyPart["body_part"], poseData):
                        user_in_view = False
                        break
            if not user_in_view:
                print("not all bodyparts are in view, pausing score system until user becomes (partially) visible again")
                continue
            ###
            # Has exercise been started?
            ###
            if user_in_view == True and exerciseStarted == False:
                exerciseStarted = True
                neutral_pose = neutralBodyPose.createNeutralPose(poseData, exerciseData)
                print("\n\n\n\nUW POSITIE IN RUST\n\n\n\n")
                print(json.dumps(neutral_pose, indent=4))
                continue
            ###
            # Does user want to quit?
            ###
            # TODO: FIND OUT HOW TO DO THIS IN PRODUCTION!
            ###
            # Score the first exercise part
            ###
            exercisePartData = exerciseData["parts"][exercisePart]
            _bodyPart = BodyPart(0) # Only used for the serialize function
            for bodyPart in exercisePartData:
                # Get bodypart angle
                currentBodyPartAngles = bodyPoseDetection.getAnglesForBodyPart(bodyPart["body_part"], poseData)
                if currentBodyPartAngles is None:
                    print(time(), "Skipping frame, because user is not fully in view anymore (?)")
                    break
                print("TESTING:", currentBodyPartAngles)
                plane = bodyPart["angles"]["plane"]
                currentBodyPartAngle = currentBodyPartAngles[plane]
                givenAngles = bodyPart["angles"]
                # print("CURRENT_ANGLE:", currentBodyPartAngle)
                # print("GIVEN ANGLES: ", givenAngles)
                poseMetadata = {
                    "body_part": _bodyPart.serialize(bodyPart["body_part"]),
                    "plane": plane,
                    "angles": currentBodyPartAngles,
                    "score": 0
                }
                if givenAngles["score_2_min"] < currentBodyPartAngle < givenAngles["score_2_max"]:
                    print(time(), "user scored 2 on bodypart:", _bodyPart.serialize(bodyPart["body_part"]))
                    score[exercisePart] = 2
                    poseMetadata.update({"score": 2})
                else:
                    if score[exercisePart] == 2:
                        score[exercisePart] = 1
                        poseMetadata.update({"score": 1})
                self.metadataAddPose(metadata, exercisePart, startTime, poseMetadata)
            if score[exercisePart] == 2:
                exercisePart += 1
                if exercisePart >= 2:
                    break
                else:
                    print("Onto the next side we go!")
            ###
            # Relevant joints are close to neutral position?
            ###
            for exercise_part in exerciseData["parts"]:
                # check landmark visibility for each body part
                for bodyPart in exercise_part:
                    currentBodyPartAngles = bodyPoseDetection.getAnglesForBodyPart(bodyPart["body_part"], poseData)
                    angleDiffs = neutralBodyPose.getAngleDiffs(currentBodyPartAngles, bodyPart)
                    print("BODY_PART:", bodyPart, "\nDIFFS:", angleDiffs)
            # TODO: DIT VEREIST OOK DAT WE DE RUSTPOSITIE INLEZEN VOORDAT DE OEFENING WORDT BEGONNEN!!!!
        self.metadataFixTimestamps(metadata)
        return score, json.dumps(metadata, indent=4)







    # def exerciseRaiseArmToSideTest(self, camera, bodyPoseDetection, nonImpairedElbowBodyPart, visibilityThreshold=0.85):
    #     if not camera.is_running():
    #         camera.start()
    #     armAngles = {
    #         "neutral_min": -90,
    #         "neutral_max": -80,
    #         "score_1_min": -60,
    #         "score_2_min": -10,
    #     }
    #     exerciseStarted = False
    #     score = 0
    #     # Handle exercise
    #     while True:
    #         ###
    #         # Get camera frame
    #         ###
    #         frame = camera.getFrame()
    #         ###
    #         # Detect body pose (mediapipe)
    #         ###
    #         poseData = bodyPoseDetection.getPose(frame)
    #         frame = bodyPoseDetection.drawPose(frame, poseData)
    #         cv2.imshow('body frame', cv2.flip(frame, 1))
    #         if cv2.waitKey(1) == ord('q'):
    #             break
    #         ###
    #         # Are all relevant joints in frame?
    #         ###
    #         leftShoulderLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.LEFT_SHOULDER, poseData)
    #         rightShoulderLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.RIGHT_SHOULDER, poseData)
    #         leftElbowLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.LEFT_ELBOW, poseData)
    #         rightElbowLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.RIGHT_ELBOW, poseData)
    #         if not self.landmarksAreVisible([leftShoulderLandmark, rightShoulderLandmark, leftElbowLandmark, rightElbowLandmark]):
    #             print("user is not fully in frame for this exercise")
    #             continue
    #         ###
    #         # Has exercise been started?
    #         ###
    #         if not exerciseStarted:
    #             exerciseStarted = True
    #             continue
    #         ###
    #         # Has user pressed "quit"?
    #         ###
    #         # TODO: FIND OUT HOW TO DO THIS IN PRODUCTION! MAYBE SOME DBUS MAGIC SO OTHER PROCESSES CAN TALK TO US?
    #
    #         ###
    #         # Calculate relevant joint angles
    #         ###
    #         leftUpperArmAngle = bodyPoseDetection.getAnglesForBodyPart(BodyPart.LEFT_ELBOW, poseData)
    #         rightUpperArmAngle = bodyPoseDetection.getAnglesForBodyPart(BodyPart.RIGHT_ELBOW, poseData)
    #         leftLowerArmAngle = bodyPoseDetection.getAnglesForBodyPart(BodyPart.LEFT_WRIST, poseData)
    #         rightLowerArmAngle = bodyPoseDetection.getAnglesForBodyPart(BodyPart.RIGHT_WRIST, poseData)
    #         try:
    #             print("ARM ANGLES:\nLeft: ", leftUpperArmAngle["xy"],
    #                 "\nRight:", rightUpperArmAngle["xy"], "\n",
    #                 "WRIST ANGLES:\nLeft: ", leftLowerArmAngle["xy"],
    #                 "\nRight:", rightLowerArmAngle["xy"], "\n")
    #         except:
    #             pass
    #         ###
    #         # Relevant joints have reached threshold?
    #         ###
    #         if leftUpperArmAngle["xy"] > armAngles["score_1_min"] and score != 2:
    #             print("\n\n\n\nSCORE IS 1 NOW!\n\n\n\n")
    #             score = 1
    #         if leftUpperArmAngle["xy"] > armAngles["score_2_min"]:
    #             print("\n\n\n\nSCORE IS 2 NOW!\n\n\n\n")
    #             score = 2
    #             break
    #         ###
    #         # Relevant joints are close to neutral position?
    #         ###
    #         if score >= 1 and leftUpperArmAngle["xy"] < armAngles["neutral_max"]:
    #             break
    #     return score
    #
    #
    #
