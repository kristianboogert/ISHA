from poseDetection.Camera import Camera
# from dataExporter.ExcelExporter import * # TODO: deze is op het moment stuk
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
import stitching

def main():
    # HAND TEST
    # camera = Camera(cameraId=0)
    # camera.start()
    # handPoseDetection = HandPoseDetection()
    # handPoseL = HandPose()
    # handPoseR = HandPose()
    # while True:
    #     poseLandmarks = handPoseDetection.getPose(camera.getFrame())
    #     handPoseL.createPose(poseLandmarks, "LEFT_HAND", [])
    #     print("L", handPoseL.getHandPose())
    #     handPoseR.createPose(poseLandmarks, "RIGHT_HAND", [])
    #     print("R", handPoseR.getHandPose())




    # Read JSON containing an exerciseDescription
    # exerciseDescriptionFilepath = "./exerciseDescriptions/arm_to_side.json"    # body pose exercise demo
    # exerciseDescriptionFilepath = "./exerciseDescriptions/hand_rotation.json"  # hand rotation exercise demo
    exerciseDescriptionFilepath = "./exerciseDescriptions/fist.json"           # hand exercise demo

    exerciseDescription = open(exerciseDescriptionFilepath).read()
    print(exerciseDescription)
    # Convert the exerciseDescription to exerciseData, so the pose detection can just follow instructions,
    # without having any real world knowlegde
    exerciseData = ExerciseDataCreator.createExerciseData(exerciseDescription, ImpairedSideType.LEFT)
    # Initialize camera. If camera.start() is not called, it will not give frames. Same goes for camera.stop()
    camera = Camera(cameraId=0)
    camera.start()
    # Initialize pose detections
    bodyPoseDetection = BodyPoseDetection()
    handPoseDetection = HandPoseDetection()
    # Try to get a score by looking at a user's movements
    print(exerciseData)
    score, pose_metadata = FuglMeyer.scoreExercise(camera, bodyPoseDetection, handPoseDetection, exerciseData)
    print(pose_metadata)
    print(score)
main()