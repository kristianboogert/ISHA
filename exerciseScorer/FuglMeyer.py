# from ..poseDetection.HandPoseDetection import HandPoseDetection
# from ..poseDetection.Camera import Camera

import sys
import json
import cv2
from math import degrees, radians
from time import time
from datetime import datetime
from .BodyPoseMetadata import BodyPoseMetadata
from .ExerciseDataReader import ExerciseDataReader
sys.path.append("..")
#from poseDetection.HandPoseDetection import *
# from poseDetection.HandPart import *
from poseDetection.BodyPose import BodyPose
from poseDetection.BodyPart import *

### niet-fugl-meyer oefeningen:
#schuiven arm over tafel  (oefening 22)
#hand omdraaien           (oefening 10: alleen de eerste 3)
#spreiden sluiten vingers (oefening 9: alleen de eerste, voor de leuk ook de tweede)
###

class FuglMeyer:
    def isUserInView(exerciseData, bodyPoseDetection, poseLandmarks):
        for exercisePart in exerciseData["parts"]:
            # check landmark visibility for each body part
            for bodyPart in exercisePart:
                if not bodyPoseDetection.isBodyPartVisible(bodyPart["body_part"], poseLandmarks):
                    return False
        return True
    def scoreExercise(camera, bodyPoseDetection, exerciseData, visibilityThreshold=0.85):
        exerciseStarted = False
        exerciseData = json.loads(exerciseData)
        score = [0, 0] # [first part, second part]
        currentExercisePart = 0
        neutralBodyPoseCreator = BodyPose()
        currentBodyPoseCreator = BodyPose()
        neutralBodyPose = [None, None]
        metadata = BodyPoseMetadata(exerciseData["name"], exerciseData["pose_detection_type"], exerciseData["impaired_side"])
        relevantBodyPartTypeStrings = [[], []]
        for exercisePart in range(len(exerciseData["parts"])):
            for bodyPartData in exerciseData["parts"][exercisePart]:
                bodyPartTypeString = BodyPartType.serialize(bodyPartData["body_part"])
                relevantBodyPartTypeStrings[exercisePart].append(bodyPartTypeString)
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
            poseLandmarks = bodyPoseDetection.getPose(frame)
            frame_end = time()*1000
            FPS = int(1000/(frame_end-frame_start))
            frame = cv2.flip(frame, 1)
            cv2.putText(frame, "FPS: "+str(FPS), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2, cv2.LINE_AA)
            cv2.imshow('body frame', frame)
            if cv2.waitKey(1) == ord('q'):
                currentExercisePart += 1
                if currentExercisePart >= 2:
                    break
                else:
                    print("Onto the next side we go!")
            ###
            # Are all relevant body parts in frame?
            ###
            userInView = FuglMeyer.isUserInView(exerciseData, bodyPoseDetection, poseLandmarks)
            if not userInView:
                print("not all bodyparts are in view, pausing score system until user becomes (partially) visible again")
                continue
            ###
            # Has exercise been started?
            ###
            if userInView and exerciseStarted == False:
                exerciseStarted = True
                continue
            ###
            # Does user want to quit?
            ###
            # TODO: FIND OUT HOW TO DO THIS IN PRODUCTION! WE NEED SOME SORT OF API/DBUS SYSTEM FOR THIS!
            ###
            # Create neutral pose if it doesn't exist
            ###
            if neutralBodyPose[currentExercisePart] is None:
                print("CREATING NEUTRAL POSE SNAPSHOT!")
                neutralBodyPose[currentExercisePart] = neutralBodyPoseCreator.createPose(poseLandmarks, relevantBodyPartTypeStrings[currentExercisePart])
            ###
            # Create current body pose
            ###
            currentBodyPose = currentBodyPoseCreator.createPose(poseLandmarks, relevantBodyPartTypeStrings[currentExercisePart])
            ###
            # See if the user moved (score 1)
            ###
            bodyPoseDiffs = BodyPose.getDiffs(currentBodyPose, neutralBodyPose[currentExercisePart])
            for diff in bodyPoseDiffs:
                plane = ExerciseDataReader.getPlaneForBodyPart(exerciseData, currentExercisePart, diff["body_part"])
                if diff["heading"][plane]>20:
                    if score[currentExercisePart] < 1:
                        score[currentExercisePart] = 1
            if score[currentExercisePart]:
                print("USER SCORED 1!")
            ###
            # See if the user's body position is close to the correct one (score 2)
            ###
            # TODO: KIJK HIER NOG EVEN NAAR, HET LIJKT ER NAMELIJK OP DAT ER MAAR 1 BODY PART GOED HOEFT TE ZIJN
            userHasCorrectBodyPose = False
            for bodyPartData in currentBodyPose:
                plane = ExerciseDataReader.getPlaneForBodyPart(exerciseData, currentExercisePart, diff["body_part"])
                currentBodyPartAngle = bodyPartData["heading"][plane]
                maxOffsets = ExerciseDataReader.getCorrectAngleOffsets(exerciseData, currentExercisePart, diff["body_part"])
                print(maxOffsets)
                print(currentBodyPartAngle)
                if maxOffsets[0] > currentBodyPartAngle and currentBodyPartAngle > maxOffsets[1]:
                    userHasCorrectBodyPose = True
                else:
                    userHasCorrectBodyPose = False
                    break

            if userHasCorrectBodyPose:
                print("USER SCORED 2!")
                score[currentExercisePart] = 2
            ###
            # See if the user moved back to neutral position before moving on
            ###
            bodyPoseDiffs = BodyPose.getDiffs(currentBodyPose, neutralBodyPose[currentExercisePart])
            userInNeutralPosition = False
            print("exercise part", currentExercisePart)
            print("score:", score[currentExercisePart])
            if score[currentExercisePart] > 0:
                userInNeutralPosition = True
                for diff in bodyPoseDiffs:
                    if diff["heading"]["xy"]>20:
                        userInNeutralPosition = False
            print(userInNeutralPosition)
            if userInNeutralPosition:
                currentExercisePart+=1
            if currentExercisePart >= 2:
                print("all done!")
                break
            ###
            # Add body pose data to metadata
            ###
            for bodyPart in exerciseData["parts"][currentExercisePart]:
                # Get bodypart angle
                currentBodyPartAngles = bodyPoseDetection.getAnglesForBodyPart(bodyPart["body_part"], poseLandmarks)
                if currentBodyPartAngles is None:
                    print(time(), "Skipping frame, because user is not fully in view anymore (?)")
                    break
                print("TESTING:", currentBodyPartAngles)
                plane = bodyPart["angles"]["plane"]
                currentBodyPartAngle = currentBodyPartAngles[plane]
                givenAngles = bodyPart["angles"]
                poseMetadata = {
                    "body_part": BodyPartType.serialize(bodyPart["body_part"]),
                    "plane": plane,
                    "angles": currentBodyPartAngles,
                    "score": 0
                }
                if givenAngles["score_2_min"] < currentBodyPartAngle < givenAngles["score_2_max"]:
                    print(time(), "user scored 2 on bodypart:", BodyPartType.serialize(bodyPart["body_part"]))
                    score[currentExercisePart] = 2
                    poseMetadata.update({"score": 2})
                else:
                    if score[currentExercisePart] == 2:
                        score[currentExercisePart] = 1
                        poseMetadata.update({"score": 1})
                metadata.addPose(BodyPartType.serialize(bodyPart["body_part"]), plane, currentBodyPartAngles, score[currentExercisePart], currentExercisePart, startTime)
        print("METADATA:", metadata.getMetadata()) 
        return score, json.dumps(metadata.getMetadata(), indent=4)






















