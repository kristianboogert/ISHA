import mediapipe as mp
import cv2

class PoseDetection:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
        	min_detection_confidence=0.5,
	        min_tracking_confidence=0.5,
	        enable_segmentation=True,
            smooth_segmentation=True
        )
        self.draw = mp.solutions.drawing_utils

    def process(self, color_frame):
        results = self.pose.process(cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB))
        self.draw.draw_landmarks(color_frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        
<<<<<<< HEAD:poseDetection.py
        return results, color_frame
=======
        return results, color_frame
    
>>>>>>> b65200c1d19b6f7570d00dca913eb88bdc44ac64:__legacy/2/poseDetection.py
