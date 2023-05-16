from poseDetection import PoseDetection
from newDepthCamera import NewDepthCamera
<<<<<<< HEAD:plotting.py
from buildinCamera import BuiltinCamera
import numpy as np
import matplotlib.pyplot as plt
from enum import IntEnum
import mediapipe as mp
from mpl_toolkits import mplot3d

# plt.interactive(True)

fig = plt.figure()

# class BodyPart(IntEnum):
#     NOSE = 0,
#     LEFT_EYE_INNER = 1,
#     LEFT_EYE = 2,
#     LEFT_EYE_OUTER = 3,
#     RIGHT_EYE_INNER = 4,
#     RIGHT_EYE = 5,
#     RIGHT_EYE_OUTER = 6,
#     LEFT_EAR = 7,
#     RIGHT_EAR = 8,
#     MOUTH_LEFT = 9,
#     MOUTH_RIGHT = 10,
#     LEFT_SHOULDER = 11,
#     RIGHT_SHOULDER = 12,
#     LEFT_ELBOW = 13,
#     RIGHT_ELBOW = 14,
#     LEFT_WRIST = 15,
#     RIGHT_WRIST = 16,
#     LEFT_PINKY = 17,
#     RIGHT_PINKY = 18,
#     LEFT_INDEX = 19,
#     RIGHT_INDEX = 20,
#     LEFT_THUMB = 21,
#     RIGHT_THUMB = 22,
#     LEFT_HIP = 23,
#     RIGHT_HIP = 24,
#     LEFT_KNEE = 25,
#     RIGHT_KNEE = 26,
#     LEFT_ANKLE = 27,
#     RIGHT_ANKLE = 28,
#     LEFT_HEEL = 29,
#     RIGHT_HEEL = 30,
#     LEFT_FOOT_INDEX = 31,
#     RIGHT_FOOT_INDEX = 32

# ax = plt.figure().add_subplot(projection='3d')

ax = plt.axes(projection='3d')

# class Plot3D:
#     def __init__(self):
#         self.depth_cam = BuiltinCamera()

#         while True:
#             frame = self.depth_cam.getFrame()
#             self.poseDetection = PoseDetection()
#             results, _ = self.poseDetection.process(frame)
#             self.plot(results)
            
#     def plot(self, poseData):
#         xpoints = np.array(
#             [
#             poseData.pose_landmarks.landmark[11].x,
#             poseData.pose_landmarks.landmark[12].x,
#             poseData.pose_landmarks.landmark[13].x,
#             poseData.pose_landmarks.landmark[14].x,
#             poseData.pose_landmarks.landmark[15].x,
#             poseData.pose_landmarks.landmark[16].x]
#         )
#         ypoints = np.array(
#             [
#             poseData.pose_landmarks.landmark[11].y,
#             poseData.pose_landmarks.landmark[12].y,
#             poseData.pose_landmarks.landmark[13].y,
#             poseData.pose_landmarks.landmark[14].y,
#             poseData.pose_landmarks.landmark[15].y,
#             poseData.pose_landmarks.landmark[16].y]
#         )
#         zpoints = np.array(
#             [
#             poseData.pose_landmarks.landmark[11].z,
#             poseData.pose_landmarks.landmark[12].z,
#             poseData.pose_landmarks.landmark[13].z,
#             poseData.pose_landmarks.landmark[14].z,
#             poseData.pose_landmarks.landmark[15].z,
#             poseData.pose_landmarks.landmark[16].z]
#         )
        
#         plt.axis([-1,1,-1,1])
#         plt.ion()
 
   
#         plt()
#         plt.pause(0.01)

# Data for a three-dimensional line
zline = np.linspace(0, 15, 1000)
xline = np.sin(zline)
yline = np.cos(zline)
ax.plot3D(xline, yline, zline, 'gray')

# Data for three-dimensional scattered points
zdata = 15 * np.random.random(100)
xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')
=======
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
    
>>>>>>> b65200c1d19b6f7570d00dca913eb88bdc44ac64:__legacy/2/plotting.py
