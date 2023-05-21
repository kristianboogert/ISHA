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
from poseDetection.HandPose import HandPose
from poseDetection.HandPart import *

### niet-fugl-meyer oefeningen:
#schuiven arm over tafel  (oefening 22)
#hand omdraaien           (oefening 10: alleen de eerste 3)
#spreiden sluiten vingers (oefening 9: alleen de eerste, voor de leuk ook de tweede)
###

class FuglMeyer:
    def areBodyPartsInView(exerciseData, bodyPoseDetection, poseLandmarks):
        for exercisePart in exerciseData["parts"]:
            # check landmark visibility for each body part
            for bodyPart in exercisePart:
                if not bodyPoseDetection.isBodyPartVisible(bodyPart["body_part"], poseLandmarks):
                    return False
        return True
    def areHandPartsInView(exerciseData, bodyPoseDetection, poseLandmarks):
        for exercisePart in exerciseData["parts"]:
            # check landmark visibility for each hand part
            for handPart in exercisePart:
                if not handPoseDetection.isBodyPartVisible(handPart["hand_part"], poseLandmarks):
                    return False
        return True
    def scoreExercise(camera, bodyPoseDetection, handPoseDetection, exerciseData):
        _exerciseData = json.loads(exerciseData)
        if _exerciseData["pose_detection_type"] == "body_pose":
            return FuglMeyer.scoreBodyExercise(camera, bodyPoseDetection, exerciseData)
        if _exerciseData["pose_detection_type"] == "hand_rotation":
            return FuglMeyer.scoreHandRotationExercise(camera, handPoseDetection, exerciseData)
        if _exerciseData["pose_detection_type"] == "hand_pose":
            return FuglMeyer.scoreHandExercise(camera, handPoseDetection, exerciseData)
        print("Invalid pose detection type was given, exiting.")
        exit(1)
    def scoreHandRotationExercise(camera, handPoseDetection, exerciseData):
        # Create a neutral hand pose? The first thing the camera sees, it should consider a neutral hand pose
        exerciseData = json.loads(exerciseData)
        score = [0, 0]
        for exercisePart in range(len(exerciseData["parts"])):
            neutralHandPose = None
            currentHandPose = None
            # Get neutral hand pose first, for score 1
            neutralHandPoseCreator = HandPose()
            currentHandPoseCreator = HandPose()
            while True:
                handPoseData = handPoseDetection.getPose(camera.getFrame())
                neutralHandPoseCreator.createPose(handPoseData, HandType.serialize(exerciseData["parts"][exercisePart]["hand"]), []) # only hand rotation is needed, so no hand parts are given
                neutralHandPose = neutralHandPoseCreator.getHandPose()
                if len(neutralHandPose):
                    print("Neutral pose has been saved!\nDATA:", neutralHandPose)
                    break
            while True:
                handPoseData = handPoseDetection.getPose(camera.getFrame())
                currentHandPoseCreator.createPose(handPoseData, HandType.serialize(exerciseData["parts"][exercisePart]["hand"]), [])
                currentHandPose = currentHandPoseCreator.getHandPose()
                # see if the user moved their hand at all (score 1)
                print(currentHandPose)
                if len(neutralHandPose) and len(currentHandPose):
                    neutralHandPoseRotationAngle = neutralHandPose[0]["hand_rotation_xy"]
                    currentHandPoseRotationAngle = currentHandPose[0]["hand_rotation_xy"]
                    if currentHandPoseRotationAngle - neutralHandPoseRotationAngle >= exerciseData["parts"][exercisePart]["angles"]["score_1_min_diff"]:
                        if score[exercisePart] < 1:
                            score[exercisePart] = 1
                        print("SCORE 1!!!!!!!!!!!11!1")
                # see if the user moved their hand enough (score 2)
                if len(currentHandPose) and currentHandPose[0]["hand_rotation_xy"] > 160:
                    score[exercisePart] = 2
                    print("SCORE 2!")
                # see if the hand positition is close to neutral
                if len(neutralHandPose) and len(currentHandPose):
                    neutralHandPoseRotationAngle = neutralHandPose[0]["hand_rotation_xy"]
                    currentHandPoseRotationAngle = currentHandPose[0]["hand_rotation_xy"]
                    if currentHandPoseRotationAngle - neutralHandPoseRotationAngle < exerciseData["parts"][exercisePart]["angles"]["score_1_min_diff"] and score[exercisePart] >= 1:
                        break
                        
        return score, None
    def scoreBodyExercise(camera, bodyPoseDetection, exerciseData):
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
            userInView = FuglMeyer.areBodyPartsInView(exerciseData, bodyPoseDetection, poseLandmarks)
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
            userHasCorrectBodyPose = False
            for bodyPartData in currentBodyPose:
                plane = ExerciseDataReader.getPlaneForBodyPart(exerciseData, currentExercisePart, diff["body_part"])
                currentBodyPartAngle = bodyPartData["heading"][plane]
                maxScoreAngles = ExerciseDataReader.getCorrectBodyPartAngleOffsets(exerciseData, currentExercisePart, diff["body_part"])
                print(maxScoreAngles)
                print(currentBodyPartAngle)
                if maxScoreAngles[0] > currentBodyPartAngle and currentBodyPartAngle > maxScoreAngles[1]:
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
        return score, json.dumps(metadata.getMetadata(), indent=4)
    def scoreHandExercise(camera, handPoseDetection, exerciseData):
        exerciseStarted = False
        exerciseData = json.loads(exerciseData)
        score = [0, 0] # [first part, second part]
        currentExercisePart = 0
        neutralHandPoseCreator = HandPose()
        currentHandPoseCreator = HandPose()
        neutralHandPose = [None, None]
        relevantHandPartTypeStrings = [[], []]
        for exercisePart in range(len(exerciseData["parts"])):
            for handPartData in exerciseData["parts"][exercisePart]:
                handPartTypeString = HandPartType.serialize(handPartData["hand_part"])
                relevantHandPartTypeStrings[exercisePart].append(handPartTypeString)
        startTime = int(time()*1000) # in ms
        print("hand exercise")
        print(exerciseData)
        while True:
            ###
            # Get camera frame
            ###
            frame = camera.getFrame()
            ###
            # Detect hand pose (mediapipe)
            ###
            frame_start = time()*1000
            poseLandmarks = handPoseDetection.getPose(frame)
            frame_end = time()*1000
            FPS = int(1000/(frame_end-frame_start))
            frame = cv2.flip(frame, 1)
            cv2.putText(frame, "FPS: "+str(FPS), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2, cv2.LINE_AA)
            cv2.imshow('hand frame', frame)
            if cv2.waitKey(1) == ord('q'):
                currentExercisePart += 1
                if currentExercisePart >= 2:
                    break
                else:
                    print("Onto the next side we go!")
            ###
            # Is the required hand in frame?
            ###
            handInView, _ = currentHandPoseCreator.isHandInView(poseLandmarks, HandType.serialize(exerciseData["parts"][currentExercisePart][0]["hand"]))
            if not handInView:
                print("Hand is not in view")
                continue
            ###
            # Has exercise been started?
            ###
            if handInView and exerciseStarted == False:
                exerciseStarted = True
                continue
            ###
            # Does user want to quit?
            ###
            # TODO: FIND OUT HOW TO DO THIS IN PRODUCTION! WE NEED SOME SORT OF API/DBUS SYSTEM FOR THIS!
            ###
            # Create neutral pose if it doesn't exist
            ###
            if neutralHandPose[currentExercisePart] is None:
                print("CREATING NEUTRAL POSE SNAPSHOT!")
                neutralHandPose[currentExercisePart] = neutralHandPoseCreator.createPose(poseLandmarks, HandType.serialize(exerciseData["parts"][currentExercisePart][0]["hand"]), relevantHandPartTypeStrings[currentExercisePart])
            else:
                print("SNAPSHOT WAS MADE")
            ###
            # Create a current handpose snapshot
            ###
            currentHandPose = currentHandPoseCreator.createPose(poseLandmarks, HandType.serialize(exerciseData["parts"][currentExercisePart][0]["hand"]), relevantHandPartTypeStrings[currentExercisePart])
            ###
            # See if the user moved (score 1)
            ###
            handPoseDiffs = HandPose.getDiffs(currentHandPose, neutralHandPose[currentExercisePart])
            for diff in handPoseDiffs:
                plane = ExerciseDataReader.getPlaneForHandPart(exerciseData, currentExercisePart, diff["hand_part"])
                if diff["heading"][plane]>20:
                    if score[currentExercisePart] < 1:
                        score[currentExercisePart] = 1
            if score[currentExercisePart]:
                print("USER SCORED 1!")
            ###
            # See if the user's hand position is close to the correct one (score 2)
            # TODO: FIX THIS!
            ###
            userHasCorrectHandPose = False
            for handPartData in currentHandPose:
                try:
                    plane = ExerciseDataReader.getPlaneForHandPart(exerciseData, currentExercisePart, diff["hand_part"])
                    currentHandPartAngle = handPartData["heading"][plane]
                    maxScoreAngles = ExerciseDataReader.getCorrectHandPartAngleOffsets(exerciseData, currentExercisePart, diff["hand_part"])
                    print("FUCK:", currentHandPartAngle, maxScoreAngles)
                    if maxScoreAngles[0] < currentHandPartAngle and currentHandPartAngle < maxScoreAngles[1]:
                        userHasCorrectHandPose = True
                    else:
                        userHasCorrectHandPose = False
                        break
                except:
                    continue
            if userHasCorrectHandPose:
                print("USER SCORED 2!")
                score[currentExercisePart] = 2
            ###
            # See if the user moved back to neutral position before moving on
            ###
            handPoseDiffs = HandPose.getDiffs(currentHandPose, neutralHandPose[currentExercisePart])
            userInNeutralPosition = False
            print("exercise part", currentExercisePart)
            print("score:", score[currentExercisePart])
            if score[currentExercisePart] > 0:
                userInNeutralPosition = True
                for diff in handPoseDiffs:
                    if diff["heading"]["xy"]>20:
                        userInNeutralPosition = False
            if userInNeutralPosition:
                currentExercisePart+=1
            if currentExercisePart >= 2:
                print("all done!")
                break
        return score, None