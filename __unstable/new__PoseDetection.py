import mediapipe
import math
from enum import IntEnum

class BodyPart(IntEnum):
    NOSE = 0,
    LEFT_EYE_INNER = 1,
    LEFT_EYE = 2,
    LEFT_EYE_OUTER = 3,
    RIGHT_EYE_INNER = 4,
    RIGHT_EYE = 5,
    RIGHT_EYE_OUTER = 6,
    LEFT_EAR = 7,
    RIGHT_EAR = 8,
    MOUTH_LEFT = 9,
    MOUTH_RIGHT = 10,
    LEFT_SHOULDER = 11,
    RIGHT_SHOULDER = 12,
    LEFT_ELBOW = 13,
    RIGHT_ELBOW = 14,
    LEFT_WRIST = 15,
    RIGHT_WRIST = 16,
    LEFT_PINKY = 17,
    RIGHT_PINKY = 18,
    LEFT_INDEX = 19,
    RIGHT_INDEX = 20,
    LEFT_THUMB = 21,
    RIGHT_THUMB = 22,
    LEFT_HIP = 23,
    RIGHT_HIP = 24,
    LEFT_KNEE = 25,
    RIGHT_KNEE = 26,
    LEFT_ANKLE = 27,
    RIGHT_ANKLE = 28,
    LEFT_HEEL = 29,
    RIGHT_HEEL = 30,
    LEFT_FOOT_INDEX = 31,
    RIGHT_FOOT_INDEX = 32

class PoseDetection:
    ###
    # Public
    ###
    def __init__(self):
        # Define pose detection model
        self.mpPose = mediapipe.solutions.pose
        self.pose = self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        # Define hand detection model
        self.mpHands = mediapipe.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
        # Define mediapipe drawing util
        self.draw = mediapipe.solutions.drawing_utils
    def getPose(self, cameraFrame):
        # Get the pose data from mediapipe
        poseData = self.pose.process(cameraFrame)
        handData = self.hands.process(cameraFrame)
        return (poseData, handData)
    def getPoseLandmark(self, poseData, limb):
        try:
            return poseData.pose_landmarks.landmark[limb]
        except:
            None
    def getAngles(self, point_1, point_2):
        if point_1 is None or point_2 is None:
            return None
        # Calculate the direction vector from point 1 to point 2
        direction_vector = [point_2.x - point_1.x, point_2.y - point_1.y, point_2.z - point_1.z]
        # Calculate the heading angle
        heading = math.degrees(math.atan2(direction_vector[1], direction_vector[0]))
        # Calculate the pitch angle
        pitch = math.degrees(math.atan2(-direction_vector[2], math.sqrt(direction_vector[0]**2 + direction_vector[1]**2)))
        # Calculate the bank angle
        bank = math.degrees(math.atan2(direction_vector[0], direction_vector[2]))
        return (heading, pitch, bank)