# class NeutralPose:
#     def __init__(self, bodyPoseDetection):
#         self.neutralPose = []
#         self.bodyPoseDetection = bodyPoseDetection
#     def addToNeutralPose(self, angleData):
#         self.neutralPose.append(angleData)
#     def createNeutralPose(self, poseLandmarks, exerciseData):
#         for exercisePart in range(len(exerciseData["parts"])):
#             for bodyPartData in exerciseData["parts"][exercisePart]:
#                 bodyPartType = bodyPartData["body_part"]
#                 bodyPartTypeString = BodyPartType.serialize(bodyPartType)
#                 bodyPart = BodyPart.createFromLandmarks(poseLandmarks, bodyPartTypeString)
#                 if bodyPart is None:
#                     continue
#                 self.neutralPose.append({
#                     "exercise_part": exercisePart,
#                     "body_part": bodyPartType,
#                     "heading": bodyPart.getHeading()
#                 })
#         return self.neutralPose
#     def getAngleDiffs(self, currentBodyPose, bodyPart):
#         # Get neutral angles for body part
#         neutralPose = None
#         for item in self.neutralPose:
#             print(item["body_part"], bodyPart["body_part"])
#             if item["body_part"] == bodyPart["body_part"]:
#                 neutralPose = item
#                 break
#         print(neutralPose)
#         if neutralPose is None:
#             return None
#             exit(1)
#         # compare angles
#         planes = ["xy", "yz", "xz"]
#         diffs = {}
#         for plane in planes:
#             print("CURR:", currentBodyPose["heading"][plane], plane)
#             print("PREV:", neutralPose["heading"][plane], plane)
#             diffs[plane] = degrees(radians(currentBodyPartAngles[plane])) - degrees(radians(neutralPose["heading"][plane]))
#         return diffs

#         # xy_diff = item["xy"] - currentBodyPartAngles["xy"]
#         # print(xy_diff)




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
    #         poseLandmarks = bodyPoseDetection.getPose(frame)
    #         frame = bodyPoseDetection.drawPose(frame, poseLandmarks)
    #         cv2.imshow('body frame', cv2.flip(frame, 1))
    #         if cv2.waitKey(1) == ord('q'):
    #             break
    #         ###
    #         # Are all relevant joints in frame?
    #         ###
    #         leftShoulderLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.LEFT_SHOULDER, poseLandmarks)
    #         rightShoulderLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.RIGHT_SHOULDER, poseLandmarks)
    #         leftElbowLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.LEFT_ELBOW, poseLandmarks)
    #         rightElbowLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.RIGHT_ELBOW, poseLandmarks)
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
    #         leftUpperArmAngle = bodyPoseDetection.getAnglesForBodyPart(BodyPart.LEFT_ELBOW, poseLandmarks)
    #         rightUpperArmAngle = bodyPoseDetection.getAnglesForBodyPart(BodyPart.RIGHT_ELBOW, poseLandmarks)
    #         leftLowerArmAngle = bodyPoseDetection.getAnglesForBodyPart(BodyPart.LEFT_WRIST, poseLandmarks)
    #         rightLowerArmAngle = bodyPoseDetection.getAnglesForBodyPart(BodyPart.RIGHT_WRIST, poseLandmarks)
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
