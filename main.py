from poseDetection.Camera import Camera
from poseDetection.PoseDetection import PoseDetection
from poseDetection.BodyPart import *

import cv2

def main():
    camera = Camera(cameraId=0)
    # camera = Camera(use_realsense=True)
    camera.start()
    # preview = CameraPreview()
    # preview.show(camera)
    poseDetection = PoseDetection(display_pose=True)
    while True:
        frame = camera.getFrame()
        print(frame)
        try:
            while True:
                # color_frame, depth_frame = camera.getFrame()
                # poseData, handData, frame = poseDetection.getPose(color_frame)
                frame = camera.getFrame()
                poseData, handData, frame = poseDetection.getPose(frame)
                try:
                    print("SITTING UP:", poseDetection.isSittingUp(poseData))
                    print("T POSING:  ", poseDetection.isTPosing(poseData))
                except:
                    pass
                cv2.imshow('frame', cv2.flip(frame, 1))
                if cv2.waitKey(1) == ord('q'):
                    break
        finally:
            camera.stop()
main()
