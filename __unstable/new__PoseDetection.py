import mediapipe
import math
from enum import IntEnum
import cv2

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
    def __init__(self, display_frames=False):
        self.display_frames = display_frames
        # Define pose detection model
        self.mpPose = mediapipe.solutions.pose
        self.pose = self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        # Define hand detection model
        self.mpHands = mediapipe.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
        # Define mediapipe drawing util
        self.draw = mediapipe.solutions.drawing_utils
        # Keep track of pose data
        self.poseData = None
        self.handData = None
    def getPose(self, cameraFrame):
        # if self.display_frames:
        #     # cv2.imshow('orig', cameraFrame)
        # Get the pose data from mediapipe
        cameraFrame = cv2.cvtColor(cameraFrame, cv2.COLOR_BGR2RGB)
        cameraFrame.flags.writeable = False
        self.poseData = self.pose.process(cameraFrame)
        self.handData = self.hands.process(cameraFrame)
        cameraFrame.flags.writeable = True
        cameraFrame = cv2.cvtColor(cameraFrame, cv2.COLOR_RGB2BGR)
        # If required, display the data
        if self.display_frames:
            self.draw.draw_landmarks(cameraFrame, self.poseData.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
            if self.handData.multi_hand_landmarks:
                for hand, hand_landmarks in enumerate(self.handData.multi_hand_landmarks):
                    self.draw.draw_landmarks(image=cameraFrame, landmark_list=hand_landmarks, connections=self.mpHands.HAND_CONNECTIONS)
        return (self.poseData, self.handData, cameraFrame)
    def getPoseLandmark(self, poseData, limb):
        try:
            return poseData.pose_landmarks.landmark[limb]
        except:
            None
    def getShoulderAngle(self, left_shoulder, right_shoulder):
        if (left_shoulder is None or right_shoulder is None) or (left_shoulder.visibility < 0.9 or right_shoulder.visibility < 0.9):
            return None
        angle = math.degrees(math.atan2(right_shoulder.y - left_shoulder.y, right_shoulder.x - left_shoulder.x))
        return angle

    # TODO: also see if the user is not laying down
    def isSittingUp(self, shoulder_angle, correct_angle=180, tolerance=10):
        if shoulder_angle is None:
            return False
        if shoulder_angle < -correct_angle+tolerance or shoulder_angle > correct_angle-tolerance:
            return True
        else:
            return False
    def getElbowShoulderAngle(self, shoulder, elbow):
        if shoulder is None or elbow is None:
            return None
        shoulder_x, shoulder_y = shoulder.x, shoulder.y
        elbow_x, elbow_y = elbow.x, elbow.y
        dx = elbow_x - shoulder_x
        dy = elbow_y - shoulder_y
        angle = math.degrees(math.atan2(dy, dx))
        return angle
    def getDepthAngle(self, left_shoulder, left_elbow):
        if (left_shoulder is None or left_elbow is None) or (left_shoulder.visibility < 0.9 or left_elbow.visibility < 0.9):
            return None
        depth_angle = math.degrees(math.atan2(left_elbow.y - left_shoulder.y, left_elbow.z - left_shoulder.z))
        return depth_angle

    def isTPosing(self, left_elbow_angle, right_elbow_angle):
        if (abs(left_elbow_angle) < 15 or 365-abs(left_elbow_angle < 15)) and (abs(right_elbow_angle) < 15 or 365-abs(right_elbow_angle) < 15):
            return True
        return False




    # def getAngle(self, point_1, point_2):
    #     if (point_1 is None or point_2 is None) or (point_1.visibility < 0.9 or point_2.visibility < 0.9):
    #         return None
    #     # Check the order of the points and calculate the direction vector
    #     direction_vector = [point_2.x - point_1.x, point_2.y - point_1.y, point_2.z - point_1.z]
    #     # Normalize the direction vector
    #     length = math.sqrt(direction_vector[0]**2 + direction_vector[1]**2 + direction_vector[2]**2)
    #     direction_vector = [direction_vector[0]/length, direction_vector[1]/length, direction_vector[2]/length]
    #     # Calculate the heading angle
    #     heading = math.degrees(math.atan2(direction_vector[1], direction_vector[0]))
    #     # Calculate the pitch angle
    #     pitch = math.degrees(math.atan2(-direction_vector[2], math.sqrt(direction_vector[0]**2 + direction_vector[1]**2)))
    #     # Calculate the bank angle
    #     bank = math.degrees(math.atan2(direction_vector[0], direction_vector[2]))
    #     return (heading, pitch, bank)

    # def getAngle(self, point_1, point_2):
    #     if (point_1 is None or point_2 is None) or (point_1.visibility < 0.9 or point_2.visibility < 0.9):
    #         return None
    #     # Calculate the direction vector from point 1 to point 2
    #     direction_vector = [point_2.x - point_1.x, point_2.y - point_1.y, point_2.z - point_1.z]
    #     # Calculate the heading angle
    #     heading = math.degrees(math.atan2(direction_vector[1], direction_vector[0]))
    #     # Calculate the pitch angle
    #     pitch = math.degrees(math.atan2(-direction_vector[2], math.sqrt(direction_vector[0]**2 + direction_vector[1]**2)))
    #     # Calculate the bank angle
    #     bank = math.degrees(math.atan2(direction_vector[0], direction_vector[2]))
    #     return (heading, pitch, bank)