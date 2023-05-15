import cv2
import threading
#import pyrealsense2 as realsense
import numpy as np

DEFAULT_CAMERA_RESOLUTION=(640,480)

class Camera:
    def __init__(self, cameraId=None, resolution=DEFAULT_CAMERA_RESOLUTION, use_realsense=False, realsense_framerate=30, realsense_frame_queue_size=5):
        self.resolution = resolution
        self.cameraId = cameraId
        self.videoCapture = None
        self.running = False
    # Start collecting frames
    def start(self):
        self.videoCapture = cv2.VideoCapture(self.cameraId)
    # Stop the collection of frames
    def stop(self):
        self.videoCapture = None
    def is_running(self):
        return self.videoCapture is None
    # Get current frame
    def getFrame(self):
        if self.videoCapture is not None:
            _, frame = self.videoCapture.read()
            if frame is not None:
                return self._resize(frame)
        return None
    # Resize a frame
    def _resize(self, frame):
        resized_frame = cv2.resize(frame, dsize=self.resolution)
        return resized_frame
