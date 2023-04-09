# from ..poseDetection.HandPoseDetection import HandPoseDetection
# from ..poseDetection.Camera import Camera

import sys
import json
import time
sys.path.append("..")
from poseDetection.HandPoseDetection import *
from poseDetection.HandPart import *
from poseDetection.BodyPart import *

### niet-fugl-meyer oefeningen:
#schuiven arm over tafel  (oefening 22)
#hand omdraaien           (oefening 10: alleen de eerste 3)
#spreiden sluiten vingers (oefening 9: alleen de eerste, voor de leuk ook de tweede)
###

class FuglMeyer:
    def __init__(self):
        self.none = None
    def landmarksAreVisible(self, landmarks, visibilityThreshold=0.85):
        for landmark in landmarks:
            if landmark is None or landmark.visibility < visibilityThreshold:
                return False
        return True
    def scoreExercisePart(self, camera, bodyPoseDetection, exerciseData, visibilityThreshold=0.85):
        exerciseStarted = False
        exerciseData = json.loads(exerciseData)
        score = [0, 0] # [left side, right side]
        exercisePart = 0
        neutralBodyPose = None # TODO: save the neutral pose for later comparison, so a core of 1 can be generated
        while True:
            ###
            # Get camera frame
            ###
            frame = camera.getFrame()
            ###
            # Detect body pose (mediapipe)
            ###
            poseData = bodyPoseDetection.getPose(frame)
            frame = bodyPoseDetection.drawPose(frame, poseData)
            cv2.imshow('body frame', cv2.flip(frame, 1))
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
                print("user is not in view")
                continue
            ###
            # Has exercise been started?
            ###
            if user_in_view == True and exerciseStarted == False:
                exerciseStarted = True
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
                currentBodyPart = bodyPoseDetection.getAnglesForBodyPart(bodyPart["body_part"], poseData)
                if currentBodyPart is None:
                    print(time.time(), "Skipping frame, because user is not fully in view anymore (?)")
                    break
                currentBodyPartAngle = currentBodyPart[bodyPart["angles"]["plane"]]
                givenAngles = bodyPart["angles"]
                # print("CURRENT_ANGLE:", currentBodyPartAngle)
                # print("GIVEN ANGLES: ", givenAngles)
                if givenAngles["score_2_min"] < currentBodyPartAngle < givenAngles["score_2_max"]:
                    print(time.time(), "user scored 2 on bodypart:", _bodyPart.serialize(bodyPart["body_part"]))
                    score[exercisePart] = 2
                else:
                    if score[exercisePart] == 2:
                        score[exercisePart] = 1
            if score[exercisePart] == 2:
                exercisePart += 1
                if exercisePart >= 2:
                    break
                else:
                    print("Onto the next side we go!")
            ###
            # Relevant joints are close to neutral position?
            ###
            # TODO: DIT VEREIST OOK DAT WE DE RUSTPOSITIE INLEZEN VOORDAT DE OEFENING WORDT BEGONNEN!!!!
        return score







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
