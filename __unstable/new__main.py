from new__Camera import Camera
from new__CameraPreview import CameraPreview
from new__PoseDetection import BodyPart, PoseDetection

import cv2

def main():
    camera = Camera(cameraId=0)
    # camera = Camera(use_realsense=True)
    camera.start()
    preview = CameraPreview()
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
                # get torso angle
                lshoulderpos = poseDetection.getPoseLandmark(poseData, BodyPart.LEFT_SHOULDER)
                rshoulderpos = poseDetection.getPoseLandmark(poseData, BodyPart.RIGHT_SHOULDER)
                lelbowpos = poseDetection.getPoseLandmark(poseData, BodyPart.LEFT_ELBOW)
                relbowpos = poseDetection.getPoseLandmark(poseData, BodyPart.RIGHT_ELBOW)
                # print(poseDetection.getDirectionVectorForBodypart(BodyPart.LEFT_ELBOW, poseData))
                try:
                    angleData = poseDetection.getAnglesForBodyPart(BodyPart.RIGHT_WRIST, poseData)
                    print(angleData["xy"])
                    print(poseDetection.isTPosing(poseData))
                except:
                    pass
                print(poseDetection.isTPosing(poseData))
                cv2.imshow('frame', cv2.flip(frame, 1))
                if cv2.waitKey(1) == ord('q'):
                    break
        finally:
            camera.stop()
main()
