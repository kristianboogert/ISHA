from imports import *

DEFAULT_CAMERA_RESOLUTION = (640,480) # Use the holy resolution of 640x480
DEFAULT_CAMERA_FRAMERATE = 30

TEST_POSITION = tuple(value//2 for value in DEFAULT_CAMERA_RESOLUTION)

class DepthCamera:
    def __init__(self, resolution=DEFAULT_CAMERA_RESOLUTION, framerate=DEFAULT_CAMERA_FRAMERATE):
        self.resolution = resolution
        self.framerate = framerate
        self.pipeline = realsense.pipeline()
        self.config = realsense.config()
        self.config.enable_stream(realsense.stream.color, self.resolution[0], self.resolution[1], realsense.format.bgr8, self.framerate)
        self.config.enable_stream(realsense.stream.depth)
        cv2.namedWindow('RealSense color', cv2.WINDOW_AUTOSIZE)
        # cv2.namedWindow('RealSense depth', cv2.WINDOW_AUTOSIZE)
        self.hand_detection = HandDetection()
        self.pose_detection = PoseDetection()

    def display_color_frame(self, color_frame):
        color_image = np.asanyarray(color_frame.get_data())
        resized_color_image = cv2.resize(color_image, dsize=self.resolution)  #, interpolation=cv2.INTER_AREA)
        _, resized_color_image = self.hand_detection.process(resized_color_image)
        results, resized_color_image = self.pose_detection.process(resized_color_image)
        # try:
        #     condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        #     bg_image = np.zeros(resized_color_image.shape, dtype=np.uint8)
        #     BG_COLOR = (192, 192, 192)
        #     bg_image[:] = BG_COLOR
        #     resized_color_image = np.where(condition, resized_color_image, bg_image)
        # except:
        #     pass
        cv2.putText(resized_color_image, "+", TEST_POSITION, cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
        cv2.imshow('RealSense color', resized_color_image)