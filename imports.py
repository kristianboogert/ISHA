import pyrealsense2 as realsense
import cv2
import mediapipe as mp
import numpy as np
from handDetection import HandDetection
from poseDetection import PoseDetection
from depthCamera import DepthCamera
from depthCamera import TEST_POSITION
from test_pose import DEFAULT_CAMERA_RESOLUTION
from buildinCamera import BuiltinCamera