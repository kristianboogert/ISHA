import cv2
from handDetection import HandDetection
import time
# from test_pose import DEFAULT_CAMERA_RESOLUTION

class BuiltinCamera:
    def __init__(self, resolution=(640,480)):
        self.resolution = resolution
        self.capture = cv2.VideoCapture(0)
        self.hand_detection = HandDetection()
        cv2.namedWindow('Test', cv2.WINDOW_AUTOSIZE)
        time.sleep(10)

    def display_color_frame(self, color_frame):
        cv2.imshow('Test', color_frame)

    def process(self, color_frame):
        results, color_frame = self.hand_detection.process(color_frame)
        # color_frame = self.hand_detection.draw(color_frame, results)
        self.display_color_frame(color_frame)

    def getFrame(self):
            ret, color_frame = self.capture.read()
            # print(color_frame)
            return(color_frame)