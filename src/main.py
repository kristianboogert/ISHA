from poseDetection.Camera import Camera
from dataExporter.ExcelExporter import *
from poseDetection.BodyPoseDetection import BodyPoseDetection
from poseDetection.BodyJointType import *
from poseDetection.BodyJoint import BodyJoint
from poseDetection.BodyPartType import *
from poseDetection.BodyPart import BodyPart
from poseDetection.BodyPose import BodyPose
from poseDetection.HandPoseDetection import HandPoseDetection
from poseDetection.HandType import *
from poseDetection.HandPartType import *
from poseDetection.HandJoint import HandJoint
from poseDetection.HandPart import HandPart
from poseDetection.HandPose import HandPose
from poseDetection.HandJointType import *
from exerciseScorer.FuglMeyer import FuglMeyer
from exerciseDataCreator.ImpairedSideType import ImpairedSideType
from exerciseDataCreator.PoseDetectionType import PoseDetectionType
from exerciseDataCreator.BodyPartDescriptionType import BodyPartDescriptionType
from exerciseDataCreator.ExerciseDataCreator import ExerciseDataCreator
from time import time
from time import sleep
import cv2
import requests

def getScoreForBodyPart(bodyPartType, frame, bodyPoseDetection):
    frame = cv2.flip(frame, 1)
    poseData = bodyPoseDetection.getPose(frame)
    angles = bodyPoseDetection.getAnglesForBodyPart(bodyPartType, poseData)
    if angles is None:
        return 0, "??"
    xyAngle = angles["xy"]
    score = 0
    if xyAngle > -90+20:
        score = 1
    if abs(xyAngle) < 20:
        score = 2
    return score, xyAngle

# This function checks if a user is sitting up straight,
# and is not leaning to the left or right.
def areShouldersStraight(bodyPoseDetection, frame):
    # Detect if shoulders are straight
    frame = cv2.flip(frame, 1)
    poseLandmarks = bodyPoseDetection.getPose(frame)
    leftShoulderAngles = bodyPoseDetection.getAnglesForBodyPart(BodyPartType.LEFT_SHOULDER, poseLandmarks)
    if leftShoulderAngles is not None:
        if abs(leftShoulderAngles["xy"]) < 10:
            return "ja"
    return "nee"

def userIsFacingTheCamera(bodyPoseDetection, frame):
    # Detect if shoulders are straight
    frame = cv2.flip(frame, 1)
    poseLandmarks = bodyPoseDetection.getPose(frame)
    leftShoulderAngles = bodyPoseDetection.getAnglesForBodyPart(BodyPartType.LEFT_SHOULDER, poseLandmarks)
    if leftShoulderAngles is not None:
        if abs(leftShoulderAngles["xz"]) < 25:
            # The shoulders are correct, but the user could be rotated 180 degrees. So, check if the nose is in view.
            if bodyPoseDetection._getPoseLandmark(BodyJointType.NOSE, poseLandmarks) is not None:
                return "ja"
    return "nee"

