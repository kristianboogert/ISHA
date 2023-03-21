import pyrealsense2
import numpy as np

class NewDepthCamera():
    def __init__(self):
        self.pipeline = pyrealsense2.pipeline()
        self.config = pyrealsense2.config()
        self.config.enable_stream(pyrealsense2.stream.color, 640, 480, pyrealsense2.format.bgr8, 30)
        self.config.enable_stream(pyrealsense2.stream.depth)

    def process(self, rgbDFrame):
        colorFrame = np.asanyarray(rgbDFrame.get_color_frame().get_data())
        depthFrame = np.asanyarray(rgbDFrame.get_depth_frame().get_data())
        return colorFrame, depthFrame

    def getFrame(self):
        return self.process(self.pipeline.wait_for_frames())

    def run(self):
        self.pipeline.start(self.config)