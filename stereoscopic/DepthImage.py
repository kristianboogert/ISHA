import numpy as np
import cv2

class DepthImage:
    def __init__(self, resolution=(640,480)):
        self.resolution = resolution
        block_size = 5
        min_disp = -128
        max_disp = 128
        num_disp = max_disp - min_disp
        uniqueness_ratio = 5
        speckle_window_size = 200
        speckle_range = 2
        self.stereo = cv2.StereoSGBM_create(
            minDisparity=min_disp,
            numDisparities=num_disp,
            blockSize=block_size,
            uniquenessRatio=uniqueness_ratio,
            speckleWindowSize=speckle_window_size,
            speckleRange=speckle_range,
            # disp12MaxDiff=disp12MaxDiff,
            P1=8 * 1 * block_size * block_size,
            P2=32 * 1 * block_size * block_size,
        )
    def create(self, frame1, frame2):
        depth_image = self.stereo.compute(frame1, frame2)
        depth_image = cv2.normalize(depth_image, depth_image, alpha=255,
                        beta=0, norm_type=cv2.NORM_MINMAX)
        depth_image = np.uint8(depth_image)
        return self._resize(depth_image)
    def _resize(self, frame):
        resized_frame = cv2.resize(frame, dsize=self.resolution)
        return resized_frame