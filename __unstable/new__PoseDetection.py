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
    def __init__(self, display_pose=False, visibility_threshold=0.9):
        self.display_pose = display_pose
        self.visibility_threshold = visibility_threshold
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
        # Get the pose data from mediapipe
        cameraFrame = cv2.cvtColor(cameraFrame, cv2.COLOR_BGR2RGB)
        cameraFrame.flags.writeable = False
        self.poseData = self.pose.process(cameraFrame)
        self.handData = self.hands.process(cameraFrame)
        cameraFrame.flags.writeable = True
        cameraFrame = cv2.cvtColor(cameraFrame, cv2.COLOR_RGB2BGR)
        # If required, display the data
        if self.display_pose:
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
    # TODO: also see if the user is not laying down
    def isSittingUp(self, shoulders_direction_vector, penalty_threshold=0.05, tolerance=0.02):
        try:
            return (abs(shoulders_direction_vector["y"])-tolerance) < penalty_threshold
        except:
            return None
    def getDirectionVectorForBodypart(self, bodyPart, poseData, originBodyPart=None):
        if poseData.pose_landmarks is None:
            return None
        landmarks = poseData.pose_landmarks.landmark
        if bodyPart == BodyPart.LEFT_ELBOW:
            return self._getDirectionVector(landmarks[BodyPart.LEFT_ELBOW], landmarks[BodyPart.LEFT_SHOULDER])
        elif bodyPart == BodyPart.LEFT_WRIST:
            return self._getDirectionVector(landmarks[BodyPart.LEFT_WRIST], landmarks[BodyPart.LEFT_ELBOW])
        elif bodyPart == BodyPart.LEFT_INDEX:
            return self._getDirectionVector(landmarks[BodyPart.LEFT_INDEX], landmarks[BodyPart.LEFT_WRIST])
        elif bodyPart == BodyPart.RIGHT_ELBOW:
            return self._getDirectionVector(landmarks[BodyPart.RIGHT_ELBOW], landmarks[BodyPart.RIGHT_SHOULDER])
        elif bodyPart == BodyPart.RIGHT_WRIST:
            return self._getDirectionVector(landmarks[BodyPart.RIGHT_WRIST], landmarks[BodyPart.RIGHT_ELBOW])
        elif bodyPart == BodyPart.RIGHT_INDEX:
            return self._getDirectionVector(landmarks[BodyPart.RIGHT_INDEX], landmarks[BodyPart.RIGHT_WRIST])
        elif originBodyPart is not None:
            return self._getDirectionVector(landmarks[bodyPart], landmarks[originBodyPart])
    def _getDirectionVector(self, landmark_1, landmark_2, visibility_threshold=0.75):
        print(landmark_1, landmark_2)
        if landmark_1.visibility > visibility_threshold and landmark_2.visibility > visibility_threshold:
            return {
                "x": landmark_1.x - landmark_2.x,
                "y": landmark_1.y - landmark_2.y,
                "z": landmark_1.z - landmark_2.z
            }
        return None
    # TODO: GET DATA FROM DEPTH CAMERA AND SCALE THE X THRESHOLD!
    # TODO: WE DOEN DAT ZEKER WEL OP BASIS VAN EMPIRISCH NATTEVINGERWERK!
    def isTPosing(self, poseData, x_threshold=0.13, x_threshold_depth_scale=1.0):
        if poseData.pose_landmarks is None:
            return None
        landmarks = poseData.pose_landmarks.landmark
        # see if the left upper arm is pointing to the left
        left_upper_arm_direction = self.getDirectionVectorForBodypart(BodyPart.LEFT_ELBOW, poseData)
        left_lower_arm_direction = self.getDirectionVectorForBodypart(BodyPart.LEFT_WRIST, poseData)
        left_index_finger_direction = self.getDirectionVectorForBodypart(BodyPart.LEFT_INDEX, poseData)
        right_upper_arm_direction = self.getDirectionVectorForBodypart(BodyPart.RIGHT_ELBOW, poseData)
        right_lower_arm_direction = self.getDirectionVectorForBodypart(BodyPart.RIGHT_WRIST, poseData)
        right_index_finger_direction = self.getDirectionVectorForBodypart(BodyPart.RIGHT_INDEX, poseData)
        print("left upper arm", left_upper_arm_direction)
        print("left lower arm", left_lower_arm_direction)
        print("left finger", left_index_finger_direction)
        print("right upper arm", right_upper_arm_direction)
        print("right lower arm", right_lower_arm_direction)
        print("right finger", right_index_finger_direction)
        try:
            if left_upper_arm_direction["x"] >= x_threshold and \
               left_lower_arm_direction["x"] >= x_threshold and \
               abs(left_index_finger_direction["y"]) <= x_threshold/2 and \
               right_upper_arm_direction["x"] <= -x_threshold and \
               right_lower_arm_direction["x"] <= -x_threshold and \
               abs(right_index_finger_direction["y"]) <= x_threshold/2:
                return True
        except:
            pass

        return False

















    # # om te testen
    # def correct_z_using_realsense(body_position, depth_image):
    #     landmarks = np.array([[lmk.x, lmk.y, lmk.z] for lmk in body_position.landmark])
    #     xs = (landmarks[:,0] * int(depth_image.shape[1]))
    #     ys = (landmarks[:,1] * int(depth_image.shape[0]))
    #     depths = depth_image[ys, xs]
    #     z_scale_factor = np.median(depths) / np.median(landmarks[:,2])
    #     corrected_landmarks = landmarks.copy()
    #     corrected_landmarks[:,2] *= z_scale_factor
    #     corrected_body_position = mp.solutions.pose.PoseLandmarkList()
    #     for i in range(len(body_position.landmark)):
    #         corrected_lmk = mp.solutions.pose.PoseLandmark()
    #         corrected_lmk.x, corrected_lmk.y, corrected_lmk.z = corrected_landmarks[i]
    #         corrected_lmk.visibility = body_position.landmark[i].visibility
    #         corrected_lmk.presence = body_position.landmark[i].presence
    #         corrected_body_position.landmark.append(corrected_lmk)
    #     return corrected_body_position





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