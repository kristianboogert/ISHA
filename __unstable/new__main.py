from new__Camera import Camera
from new__CameraPreview import CameraPreview
from new__PoseDetection import BodyPart, PoseDetection

import cv2

def main():
    # camera = Camera(cameraId=0)
    camera = Camera(use_realsense=True)
    camera.start()
    preview = CameraPreview()
    # preview.show(camera)
    poseDetection = PoseDetection(display_pose=True)
    while True:
        frame = camera.getFrame()
        print(frame)
        try:
            while True:
                color_frame, depth_frame = camera.getFrame()
                poseData, handData, frame = poseDetection.getPose(color_frame)
                # get torso angle
                lshoulderpos = poseDetection.getPoseLandmark(poseData, BodyPart.LEFT_SHOULDER)
                rshoulderpos = poseDetection.getPoseLandmark(poseData, BodyPart.RIGHT_SHOULDER)
                lelbowpos = poseDetection.getPoseLandmark(poseData, BodyPart.LEFT_ELBOW)
                relbowpos = poseDetection.getPoseLandmark(poseData, BodyPart.RIGHT_ELBOW)
                # print(poseDetection.getDirectionVectorForBodypart(BodyPart.LEFT_ELBOW, poseData))
                shoulders_direction_vector = poseDetection.getDirectionVectorForBodypart(BodyPart.LEFT_SHOULDER, poseData, originBodyPart=BodyPart.RIGHT_SHOULDER)
                print("SHOULDERS STRAIGHT:", poseDetection.isSittingUp(poseData))
                print("T-POSING:", poseDetection.isTPosing(poseData))
                # try:
                #     shoulder_angle = poseDetection.getShoulderAngle(lshoulderpos, rshoulderpos)
                #     depth_angle = poseDetection.getDepthAngle(lshoulderpos, lelbowpos)
                #     lshoulder_lelbow_angle = abs((180-shoulder_angle))-abs(poseDetection.getElbowShoulderAngle(lshoulderpos, lelbowpos))
                #     rshoulder_relbow_angle = abs((shoulder_angle))-abs(poseDetection.getElbowShoulderAngle(rshoulderpos, relbowpos))
                #     print(lshoulder_lelbow_angle)
                #     print(rshoulder_relbow_angle)
                #     print("VECTOR:", vector)
                #     print("sitting up:", poseDetection.isSittingUp(shoulder_angle))
                #     print("T-pose detected:", poseDetection.isTPosing(lshoulder_lelbow_angle, rshoulder_relbow_angle))
                #     print("depth:", depth_angle)
                # except:
                #     pass
                # print(lelbowpos, lshoulderpos)
                # relbowpos = poseDetection.getPoseLandmark(poseData, BodyPart.RIGHT_ELBOW)

                # print(poseDetection.getAngle(lshoulderpos, lelbowpos))
                cv2.imshow('frame', cv2.flip(frame, 1))
                if cv2.waitKey(1) == ord('q'):
                    break
        finally:
            camera.stop()
main()
