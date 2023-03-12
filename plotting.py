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
            [
            poseData.pose_landmarks.landmark[11].x,
            poseData.pose_landmarks.landmark[12].x,
            poseData.pose_landmarks.landmark[13].x,
            poseData.pose_landmarks.landmark[14].x,
            poseData.pose_landmarks.landmark[15].x,
            poseData.pose_landmarks.landmark[16].x]
        )
        ypoints = np.array(
            [
            poseData.pose_landmarks.landmark[11].y,
            poseData.pose_landmarks.landmark[12].y,
            poseData.pose_landmarks.landmark[13].y,
            poseData.pose_landmarks.landmark[14].y,
            poseData.pose_landmarks.landmark[15].y,
            poseData.pose_landmarks.landmark[16].y]
        )
        zpoints = np.array(
            [
            poseData.pose_landmarks.landmark[11].z,
            poseData.pose_landmarks.landmark[12].z,
            poseData.pose_landmarks.landmark[13].z,
            poseData.pose_landmarks.landmark[14].z,
            poseData.pose_landmarks.landmark[15].z,
            poseData.pose_landmarks.landmark[16].z]
        )
        
        plt.axis([-1,1,-1,1])
        plt.ion()
 
        for phase in poseData(xpoints, ypoints, zpoints):
            plt.plot(xpoints[0], ypoints[0], zpoints[0])
            plt.pause(1)
    