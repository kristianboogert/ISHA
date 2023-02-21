import mediapipe

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
