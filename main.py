from poseDetection.Camera import Camera
from poseDetection.BodyPoseDetection import BodyPoseDetection
from poseDetection.HandPoseDetection import HandPoseDetection
from poseDetection.BodyPart import *
from poseDetection.HandPart import *
from stereoscopic.DepthImage import DepthImage
# from exercise.FuglMeyer import FuglMeyer

import cv2

def main():
    camera = Camera(cameraId=0)           # if using a webcam
    camera.start()
    # camera2 = Camera(cameraId=1)           # if using a webcam
    # camera2.start()
    bodyPoseDetection = BodyPoseDetection(displayPose=True)
    handPoseDetection = HandPoseDetection(displayPose=True)
    depthImage = DepthImage()
    testphases = ["image_capture", "neutral_position", "hand_rotation", "end"]
    current_testphase = 0
    highest_rotation = 0
    print("Put hand in front of screen")
    while True:
        frame = camera.getFrame()
        if cv2.waitKey(1) == ord('q'):
            break
        cv2.imshow('hand frame', cv2.flip(frame, 1))
        poseData = handPoseDetection.getPose(frame)
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
                current_testphase+=1
        if testphases[current_testphase] == "hand_rotation":
            landmark = handPoseDetection.getHandLandmark(poseData, Hand.LEFT_HAND, HandPart.WRIST)
            handRotation = handPoseDetection.getHandRotation(Hand.LEFT_HAND, poseData)
            if handRotation > highest_rotation:
                highest_rotation = handRotation
            if highest_rotation > 25 and (handRotation is None or abs(handRotation) < 25):
                print("Done!")
                print("Highest measured hand rotation:", highest_rotation)
                exit(0)
    camera.stop()
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
            # hand_rotation = handPoseDetection.getHandRotation(Hand.LEFT_HAND, handPoseData)
            # print("hand_rotation:", hand_rotation)
            # # cv2.imshow('body frame', cv2.flip(bodyFrame, 1))
            # cv2.imshow('hand frame', cv2.flip(handFrame, 1))
            # if cv2.waitKey(1) == ord('q'):
            #     break