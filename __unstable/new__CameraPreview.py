import cv2

class CameraPreview:
    ###
    # Public
    ###

    def __init__(self, camera):
        self.camera = camera
    def show(self):
        try:
            self.camera.start()
            while True:
                frame = self.camera.getFrame()
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) == ord('q'):
                    break
        finally:
            self.camera.stop()
