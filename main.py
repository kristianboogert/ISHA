from poseDetection.Camera import Camera
from poseDetection.BodyPoseDetection import BodyPoseDetection
from poseDetection.HandPoseDetection import HandPoseDetection
from poseDetection.BodyPart import *
from poseDetection.HandPart import *
from stereoscopic.DepthImage import DepthImage
from dataExporter.ExcelExporter import *
from exercise.FuglMeyer import FuglMeyer

import cv2

def right_arm_angle_excel_test(camera, bodyPoseDetection, bodyPart):
    data = [[], [], []]
    while True:
        frame = camera.getFrame()
        poseData = bodyPoseDetection.getPose(frame)
        poseFrame = bodyPoseDetection.drawPose(frame, poseData)
        cv2.imshow('body frame', cv2.flip(poseFrame, 1))
        if cv2.waitKey(1) == ord('q'):
            break
        landmark = bodyPoseDetection.getPoseLandmark(bodyPart, poseData)
        upper_arm_rotation = bodyPoseDetection.getAnglesForBodyPart(bodyPart, poseData)
        try:
            data[0].append(upper_arm_rotation["xy"])
            data[1].append(upper_arm_rotation["yz"])
            data[2].append(upper_arm_rotation["xz"])
        except:
            data[0].append(None)
            data[1].append(None)
            data[2].append(None)
    export_to_line_chart("data.xlsx", data)

def finger_tracker_excel_test(camera, handPoseDetection, hand, handPart):
    data = [[], [], []]
    while True:
        frame = camera.getFrame()
        handPoseData = handPoseDetection.getPose(frame)
        cv2.imshow('body frame', cv2.flip(frame, 1))
        if cv2.waitKey(1) == ord('q'):
            break
        landmark = handPoseDetection.getHandLandmark(hand, handPart, handPoseData)
        hand_angle = handPoseDetection.getAnglesForHandPart(hand, HandPart.INDEX_FINGER_MCP, handPoseData)
        angles = handPoseDetection.getAnglesForHandPart(hand, handPart, handPoseData)
        try:
            data[0].append(angles["xy"])
            data[1].append(angles["yz"])
            data[2].append(angles["xz"])
        except:
            data[0].append(None)
            data[1].append(None)
            data[2].append(None)
    export_to_line_chart("data.xlsx", data)

def main():
    fuglMeyer = FuglMeyer()
    camera = Camera(cameraId=0)           # if using a webcam
    camera.start()
    bodyPoseDetection = BodyPoseDetection()
    # handPoseDetection = HandPoseDetection()
    fuglMeyer.exerciseRaiseArmToSide(camera, bodyPoseDetection, BodyPart.LEFT_ELBOW)
main()






















        # while True:
            # color_frame, _ = camera.getFrame()
            # # color_frame2, _ = camera2.getFrame()
            # # depth_image = depthImage.create(color_frame, color_frame2)
            # # cv2.imshow('depth_image', depth_image)
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
