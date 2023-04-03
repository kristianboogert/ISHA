# from ..poseDetection.HandPoseDetection import HandPoseDetection
# from ..poseDetection.Camera import Camera

import sys
sys.path.append("..")
from poseDetection.HandPoseDetection import *
from poseDetection.HandPart import *
from poseDetection.BodyPart import *

### niet-fugl-meyer oefeningen:
#schuiven arm over tafel  (oefening 22)
#hand omdraaien           (oefening 10: alleen de eerste 3)
#spreiden sluiten vingers (oefening 9: alleen de eerste, voor de leuk ook de tweede)
###

class FuglMeyer:
    def __init__(self):
        self.none = None
    def landmarksAreVisible(self, landmarks, visibilityThreshold=0.85):
        for landmark in landmarks:
            if landmark is None or landmark.visibility < visibilityThreshold:
                return False
        return True
    def exerciseRaiseArmToSide(self, camera, bodyPoseDetection, nonImpairedElbowBodyPart, visibilityThreshold=0.85):
        if not camera.is_running():
            camera.start()
        nonImpairedAngleMin = None
        nonImpairedAngleMax = None
        impairedAngleMin = None
        impairedAngleMax = None
        # Handle exercise
        while True:
            frame = camera.getFrame()
            poseData = bodyPoseDetection.getPose(frame)
            cv2.imshow('body frame', cv2.flip(frame, 1))
            if cv2.waitKey(1) == ord('q'):
                break
            leftShoulderLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.LEFT_SHOULDER, poseData)
            rightShoulderLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.RIGHT_SHOULDER, poseData)
            leftElbowLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.LEFT_ELBOW, poseData)
            rightElbowLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.RIGHT_ELBOW, poseData)
            # See if the user is in frame by checking the visibility of key landmarks
            if self.landmarksAreVisible([leftShoulderLandmark, rightShoulderLandmark, leftElbowLandmark, rightElbowLandmark]):
                print("user is in frame")
                # TODO: handle exercise activities
            else:
                print("user is not in frame")
                # TODO: give suggestions of how to put the user in frame

# TODO: See if user is completely in frame
# TODO: See if user is raising their arm
# TODO: See if user has rotated the left hand 180-ish degrees
# TODO: See if user has rotated the left hand back to 0-ish degrees
# TODO: Maybe not the full 180-ish degrees