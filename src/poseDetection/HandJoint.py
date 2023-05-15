class HandJoint:
    def __init__(self, handType, handJointType, position):
        self.handType = handType
        self.handJointType = handJointType
        self.position = position
    @staticmethod
    def createFromLandmarks(handType, handJointType, handPoseData, handLandmarksIndex):
        try:
            landmark = handPoseData.multi_hand_landmarks[handLandmarksIndex].landmark[handJointType]
            x, y, z = landmark.x, landmark.y, landmark.z
            return HandJoint(handType, handJointType, {"x": x, "y": y, "z": z})
        except:
            return None
    def getHandType(self):
        return self.handType
    def getHandJointType(self):
        return self.handJointType
    def getPosition(self):
        return self.position