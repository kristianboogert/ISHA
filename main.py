from poseDetection.Camera import Camera
from poseDetection.BodyPoseDetection import BodyPoseDetection
from poseDetection.HandPoseDetection import HandPoseDetection
from poseDetection.BodyPart import *
from poseDetection.HandPart import *
from stereoscopic.DepthImage import DepthImage

import cv2

def main():
    camera = Camera(cameraId=0)           # if using a webcam
    camera.start()
    # camera2 = Camera(cameraId=1)           # if using a webcam
    # camera2.start()
    bodyPoseDetection = BodyPoseDetection(displayPose=True)
    handPoseDetection = HandPoseDetection(displayPose=True)
    depthImage = DepthImage()
    while True:
        frame = camera.getFrame()
        print(frame)
        try:
            while True:
                color_frame, _ = camera.getFrame()
                # color_frame2, _ = camera2.getFrame()
                # depth_image = depthImage.create(color_frame, color_frame2)
                # cv2.imshow('depth_image', depth_image)
                bodyPoseData, bodyFrame = bodyPoseDetection.getPose(color_frame)
                handPoseData, handFrame = handPoseDetection.getPose(color_frame)
                left_index = handPoseDetection.getHandLandmark(handPoseData, Hand.LEFT_HAND, HandPart.INDEX_FINGER_TIP)
                right_index = handPoseDetection.getHandLandmark(handPoseData, Hand.RIGHT_HAND, HandPart.INDEX_FINGER_TIP)
                vector = handPoseDetection.getDirectionVector(left_index, right_index)
                hand_rotation = handPoseDetection.getHandRotation(Hand.LEFT_HAND, handPoseData)
                print("hand_rotation:", hand_rotation)
                # cv2.imshow('body frame', cv2.flip(bodyFrame, 1))
                cv2.imshow('hand frame', cv2.flip(handFrame, 1))
                if cv2.waitKey(1) == ord('q'):
                    break
        finally:
            camera.stop()
main()
