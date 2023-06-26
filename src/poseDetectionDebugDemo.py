from poseDetection.Camera import Camera
from poseDetection.BodyPoseDetection import BodyPoseDetection
from poseDetection.BodyPartType import BodyPartType
from poseDetection.BodyPose import BodyPose
from exerciseScorer.FuglMeyer import FuglMeyer # for functions `areShouldersStraight()` and `userIsFacingTheCamera()`
import cv2

def main():
    camera = Camera(cameraId=0)
    camera.start()
    bodyPoseDetection = BodyPoseDetection()
    currentBodyPose = BodyPose()
    bodyPartTypes = ["LEFT_UPPER_ARM", "LEFT_FOREARM", "RIGHT_UPPER_ARM", "RIGHT_FOREARM"]
    while True:
        frame = camera.getFrame()
        poseLandmarks = bodyPoseDetection.getPose(frame)
        frame = cv2.flip(frame, 1)
        shouldersStraight = FuglMeyer.areShouldersStraight(bodyPoseDetection, frame)
        cv2.putText(frame, "Schouders recht: "+str(shouldersStraight), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        facingCamera = FuglMeyer.userIsFacingTheCamera(bodyPoseDetection, frame)
        cv2.putText(frame, "Gebruiker naar camera gericht: "+str(facingCamera), (0,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        currentBodyPoseData = currentBodyPose.createPose(poseLandmarks, bodyPartTypes)
        if currentBodyPoseData is not None:
            for index, item in enumerate(currentBodyPoseData):
                for plane in ["xy", "yz", "xz"]:
                    item["heading"][plane] = round(item["heading"][plane])
                cv2.putText(frame, "Body part: "+BodyPartType.serialize(item["body_part"])+"; Hoeken: "+str(item["heading"]), (0,50*(index+3)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            exit(0)
main()