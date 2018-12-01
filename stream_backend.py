import cv2


class WebcamBackend():
    def __init__(self, webcam_id=0):
        self.video_capture = cv2.VideoCapture(webcam_id)

    def get_frame(self, ignore_frames=0):
        """
            :param ignore_frames: How many frames to ignore for each iteration
                                  processing all the frames may not be
                                  necessary
            :type ignore_frames: int
            :return: The actual frame
            Gets a frame from the webcam
        """
        for x in range(ignore_frames):
            self.video_capture.read()

        ret, frame = self.video_capture.read()
        return frame

    def release(self):
        "Releases the webcam"
        self.video_capture.release()
