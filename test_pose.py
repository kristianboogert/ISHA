#!/usr/bin/env python3

from newDepthCamera import NewDepthCamera
from plotting import Plot3D

previousTime = 0
currentTime = 0

camera = NewDepthCamera()
camera.run()
plot3d = Plot3D()

# while True:
#     color, depth = camera.getFrame()
