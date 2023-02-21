#!/usr/bin/env python3

from imports import *

previousTime = 0
currentTime = 0

DEFAULT_CAMERA_RESOLUTION = (640,480) # Use the holy resolution of 640x480
DEFAULT_CAMERA_FRAMERATE = 30

TEST_POSITION = tuple(value//2 for value in DEFAULT_CAMERA_RESOLUTION)


class BuiltinCamera:
    def __init__(self, resolution=DEFAULT_CAMERA_RESOLUTION):
        self.resolution = resolution
        self.hand_detection = HandDetection()
        cv2.namedWindow('Test', cv2.WINDOW_AUTOSIZE)
        time.sleep(10)

    def display_color_frame(self, color_frame):
        cv2.imshow('Test', color_frame)

    def process(self, color_frame):
        results, color_frame = self.hand_detection.process(color_frame)
        # color_frame = self.hand_detection.draw(color_frame, results)
        self.display_color_frame(color_frame)

    def run(self):
        capture = cv2.VideoCapture(-1)
        while True:
            ret, color_frame = capture.read()
            print(color_frame)
            self.process(color_frame)



    def display_distance_frame(self, depth_frame, position):
        x, y = position
        depth_image = np.asanyarray(depth_frame.get_data())

        resized_depth_image = cv2.resize(depth_image, dsize=self.resolution)  #, interpolation=cv2.INTER_AREA)
        dist = (resized_depth_image[y][x]/100)-1.06299213
        print("HARDWARE Z: {} cm".format(dist*2.54))
        # cv2.imshow('RealSense depth', resized_depth_image)

    # Callback function to process a frame
    def process(self, rgb_d_frame):
        # Extract color frame and depth frame from frame
        color_frame = rgb_d_frame.get_color_frame()
        depth_frame = rgb_d_frame.get_depth_frame()
        if not depth_frame or not color_frame:
            # print("Skipping frame due to missing data")
            return

        self.display_color_frame(color_frame)
        self.display_distance_frame(depth_frame, TEST_POSITION)

    def run(self):
        self.pipeline.start(self.config)
        try:
            while True:
                rgb_d_frame = self.pipeline.wait_for_frames()
                self.process(rgb_d_frame)
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    self.exit()
        finally:
            self.exit()

    def exit(self):
        self.pipeline.stop()
        cv2.destroyAllWindows()

camera = DepthCamera()
camera.run()
