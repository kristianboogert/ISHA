#!/usr/bin/env python3

<<<<<<< HEAD:test_pose.py
# from newDepthCamera import NewDepthCamera
# from plotting import Plot3D
from buildinCamera import BuiltinCamera
from poseDetection import PoseDetection
=======
from newDepthCamera import NewDepthCamera
from plotting import Plot3D
>>>>>>> b65200c1d19b6f7570d00dca913eb88bdc44ac64:__legacy/2/test_pose.py

previousTime = 0
currentTime = 0

<<<<<<< HEAD:test_pose.py
# camera = NewDeptCamera()
camera = BuiltinCamera()
poseDetection = PoseDetection()
color_frame = camera.getFrame()
results, _ = poseDetection.process(color_frame)
# plot3d = Plot3D()
=======
camera = NewDepthCamera()
camera.run()
plot3d = Plot3D()

# while True:
#     color, depth = camera.getFrame()
>>>>>>> b65200c1d19b6f7570d00dca913eb88bdc44ac64:__legacy/2/test_pose.py
