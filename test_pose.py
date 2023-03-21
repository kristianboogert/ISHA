#!/usr/bin/env python3

# from newDepthCamera import NewDepthCamera
# from plotting import Plot3D
from buildinCamera import BuiltinCamera
from poseDetection import PoseDetection

previousTime = 0
currentTime = 0

# camera = NewDeptCamera()
camera = BuiltinCamera()
poseDetection = PoseDetection()
color_frame = camera.getFrame()
results, _ = poseDetection.process(color_frame)
# plot3d = Plot3D()