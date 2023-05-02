from poseDetection.Camera import Camera
from poseDetection.BodyPoseDetection import BodyPoseDetection
from poseDetection.HandPoseDetection import HandPoseDetection
from poseDetection.BodyPart import *
from poseDetection.HandType import *
from poseDetection.HandPartType import *
from poseDetection.HandJoint import HandJoint
from poseDetection.HandPart import HandPart
from poseDetection.HandJointType import *
from stereoscopic.DepthImage import DepthImage
from dataExporter.ExcelExporter import *
from poseDetection.BodyJointType import *
from poseDetection.BodyJoint import BodyJoint
from poseDetection.BodyPartType import *
from poseDetection.BodyPart import BodyPart
from poseDetection.BodyPose import BodyPose
from exerciseScorer.FuglMeyer import FuglMeyer
from exerciseCreator.ExerciseCreator import ExerciseCreator, ImpairedSide, PoseDetectionType, BodyPartDescription
from time import time
from time import sleep
import cv2
import stitching

def main():
    # camera = Camera(cameraId=0)
    # camera.start()
    # # hand pose demo!
    # handPoseDetection = HandPoseDetection()
    # while True:
    #     frame = camera.getFrame()
    #     handPoseData = handPoseDetection.getPose(frame)
    #     handPartLeftIndexBase = HandPart.createFromLandmarks(handPoseData, HandType.LEFT_HAND, HandPartType.INDEX_FINGER_BASE)
    #     handPartLeftIndexTip = HandPart.createFromLandmarks(handPoseData, HandType.LEFT_HAND, HandPartType.INDEX_FINGER_TIP)
    #     try:
    #         print(handPartLeftIndexBase.getHeading())
    #         print(handPartLeftIndexTip.getHeading())
    #     except:
    #         continue




    # BODY POSE DEMO!
    exerciseCreator = ExerciseCreator()
    exerciseDescription = '\
    {\
        "name": "Raise arm to side",\
        "pose_detection_type": "body_pose",\
        "body_parts":\
        [\
            {\
                "body_part": "upper_arm",\
                "angles":\
                {\
                    "plane": "xy",\
                    "score_1_min_diff": 20,\
                    "score_2_min": -15,\
                    "score_2_max": 15\
                }\
            },\
            {\
                "body_part": "forearm",\
                "angles":\
                {\
                    "plane": "xy",\
                    "score_1_min_diff": 20,\
                    "score_2_min": -15,\
                    "score_2_max": 15\
                }\
            }\
        ]\
    }\
    '

    exerciseData = exerciseCreator.createExercise(exerciseDescription, ImpairedSide.RIGHT)
    print("exerciseData:", exerciseData)
    camera = Camera(cameraId=0)
    camera.start()
    bodyPoseDetection = BodyPoseDetection()
    fuglMeyer = FuglMeyer()
    score, metadata = fuglMeyer.scoreExercisePart(camera, bodyPoseDetection, exerciseData, visibilityThreshold=0.85)
    print(metadata)
    print(score)
main()