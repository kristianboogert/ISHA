from poseDetection.Camera import Camera
from poseDetection.BodyPoseDetection import BodyPoseDetection
# from poseDetection.HandPoseDetection import HandPoseDetection # TODO!
from poseDetection.BodyPart import *
from poseDetection.HandPart import *
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

















































    # camera2 = Camera(cameraId=2)
    # camera2.start()
    # for _ in range(10):
    #     camera.getFrame()
    #     camera2.getFrame()
    # imgs = []
    # imgs.append(camera.getFrame());
    # imgs.append(camera2.getFrame());
    # for img in range(len(imgs)):
    #     cv2.imwrite("frame{}.jpg".format(img), imgs[img])
    # exit(1)
    # out = None
    # try:
    #     stitcher = cv2.createStitcher(True)
    # except:
    #     stitcher = cv2.Stitcher.create()
    # frame1 = camera.getFrame()
    # frame2 = camera2.getFrame()
    # cv2.imshow("frame1", frame1)
    # cv2.imshow("frame2", frame2)
    # cv2.waitKey(0)
    # result, out = stitcher.stitch((frame1, frame2))
    # print(result)
    # print(out)
    # cv2.imshow("camera", result)
    # cv2.waitKey(10000)
    # exit(1)















#
#
#
#
#
#
# def right_arm_angle_excel_test(camera, bodyPoseDetection, bodyPart):
#     data = [[], [], []]
#     while True:
#         frame = camera.getFrame()
#         poseData = bodyPoseDetection.getPose(frame)
#         poseFrame = bodyPoseDetection.drawPose(frame, poseData)
#         cv2.imshow('body frame', cv2.flip(poseFrame, 1))
#         if cv2.waitKey(1) == ord('q'):
#             break
#         landmark = bodyPoseDetection.getPoseLandmark(bodyPart, poseData)
#         upper_arm_rotation = bodyPoseDetection.getAnglesForBodyPart(bodyPart, poseData)
#         try:
#             data[0].append(upper_arm_rotation["xy"])
#             data[1].append(upper_arm_rotation["yz"])
#             data[2].append(upper_arm_rotation["xz"])
#         except:
#             data[0].append(None)
#             data[1].append(None)
#             data[2].append(None)
#     export_to_line_chart("data.xlsx", data)
#
# def finger_tracker_excel_test(camera, handPoseDetection, hand, handPart):
#     metadata = [[], [], [], []]
#     start_time = int(time()*1000) # in ms
#     while True:
#         frame = camera.getFrame()
#         handPoseData = handPoseDetection.getPose(frame)
#         poseFrame = handPoseDetection.drawPose(frame, handPoseData)
#         cv2.imshow('body frame', cv2.flip(poseFrame, 1))
#         if cv2.waitKey(1) == ord('q'):
#             break
#         landmark = handPoseDetection.getHandLandmark(hand, handPart, handPoseData)
#         hand_angle = handPoseDetection.getAnglesForHandPart(hand, HandPart.INDEX_FINGER_MCP, handPoseData)
#         angles = handPoseDetection.getAnglesForHandPart(hand, handPart, handPoseData)
#         current_time = int(time()*1000)
#         ms_since_start = current_time - start_time
#         try:
#             metadata[0].append(angles["xy"])
#             metadata[1].append(angles["yz"])
#             metadata[2].append(angles["xz"])
#             metadata[3].append(ms_since_start)
#         except:
#             metadata[0].append(None)
#             metadata[1].append(None)
#             metadata[2].append(None)
#             metadata[3].append(ms_since_start)
#     export_to_line_chart("finger_test.xlsx", data)
#
# # Test if we can see depth using only mediapipe
# def depth_excel_test(camera, bodyPoseDetection):
#     data = [[], [], [], []]
#     start_time = int(time()*1000) # in ms
#     while True:
#         frame = camera.getFrame()
#         poseData = bodyPoseDetection.getPose(frame)
#         poseFrame = bodyPoseDetection.drawPose(frame, poseData)
#         cv2.imshow('body frame', cv2.flip(poseFrame, 1))
#         if cv2.waitKey(1) == ord('q'):
#             break
#         nose_landmark = bodyPoseDetection.getPoseLandmark(BodyPart.NOSE, poseData)
#         right_shoulder_landmark = bodyPoseDetection.getPoseLandmark(BodyPart.RIGHT_SHOULDER, poseData)
#         directionVector = bodyPoseDetection.getDirectionVector(nose_landmark, right_shoulder_landmark)
#         angles = bodyPoseDetection.getAnglesFromDirectionVector(directionVector)
#         print(angles)
#         current_time = int(time()*1000)
#         ms_since_start = current_time - start_time
#         try:
#             data[0].append(angles["xy"])
#             data[1].append(angles["yz"])
#             data[2].append(angles["xz"])
#             data[3].append(ms_since_start)
#         except:
#             data[0].append(None)
#             data[1].append(None)
#             data[2].append(None)
#             data[3].append(ms_since_start)
#     export_to_line_chart("data_user_sitting_up_depth_test.xlsx", data)
#
#
#
#         # while True:
#             # color_frame, _ = camera.getFrame()
#             # # color_frame2, _ = camera2.getFrame()
#             # # depth_image = depthImage.create(color_frame, color_frame2)
#             # # cv2.imshow('depth_image', depth_image)
            # bodyPoseData, bodyFrame = bodyPoseDetection.getPose(color_frame)
            # handPoseData, handFrame = handPoseDetection.getPose(color_frame)
            # left_index = handPoseDetection.getHandLandmark(handPoseData, Hand.LEFT_HAND, HandPart.INDEX_FINGER_TIP)
            # right_index = handPoseDetection.getHandLandmark(handPoseData, Hand.RIGHT_HAND, HandPart.INDEX_FINGER_TIP)
            # vector = handPoseDetection.getDirectionVector(left_index, right_index)
            # hand_ron = handPoseDetection.getHandRotation(Hand.LEFT_HAND, handPoseData)
            # print("hand_rotation:", hand_rotation)
            # # cv2.imshow('body frame', cv2.flip(bodyFrame, 1))
            # cv2.imshow('hand frame', cv2.flip(handFrame, 1))
            # if cv2.waitKey(1) == ord('q'):
            #     break
