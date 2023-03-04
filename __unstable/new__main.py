from new__Camera import Camera
from new__CameraPreview import CameraPreview
from new__PoseDetection import BodyPart, PoseDetection

def main():
    camera = Camera()
    camera.start()
    poseDetection = PoseDetection()
    while True:
        frame = camera.getFrame()
        if frame is not None:
            poseData, _ = poseDetection.getPose(frame)
            nosepos = poseDetection.getPoseLandmark(poseData, BodyPart.NOSE)
            lshoulderpos = poseDetection.getPoseLandmark(poseData, BodyPart.LEFT_SHOULDER)
            rshoulderpos = poseDetection.getPoseLandmark(poseData, BodyPart.RIGHT_SHOULDER)
            print("NOSE:          ", nosepos)
            print("LEFT SHOULDER: ", lshoulderpos)
            print("RIGHT SHOULDER:", rshoulderpos)
            print("NOSE_ANGLE:    ", poseDetection.getAngles(nosepos, lshoulderpos))
main()
