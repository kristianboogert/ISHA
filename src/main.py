import requests
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
# import stitching # niet meer nodig
import requests

def main():
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




    # # Read JSON containing an exerciseDescription
    # # exerciseDescriptionFilepath = "./exerciseDescriptions/arm_to_side.json"    # body pose exercise demo
    # # exerciseDescriptionFilepath = "./exerciseDescriptions/hand_rotation.json"  # hand rotation exercise demo
    # exerciseDescriptionFilepath = "./exerciseDescriptions/fist.json"           # hand exercise demo

    # exerciseDescription = open(exerciseDescriptionFilepath).read()
    # print(exerciseDescription)
    # # Convert the exerciseDescription to exerciseData, so the pose detection can just follow instructions,
    # # without having any real world knowlegde
    # exerciseData = ExerciseDataCreator.createExerciseData(exerciseDescription, ImpairedSideType.LEFT)
    # # Initialize camera. If camera.start() is not called, it will not give frames. Same goes for camera.stop()
    camera = Camera(cameraId=0)
    camera.start()
    # Initialize pose detections
    bodyPoseDetection = BodyPoseDetection()

    metadata = [[], [], [], []];

    while True:
        frame=camera.getFrame()
        frame2 = cv2.flip(frame, 1)
        bodyPoseData = bodyPoseDetection.getPose(camera.getFrame())
        bodyPose = BodyPose()
        bodyPose.createPose(bodyPoseData, ['LEFT_UPPER_ARM'])
        print(bodyPose.getBodyPose())
        try:
            xy_heading = bodyPose.getBodyPose()[0]["heading"]["xy"] # dit is breedte
            xz_heading = bodyPose.getBodyPose()[0]["heading"]["xz"]
            yz_heading = bodyPose.getBodyPose()[0]["heading"]["yz"] # dit is diepte
        except:
            xy_heading = "??"
            xz_heading = "??"
            yz_heading = "??"
        cv2.putText(frame2, "xy_heading: "+str(xy_heading), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1, cv2.LINE_AA)
        cv2.putText(frame2, "xz_heading: "+str(xz_heading), (0,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1, cv2.LINE_AA)
        cv2.putText(frame2, "yz_heading: "+str(yz_heading), (0,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1, cv2.LINE_AA)
        cv2.imshow('frame', frame2)
        metadata[0].append(xy_heading)
        metadata[1].append(xz_heading)
        metadata[2].append(yz_heading)
        metadata[3].append(int(time()))
        if cv2.waitKey(1) == ord('q'):
            break

    # debug/demo function
    export_to_line_chart("demo1.xlsx", metadata)

    exit(1)

    # handPoseDetection = HandPoseDetection()

    # # Try to get a score by looking at a user's movements
    # print(exerciseData)
    # score, pose_metadata = FuglMeyer.scoreExercise(camera, bodyPoseDetection, handPoseDetection, exerciseData)
    # print(pose_metadata)
    # print(score)





    pose_metadata_txt = open("real_exercise_data.json").read()
    print(pose_metadata_txt)
    pose_metadata = json.loads(pose_metadata_txt)
    print(pose_metadata)
    # url moet nog verbeterd, maar zou moeten werken
    url = 'http://127.0.0.1:8000/metadata'
    for exercisePart in pose_metadata["exercise_parts"]:
        for bodyPart in exercisePart:
            dict_thing = {
                "bodypart_name": bodyPart["body_part"],
                "bodypart_angle_xy": bodyPart["angles"]["xy"],
                "bodypart_angle_yz": bodyPart["angles"]["yz"],
                "bodypart_angle_xz": bodyPart["angles"]["xz"],
                "score_id": 1
            }
            # make the post request
            response = requests.post(url, json = dict_thing)
            if response is not None:
                print(response.text)
            else:
                print("alles ging fout")
main()