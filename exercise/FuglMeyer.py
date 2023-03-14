class FuglMeyer:
    def __init__(self):
        self.active_test = None
    
    def test_hand_rotation(self, bodyPose):
        neutral_angle_min = -10
        neutral_angle_max = 10
        # TODO: See if user is completely in frame
        # TODO: See if user is raising their arm
        # TODO: See if user has rotated the left hand 180-ish degrees
        # TODO: See if user has rotated the left hand back to 0-ish degrees
        # TODO: Maybe not the full 180-ish degrees