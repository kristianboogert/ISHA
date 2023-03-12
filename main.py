from poseDetection.Camera import Camera
from poseDetection.BodyPoseDetection import BodyPoseDetection
from poseDetection.HandPoseDetection import HandPoseDetection
from poseDetection.BodyPart import *
from poseDetection.HandPart import *

import cv2

def main():
    camera = Camera(cameraId=0)           # if using a webcam
    # camera = Camera(use_realsense=True) # if using a realsense camera
    camera.start()
    bodyPoseDetection = BodyPoseDetection(displayPose=True)
    handPoseDetection = HandPoseDetection(displayPose=True)
    while True:
        frame = camera.getFrame()
        print(frame)
        try:
            while True:
                color_frame, _ = camera.getFrame()
                bodyPoseData, bodyFrame = bodyPoseDetection.getPose(color_frame)
                handPoseData, handFrame = handPoseDetection.getPose(color_frame)
                left_index = handPoseDetection.getHandLandmark(handPoseData, Hand.LEFT_HAND, HandPart.INDEX_FINGER_TIP)
                right_index = handPoseDetection.getHandLandmark(handPoseData, Hand.RIGHT_HAND, HandPart.INDEX_FINGER_TIP)
                print(left_index, right_index)
                vector = handPoseDetection.getDirectionVector(left_index, right_index)
                angles = handPoseDetection.getAnglesFromDirectionVector(vector)
                print("vector:", vector)
                print("angles:", angles)
                try:
                    print("SITTING UP:", bodyPoseDetection.isSittingUp(bodyPoseData))
                    print("T POSING:  ", bodyPoseDetection.isTPosing(bodyPoseData))
                except:
                    pass
                cv2.imshow('body frame', cv2.flip(bodyFrame, 1))
                cv2.imshow('hand frame', cv2.flip(handFrame, 1))
                if cv2.waitKey(1) == ord('q'):
                    break
        finally:
            camera.stop()
main()
