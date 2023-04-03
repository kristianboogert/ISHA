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
        exerciseStarted = False
        # Handle exercise
        while True:
            ###
            # Get camera frame
            ###
            frame = camera.getFrame()
            ###
            # Detect body pose (mediapipe)
            ###
            poseData = bodyPoseDetection.getPose(frame)
            frame = bodyPoseDetection.drawPose(frame, poseData)
            cv2.imshow('body frame', cv2.flip(frame, 1))
            if cv2.waitKey(1) == ord('q'):
                break
            ###
            # Are all relevant joints in frame?
            ###
            leftShoulderLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.LEFT_SHOULDER, poseData)
            rightShoulderLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.RIGHT_SHOULDER, poseData)
            leftElbowLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.LEFT_ELBOW, poseData)
            rightElbowLandmark = bodyPoseDetection.getPoseLandmark(BodyPart.RIGHT_ELBOW, poseData)
            if not self.landmarksAreVisible([leftShoulderLandmark, rightShoulderLandmark, leftElbowLandmark, rightElbowLandmark]):
                print("user is not fully in frame for this exercise")
                continue
            ###
            # Has exercise been started?
            ###
            if not exerciseStarted:
                exerciseStarted = True
                continue
            ###
            # Has user pressed "quit"?
            ###
            # TODO: FIND OUT HOW TO DO THIS! MAYBE SOME DBUS MAGIC SO OTHER PROCESSES CAN TALK TO US?

            ###
            # Calculate relevant joint angles
            ###
            leftUpperArmAngle = bodyPoseDetection.getAnglesForBodyPart(BodyPart.LEFT_ELBOW, poseData)
            rightUpperArmAngle = bodyPoseDetection.getAnglesForBodyPart(BodyPart.RIGHT_ELBOW, poseData)
            leftLowerArmAngle = bodyPoseDetection.getAnglesForBodyPart(BodyPart.LEFT_WRIST, poseData)
            rightLowerArmAngle = bodyPoseDetection.getAnglesForBodyPart(BodyPart.RIGHT_WRIST, poseData)
            print("ARM ANGLES:\nLeft: ", leftUpperArmAngle["xy"],
                  "\nRight:", rightUpperArmAngle["xy"], "\n",
                  "WRIST ANGLES:\nLeft: ", leftLowerArmAngle["xy"],
                  "\nRight:", rightLowerArmAngle["xy"], "\n",
                 )