def main():
    # kleine interactieve demo
    print("Deze demo houdt geen rekening met een eventuele rust-houding")
    camera = Camera(cameraId=0)
    camera.start()
    bodyPoseDetection = BodyPoseDetection()
    bodyPartTypes = [BodyPartType.LEFT_UPPER_ARM, BodyPartType.LEFT_FOREARM, BodyPartType.RIGHT_UPPER_ARM, BodyPartType.RIGHT_FOREARM]

    while True:
        frame = camera.getFrame()
        frame = cv2.flip(frame, 1)
        shouldersStraight = areShouldersStraight(bodyPoseDetection, frame)
        cv2.putText(frame, "Schouders recht: "+str(shouldersStraight), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1, cv2.LINE_AA)
        facingCamera = userIsFacingTheCamera(bodyPoseDetection, frame)
        cv2.putText(frame, "Gebruiker naar camera gericht: "+str(facingCamera), (0,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1, cv2.LINE_AA)
        for index, bodyPartType in enumerate(bodyPartTypes):
            score, angle = getScoreForBodyPart(bodyPartType, frame, bodyPoseDetection)
            cv2.putText(frame, "Body part: "+BodyPartType.serialize(bodyPartType)+"; Score: "+str(score)+"; Hoek: "+str(angle), (0,50*(index+3)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            exit(0)
















    # # Read JSON containing an exerciseDescription
    exerciseDescriptionFilepath = "./exerciseDescriptions/arm_to_side.json"    # body pose exercise demo
    # # exerciseDescriptionFilepath = "./exerciseDescriptions/hand_rotation.json"  # hand rotation exercise demo
    # exerciseDescriptionFilepath = "./exerciseDescriptions/fist.json"           # hand exercise demo

    exerciseDescription = open(exerciseDescriptionFilepath).read()
    # print(exerciseDescription)
    # # Convert the exerciseDescription to exerciseData, so the pose detection can just follow instructions,
    # # without having any real world knowlegde
    exerciseData = ExerciseDataCreator.createExerciseData(exerciseDescription, ImpairedSideType.LEFT)
    # # Initialize camera. If camera.start() is not called, it will not give frames. Same goes for camera.stop()
    camera = Camera(cameraId=0)
    camera.start()
    # Initialize pose detections
    bodyPoseDetection = BodyPoseDetection()
    handPoseDetection = HandPoseDetection()

    metadata = [[], [], [], []]

    # Try to get a score by looking at a user's movements
    print(exerciseData)
    score, pose_metadata = FuglMeyer.scoreExercise(camera, bodyPoseDetection, handPoseDetection, exerciseData)
    print(pose_metadata)
    print(score)





    # pose_metadata_txt = open("real_exercise_data.json").read()
    # print(pose_metadata_txt)
    # pose_metadata = json.loads(pose_metadata_txt)
    # print(pose_metadata)
    # # url moet nog verbeterd, maar zou moeten werken
    # url = 'http://127.0.0.1:8000/metadata'
    # for exercisePart in pose_metadata["exercise_parts"]:
    #     for bodyPart in exercisePart:
    #         dict_thing = {
    #             "bodypart_name": bodyPart["body_part"],
    #             "bodypart_angle_xy": bodyPart["angles"]["xy"],
    #             "bodypart_angle_yz": bodyPart["angles"]["yz"],
    #             "bodypart_angle_xz": bodyPart["angles"]["xz"],
    #             "score_id": 1
    #         }
    #         # make the post request
    #         response = requests.post(url, json = dict_thing)
    #         if response is not None:
    #             print(response.text)
    #         else:
    #             print("alles ging fout")
main()























    # # HAND TEST
    # # camera = Camera(cameraId=0)
    # # camera.start()
    # # handPoseDetection = HandPoseDetection()
    # # handPoseL = HandPose()
    # # handPoseR = HandPose()
    # # while True:
    # #     poseLandmarks = handPoseDetection.getPose(camera.getFrame())
    # #     handPoseL.createPose(poseLandmarks, "LEFT_HAND", [])
    # #     print("L", handPoseL.getHandPose())
    # #     handPoseR.createPose(poseLandmarks, "RIGHT_HAND", [])
    # #     print("R", handPoseR.getHandPose())




    # # Read JSON containing an exerciseDescription
    # exerciseDescriptionFilepath = "./exerciseDescriptions/arm_to_side.json"    # body pose exercise demo
    # # exerciseDescriptionFilepath = "./exerciseDescriptions/hand_rotation.json"  # hand rotation exercise demo

    # exerciseDescription = open(exerciseDescriptionFilepath).read()
    # print(exerciseDescription)
    # # Convert the exerciseDescription to exerciseData, so the pose detection can just follow instructions,
    # # without having any real world knowlegde
    # exerciseData = ExerciseDataCreator.createExerciseData(exerciseDescription, ImpairedSideType.RIGHT)
    # # Initialize camera. If camera.start() is not called, it will not give frames. Same goes for camera.stop()
    # camera = Camera(cameraId=0)
    # camera.start()
    # # Initialize pose detections
    # bodyPoseDetection = BodyPoseDetection()
    # handPoseDetection = HandPoseDetection()


    # handPoseL = HandPose()
    # handPoseR = HandPose()
    # while True:
    #     poseLandmarks = handPoseDetection.getPose(camera.getFrame())
    #     handPoseL.createPose(poseLandmarks, "LEFT_HAND", [])
    #     print("L", handPoseL.getHandPose())
    #     handPoseR.createPose(poseLandmarks, "RIGHT_HAND", [])
    #     print("R", handPoseR.getHandPose())



