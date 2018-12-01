from os import walk, path
import cv2
import logging
import face_recognition
import math


class FaceTracker:
    def __init__(self,
                 faces_folder='faces',
                 threshold=0.2,
                 rest_threshold=0.05,
                 pivot=(0, 0),
                 scale_factor=0.25):
        self.pivot = pivot
        self.threshold = threshold
        self.rest_threshold = rest_threshold
        self.scale_factor = scale_factor
        self.triggered = False
        self.known_encodings = []
        self.face_names = []

        for (dirpath, dirnames, filenames) in walk(faces_folder):
            for img in filenames:
                image = face_recognition.load_image_file(path.join(dirpath,
                                                                   img))
                self.known_encodings.append(face_recognition.
                                            face_encodings(image)[0])
                self.face_names.append(img)

    def process_frame(self, frame):
        small_frame = cv2.resize(frame, (0, 0),
                                 fx=self.scale_factor, fy=self.scale_factor)
        rgb_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame,
                                                         face_locations)

        face_names = []
        for i, face_encoding in enumerate(face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_encodings,
                                                     face_encoding)
            name = "Anon"

            if True in matches:
                first_match_index = matches.index(True)
                name = self.face_names[first_match_index]

            logging.debug(f"Detected {name} @ {face_locations[i]}")
            face_names.append(name)

        return face_locations, face_names

    def get_center_of_face_bounds(self, face_location):
        return ((face_location[0]+face_location[2])/(2*self.scale_factor),
                (face_location[1]+face_location[3])/(2*self.scale_factor))

    def calculate_displacement_vector(self, frame, face_location):
        pos = self.get_center_of_face_bounds((face_location[0]/frame.shape[0],
                                              face_location[1]/frame.shape[1],
                                              face_location[2]/frame.shape[0],
                                              face_location[3]/frame.shape[1])
                                             )
        displacement = (self.pivot[0] - pos[0], self.pivot[1] - pos[1])
        length = math.hypot(*displacement)
        logging.debug(length)
        if length > self.threshold:
            self.triggered = True
        elif length < self.rest_threshold:
            self.triggered = False
            return (0, 0)

        if self.triggered:
            return displacement
