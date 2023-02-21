from new__Camera import Camera
from new__CameraPreview import CameraPreview
from new__PoseDetection import PoseDetection

from mayavi import mlab

def main():
    camera = Camera()
    camera.start()
    poseDetection = PoseDetection()
    while True:
        frame = camera.getFrame()
        if frame is not None:
            poseData, _ = poseDetection.getPose(frame)
            nosepos = poseDetection.getPoseLandmark(poseData, 0)
            lshoulderpos = poseDetection.getPoseLandmark(poseData, 11)
            rshoulderpos = poseDetection.getPoseLandmark(poseData, 12)
            print(nosepos)
            print(lshoulderpos)
            print(rshoulderpos)
main()
