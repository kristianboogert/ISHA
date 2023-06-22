from poseDetection.Camera import Camera
from poseDetection.BodyPoseDetection import BodyPoseDetection
from poseDetection.BodyPose import BodyPose
from poseDetection.BodyPartType import *
from poseDetection.BodyJointType import *
from Timer.Timer import Timer
import cv2
from time import time, sleep
#####
###
# Voeg een oefening toe door deze zelf te doen
###
#####

def areShouldersStraight(bodyPoseDetection, frame):
    # Detect if shoulders are straight
    frame = cv2.flip(frame, 1)
    poseLandmarks = bodyPoseDetection.getPose(frame)
    leftShoulderAngles = bodyPoseDetection.getAnglesForBodyPart(BodyPartType.LEFT_SHOULDER, poseLandmarks)
    if leftShoulderAngles is not None:
        if abs(leftShoulderAngles["xy"]) < 10:
            return True
    return False

def userIsFacingTheCamera(bodyPoseDetection, frame):
    frame = cv2.flip(frame, 1)
    poseLandmarks = bodyPoseDetection.getPose(frame)
    leftShoulderAngles = bodyPoseDetection.getAnglesForBodyPart(BodyPartType.LEFT_SHOULDER, poseLandmarks)
    if leftShoulderAngles is not None:
        if abs(leftShoulderAngles["xz"]) < 35:
            # The shoulders are correct, but the user could be rotated 180 degrees. So, check if the nose is in view.
            if bodyPoseDetection._getPoseLandmark(BodyJointType.NOSE, poseLandmarks) is not None:
                return True
    return False

def isUserReady(bodyPoseDetection, frame):
    return areShouldersStraight(bodyPoseDetection, frame) and userIsFacingTheCamera(bodyPoseDetection, frame)

def convertBodyPartToDescription(bodyPartTypeString):
    if bodyPartTypeString == "LEFT_UPPER_ARM" or bodyPartTypeString == "RIGHT_UPPER_ARM":
        return "UPPER_ARM"
    if bodyPartTypeString == "LEFT_FOREARM" or bodyPartTypeString == "RIGHT_FOREARM":
        return "FOREARM"

def getCorrectHeadingForBodyPart(correctBodyPose, bodyPartDescriptionString):
    for item in correctBodyPose:
        print(item)
        if convertBodyPartToDescription(BodyPartType.serialize(item["body_part"])) == bodyPartDescriptionString:
            print("yes")
            return item["heading"]
    return None

# eerst maximaal (dus met overshoot)
# dan minimaal (dus met undershoot)
# score 1 blijft hetzelfde

def bodyPartExists(out, bodyPartDescriptionString):
    for item in out["body_parts"]:
        if item["body_part"] == bodyPartDescriptionString:
            return True
    return False

def convertPoseToDescription(correctBodyPose):
    out = {}
    out.update({"name": "test"})
    out.update({"pose_detection_type": "body_pose"})
    out.update({"body_parts": []})

    print(json.dumps(correctBodyPose.getBodyPose(), indent=4))
    for item in correctBodyPose.getBodyPose():
        print(item)
        # convert body part type to a description
        bodyPartDescriptionString = convertBodyPartToDescription(BodyPartType.serialize(item["body_part"]))
        print(bodyPartDescriptionString)
        # make sure there are no duplicates
        if bodyPartExists(out, bodyPartDescriptionString):
            continue
        # get headings
        correctHeading = getCorrectHeadingForBodyPart(correctBodyPose.getBodyPose(), bodyPartDescriptionString)
        # Build a body_part entry
        for plane in ["xy", "yz", "xz"]:
            # create a body part entry per plane
            body_part_entry = {
                "body_part": bodyPartDescriptionString,
                "angles": {
                    "plane": plane,
                    "score_1_min_diff": 20,
                    "score_2_min": correctHeading[plane]-20,
                    "score_2_max": correctHeading[plane]+20
                }
            }
            # add body part entry to out
            out["body_parts"].append(body_part_entry)
    return out
        




def main():
    camera = Camera(cameraId=0)
    camera.start()
    bodyPoseDetection = BodyPoseDetection()
    startPose = BodyPose()
    currentPose = BodyPose()
    timer = Timer()

    started = False
    while True:
        frame = camera.getFrame()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            exit(0)
        if not isUserReady(bodyPoseDetection, frame):
            print(str(time())+": Please face the camera and sit up straight")
            continue
        elif started == False:
            started = True
            print("Please provide the correct body pose for the new exercise")
            for counter in range(5):
                print(5-counter)
                sleep(1)
        poseLandmarks = bodyPoseDetection.getPose(frame)
        currentPose.createPose(poseLandmarks, ["LEFT_UPPER_ARM", "LEFT_FOREARM", "RIGHT_UPPER_ARM", "RIGHT_FOREARM"])
        diffs = BodyPose.getDiffs(startPose.getBodyPose(), currentPose.getBodyPose())
        if BodyPose.isPoseSimilar(diffs):
            if not timer.isRunning():
                timer.setIntervalMs(2500)
                timer.start()
            elif timer.hasElapsed():
                print(json.dumps(convertPoseToDescription(currentPose), indent=4))
                exit(1)
            else:
                print("Please hold this pose!")
        else:
            print(time(),": User moved")
            startPose.setBodyPose(currentPose.getBodyPose())
            timer.stop()
main()


# {
#     "name": "Raise arm to side",
#     "pose_detection_type": "body_pose",
#     "body_parts":
#     [
#         {
#             "body_part": "upper_arm",
#             "angles":
#             {
#                 "plane": "xy",
#                 "score_1_min_diff": 20,
#                 "score_2_min": -15,
#                 "score_2_max": 15
#             }
#         },
#         {
#             "body_part": "forearm",
#             "angles":
#             {
#                 "plane": "xy",
#                 "score_1_min_diff": 20,
#                 "score_2_min": -15,
#                 "score_2_max": 15
#             }
#         }
#     ]
# }