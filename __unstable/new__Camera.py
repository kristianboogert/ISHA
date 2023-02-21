import cv2
import threading

DEFAULT_CAMERA_RESOLUTION=(640,480)

class Camera:
    ###
    # Public
    ###

    def __init__(self, resolution=DEFAULT_CAMERA_RESOLUTION):
        self.resolution = resolution
        self.videoCapture = None
        self.running = False

    # Start collecting frames
    def start(self, cameraId=0):
        self.videoCapture = cv2.VideoCapture(cameraId)

    # Stop the collection of frames
    def stop(self):
        self.videoCapture = None

    # Get current frame
    def getFrame(self):
        if self.videoCapture is not None:
            _, frame = self.videoCapture.read()
            return self._resize(frame)
        return None

    ###
    # Private
    ###

    # Resize a frame
    def _resize(self, frame):
        return cv2.resize(frame, dsize=self.resolution)
