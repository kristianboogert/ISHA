# from ..poseDetection.HandPoseDetection import HandPoseDetection
# from ..poseDetection.Camera import Camera

import sys
sys.path.append("..")
from poseDetection.HandPoseDetection import *
from poseDetection.HandPart import *

# class FuglMeyer:
#     def __init__(self):
#         self.active_test = None
    
#     def test_hand_rotation(self, poseData, handPoseDetection, current_testphase):
#         testphases = ["image_capture", "neutral_position", "hand_rotation", "end"]
#         if testphases[current_testphase] == "image_capture":
#             print("Put hand in front of screen")
#             while True:
#                 landmark = handPoseDetection.getHandLandmark(poseData, Hand.LEFT_HAND, HandPart.WRIST)
#                 print(landmark)
#                 if landmark is not None:
#                     return current_testphase+1
        # neutral_angle_min = -10
        # neutral_angle_max = 10
        # full_rotation_angle_min = 150
        # full_rotation_angle_max = 180
        # # Start camera if needed
        # if not camera.is_running:
        #     camera.start()
        # # See if the hand is visible
        # print("Put hand in front of screen")
        # while True:
        #     handPose = handPoseDetection.getPose(camera.getFrame())
        #     landmark = handPoseDetection.getHandLandmark(handPose, Hand.LEFT_HAND, HandPart.WRIST)
        #     print(landmark)
        #     if landmark is not None:
        #         break
        # print("Done!")
        # # See if the hand is not rotated
        # print("Rotate hand to neutral position")
        # last_measured_neutral_angle = None
        # while True:
        #     handPose = handPoseDetection.getPose(camera.getFrame())
        #     handRotation = handPoseDetection.getHandRotation(handPose)
        #     if neutral_angle_min < abs(handRotation) < neutral_angle_max:
        #         last_measured_neutral_angle = abs(handRotation)
        #         break
        # print("Done")
        # # Let the user rotate their hand
        # print("Rotate hand as far as possible and then back to neutral")
        # last_measured_rotation = 0
        # while True:
        #     handPose = handPoseDetection.getPose(camera.getFrame())
        #     handRotation = handPoseDetection.getHandRotation(handPose, Hand.LEFT_HAND)
        #     if handRotation > last_measured_rotation:
        #         last_measured_rotation = handRotation
        #     if neutral_angle_min < handRotation < neutral_angle_max:
        #         break
        # print("All done!")




        # # TODO: See if user is completely in frame
        # # TODO: See if user is raising their arm
        # # TODO: See if user has rotated the left hand 180-ish degrees
        # # TODO: See if user has rotated the left hand back to 0-ish degrees
        # # TODO: Maybe not the full 180-ish degrees