import cv2
from math import sqrt, hypot


class VideoFrontend():
    def __init__(self, webcam_id=0, scale_factor=4.0):
        self.scale_factor = scale_factor

    def draw_relative_circle(self, frame, center, radius, color=(255, 0, 0)):
        x_res = frame.shape[1]
        y_res = frame.shape[0]
        abs_radius = int(hypot(x_res, y_res)*radius)
        abs_center = (int((center[0] + 1)*x_res/2),
                      int((center[1] + 1)*y_res/2))
        cv2.circle(frame, abs_center, abs_radius, color)
        return frame

    def highlight_faces(self, frame, face_locations, face_names, highligth=''):
        for (top, right, bottom, left), name in zip(face_locations,
                                                    face_names):
            frame_color = (0, 255, 239)
            text_color = (0, 0, 0)

            if highligth == name:
                frame_color = (0, 0, 255)
                text_color = (255, 255, 255)

            top *= self.scale_factor
            right *= self.scale_factor
            bottom *= self.scale_factor
            left *= self.scale_factor

            top = int(top)
            right = int(right)
            bottom = int(bottom)
            left = int(left)

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), frame_color,
                          2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom),
                          frame_color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font,
                        1.0, text_color, 1)

    def terminate(self):
        "Destroys all the windows"
        cv2.destroyAllWindows()
