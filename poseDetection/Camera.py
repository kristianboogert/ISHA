import cv2
import threading
#import pyrealsense2 as realsense
import numpy as np

DEFAULT_CAMERA_RESOLUTION=(640,480)

class Camera:
    ###
    # Public
    ###

    def __init__(self, cameraId=None, resolution=DEFAULT_CAMERA_RESOLUTION, use_realsense=False, realsense_framerate=30, realsense_frame_queue_size=5):
        self.resolution = resolution
        self.cameraId = cameraId
#        self.use_realsense = use_realsense
#        self.realsense_framerate = realsense_framerate
        self.videoCapture = None
        self.running = False
#        self.realsense_pipeline = realsense.pipeline()
#        self.realsense_config = realsense.config()
#        self.realsense_frame_queue = realsense.frame_queue(realsense_frame_queue_size)

    # Start collecting frames
    def start(self):
 #       if self.use_realsense:
 #           self.realsense_config.enable_stream(realsense.stream.color, self.resolution[0], self.resolution[1], realsense.format.bgr8, self.realsense_framerate)
 #           self.realsense_config.enable_stream(realsense.stream.depth)
 #           self.realsense_pipeline.start(self.realsense_config)
 #       else:
        self.videoCapture = cv2.VideoCapture(self.cameraId)

    # Stop the collection of frames
    def stop(self):
        #if self.use_realsense:
        #    self.realsense_pipeline.stop()
        #else:
        self.videoCapture = None
        
    def is_running(self):
        return (self.videoCapture is None) # and self.realsense_pipeline is None)

    # Get current frame
    def getFrame(self):
#        if self.use_realsense:
#            rgbDFrame = self.realsense_pipeline.wait_for_frames()
#            colorFrame = self._resize(np.asanyarray(rgbDFrame.get_color_frame().get_data()))
#            depthFrame = self._resize(np.asanyarray(rgbDFrame.get_depth_frame().get_data()))
#            return colorFrame, depthFrame
#            # return (self._resize(rgb_d_frame.get_color_frame()), self._resize(rgb_d_frame.get_depth_frame()))
#        else:
        if self.videoCapture is not None:
            _, frame = self.videoCapture.read()
            if frame is not None:
                return self._resize(frame)
        return None

    ###
    # Private
    ###

    # Resize a frame
    def _resize(self, frame):
        resized_frame = cv2.resize(frame, dsize=self.resolution)
        return resized_frame
