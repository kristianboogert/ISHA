from imports import *

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
        try:
            current_nose_val = ((100-(results.pose_landmarks.landmark[0].z*-100))*2.54)-1.06299213
            current_shoulder_val = ((100-(results.pose_landmarks.landmark[11].z*-100))*2.54)-1.06299213
            print("SOFTWARE NOSE Z: {}".format(current_nose_val))
            print("SOFT SCHOUDER Z: {}".format(current_shoulder_val))
        except:
            pass
        self.draw.draw_landmarks(color_frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return results, color_frame