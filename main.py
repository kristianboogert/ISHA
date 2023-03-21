from poseDetection.Camera import Camera
from poseDetection.BodyPoseDetection import BodyPoseDetection
from poseDetection.HandPoseDetection import HandPoseDetection
from poseDetection.BodyPart import *
from poseDetection.HandPart import *
from stereoscopic.DepthImage import DepthImage
from dataExporter.ExcelExporter import *

import cv2

def hand_test(camera, handPoseDetection):
    # Hand test
    current_testphase = 0
    highest_rotation = 0
    neutral_position = 0
    testphases = ["image_capture", "neutral_position", "rotation", "end"]
    print("Put left hand in front of screen")
    while True:
        frame = camera.getFrame()
        if cv2.waitKey(1) == ord('q'):
            break
        cv2.imshow('hand frame', cv2.flip(frame, 1))
        poseData = handPoseDetection.getPose(frame)
        poseFrame = handPoseDetection.drawPose(frame, poseData)
        cv2.imshow('hand frame', cv2.flip(poseFrame, 1))
        if cv2.waitKey(1) == ord('q'):
            break
        if testphases[current_testphase] == "image_capture":
            landmark = handPoseDetection.getHandLandmark(poseData, Hand.LEFT_HAND, HandPart.WRIST)
            if landmark is not None:
                print("Done!")
                print("Put hand in neutral position")
                current_testphase+=1
        if testphases[current_testphase] == "neutral_position":
            landmark = handPoseDetection.getHandLandmark(poseData, Hand.LEFT_HAND, HandPart.WRIST)
            handRotation = handPoseDetection.getHandRotation(Hand.LEFT_HAND, poseData)
            if handRotation is not None and abs(handRotation) < 15:
                print("Done!")
                print("Rotate hand 180 degrees and return it to neutral position")
                handRotation = handPoseDetection.getHandRotation(Hand.LEFT_HAND, poseData)
                neutral_position = handRotation
                current_testphase = 3
        else:
            handRotation = handPoseDetection.getHandRotation(Hand.LEFT_HAND, poseData)
            print(handRotation)
                
        # if testphases[current_testphase] == "rotation":
        #     landmark = handPoseDetection.getHandLandmark(poseData, Hand.LEFT_HAND, HandPart.WRIST)
        #     handRotation = handPoseDetection.getHandRotation(Hand.LEFT_HAND, poseData)
        #     if handRotation is not None and handRotation > highest_rotation:
        #         highest_rotation = handRotation
        #     if highest_rotation > 25 and (handRotation is None or abs(handRotation) < 25):
        #         print("Done!")
        #         print("Neutral position:", neutral_position)
        #         print("Highest measured hand rotation:", highest_rotation)
        #         return

def arm_side_test(camera, bodyPoseDetection):
    testphases = ["image_capture", "neutral_position", "rotation", "end"]
    highest_arm_angle = -999999999
    current_testphase = 0
    # print("Put right arm in front of screen")
    while True:
        frame = camera.getFrame()
        poseData = bodyPoseDetection.getPose(frame)
        poseFrame = bodyPoseDetection.drawPose(frame, poseData)
        cv2.imshow('body frame', cv2.flip(poseFrame, 1))
        if cv2.waitKey(1) == ord('q'):
            break
        landmark = bodyPoseDetection.getPoseLandmark(BodyPart.RIGHT_ELBOW, poseData)
        upper_arm_rotation = bodyPoseDetection.getAnglesForBodyPart(BodyPart.RIGHT_ELBOW, poseData)
        # print(upper_arm_rotation[])
        try:
            print(int(90+upper_arm_rotation["xy"]), ",", int(upper_arm_rotation["yz"]), ",", int(upper_arm_rotation["xz"]))
        except:
            print(0)
            # if upper_arm_rotation is not None:
            #     print("Current rotation:", 90+upper_arm_rotation["xy"])
            # if upper_arm_rotation is not None and upper_arm_rotation["xy"] > highest_arm_angle:
            #     highest_arm_angle = upper_arm_rotation["xy"]
            # if upper_arm_rotation is not None and upper_arm_rotation["xy"] < -70 and highest_arm_angle > -60:
            #     # print("Done!")
            #     # print("Highest measured angle:", int(90+highest_arm_angle), "degrees")
            #     return
        # elif current_testphase > len(testphases):
        #     print("Error! testphase:", current_testphase)
        #     exit(1)

def right_arm_angle_excel_test(camera, bodyPoseDetection):
    data = [[], [], []]
    while True:
        frame = camera.getFrame()
        poseData = bodyPoseDetection.getPose(frame)
        poseFrame = bodyPoseDetection.drawPose(frame, poseData)
        cv2.imshow('body frame', cv2.flip(poseFrame, 1))
        if cv2.waitKey(1) == ord('q'):
            break
        landmark = bodyPoseDetection.getPoseLandmark(BodyPart.RIGHT_ELBOW, poseData)
        upper_arm_rotation = bodyPoseDetection.getAnglesForBodyPart(BodyPart.RIGHT_ELBOW, poseData)
        try:
            data[0].append(upper_arm_rotation["xy"])
            data[1].append(upper_arm_rotation["yz"])
            data[2].append(upper_arm_rotation["xz"])
        except:
            data[0].append(None)
            data[1].append(None)
            data[2].append(None)
    export_to_line_chart("data.xlsx", data)

def main():
    camera = Camera(cameraId=0)           # if using a webcam
    camera.start()
    bodyPoseDetection = BodyPoseDetection(displayPose=True)
    right_arm_angle_excel_test(camera, bodyPoseDetection)

    # # camera2 = Camera(cameraId=1)           # if using a webcam
    # # camera2.start()
    # bodyPoseDetection = BodyPoseDetection(displayPose=True)
    # handPoseDetection = HandPoseDetection(displayPose=True)
    # depthImage = DepthImage()
    # arm_side_test(camera, bodyPoseDetection)
    # # hand_test(camera, handPoseDetection)
    # # right_arm_angle_live(camera, bodyPoseDetection)
   
    # camera.stop()
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
