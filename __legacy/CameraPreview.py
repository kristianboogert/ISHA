import cv2

class CameraPreview:
    ###
    # Public
    ###

    def show(self, camera):
        try:
            camera.start()
            while True:
                frame = camera.getFrame()
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) == ord('q'):
                    break
        finally:
            camera.stop()
