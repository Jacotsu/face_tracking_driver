#!/usr/bin/env python3
import argparse
import logging
import cv2
import stream_backend
import video_frontend
import face_tracker
import command_output
from utils import RangeContainer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('face_to_track',
                        nargs=1,
                        help='The filename of the image that contains the'
                        'face to track')

    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Starts in debug mode. This mode shows you the'
                        'various threshold and the video feed in a window')

    parser.add_argument('-t', '--distance-threshold-for-movement',
                        dest='distance_threshold',
                        nargs=1, default=0.2, type=float,
                        choices=RangeContainer(0, 1),
                        help='The distance threshold relative to the pivot'
                        'point that must be excedeed to'
                        'make the webcam move. The threshold is a percentage'
                        'of the diagonal length in pixels of the video feed')

    parser.add_argument('-r', '--distance-threshold-for-rest',
                        dest='rest_threshold',
                        nargs=1, default=0.05, type=float,
                        choices=RangeContainer(0, 1),
                        help='The distance threshold relative to the pivot'
                        'point that you consider an acceptable minimum'
                        'distance. The threshold is a percentage'
                        'of the diagonal length in pixels of the video feed')

    parser.add_argument('-s', '--scale-factor',
                        dest='scale-factor',
                        nargs=1, default=0.2, type=float,
                        choices=RangeContainer(0, 1),
                        help='The scale factor for image processing. Smaller'
                        'values will make the processing faster but '
                        'it will be less accurate.')

    parser.add_argument('-f', '--faces-folder',
                        dest='face_folder',
                        nargs=1, default='faces', type=str,
                        help='The folders which contains the labeled faces'
                        'pictures. This is useful for debugging purposes')

    parser.add_argument('-p', '--pivot-point',
                        dest='pivot_point',
                        nargs=2, default=(0, 0), type=float,
                        choices=RangeContainer(0, 1),
                        help='The point from which the distances are measured.'
                        '(The point must be expressed in OpenGL screen coords'
                        ' aka bottom-left is (-1, -1) and top-right is (1, 1)')

    args = parser.parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    webcam = stream_backend.WebcamBackend()
    f_tracker = face_tracker.FaceTracker()

    driver = command_output.GenericOutput()

    if args.debug:
        show_window = video_frontend.VideoFrontend()
        while True:
            frame = webcam.get_frame()
            face_locations, face_names = f_tracker.process_frame(frame)
            show_window.highlight_faces(frame,
                                        face_locations,
                                        face_names,
                                        args.face_to_track[0])
            show_window.draw_relative_circle(frame, args.pivot_point,
                                             args.distance_threshold)

            show_window.draw_relative_circle(frame, args.pivot_point,
                                             args.rest_threshold,
                                             (0, 255, 0))
            try:
                tracked_face_loc = face_locations[face_names.
                                                  index(args.face_to_track[0])]
                displacement = f_tracker.\
                    calculate_displacement_vector(frame, tracked_face_loc)
                driver.update(displacement)
            except ValueError:
                pass
            cv2.imshow('Face tracker', frame)
            cv2.waitKey(1)
        show_window.terminate()
    else:
        while True:
            frame = webcam.get_frame()
            face_locations, face_names = f_tracker.process_frame(frame)
            try:
                tracked_face_loc = face_locations(face_names.
                                                  index(args.face_to_track[0]))
                displacement = f_tracker.\
                    calculate_displacement_vector(frame, tracked_face_loc)
                driver.update(displacement)
            except ValueError:
                pass

    webcam.release()
