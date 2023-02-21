# from imports import *

from poseDetection import PoseDetection
from newDepthCamera import NewDepthCamera
import numpy as np
import matplotlib.pyplot as plt

plt.interactive(True)

ax = plt.figure().add_subplot(projection='3d')

class Plot3D:
    def __init__(self):
        self.depth_cam = NewDepthCamera()
        self.depth_cam.run()

        while True:
            frame, _ = self.depth_cam.getFrame()

            self.poseDetection = PoseDetection()
            results, _ = self.poseDetection.process(frame)
            self.plot(results)


            
    def plot(self, poseData):
        xpoints = np.array(
            [poseData.pose_landmarks.landmark[0].x,
            poseData.pose_landmarks.landmark[11].x,
            poseData.pose_landmarks.landmark[12].x]
        )
        ypoints = np.array(
            [poseData.pose_landmarks.landmark[0].y,
            poseData.pose_landmarks.landmark[11].y,
            poseData.pose_landmarks.landmark[12].y]
        )
        zpoints = np.array(
            [poseData.pose_landmarks.landmark[0].z,
            poseData.pose_landmarks.landmark[11].z,
            poseData.pose_landmarks.landmark[12].z]
        )
        
        plt.axis([-1,1,-1,1])
        plt.ion()
 
        for phase in poseData(xpoints, ypoints, zpoints):     
            plt.plot(xpoints, ypoints, zpoints)
            plt.pause(0.001)
            