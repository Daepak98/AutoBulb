from random import Random
import numpy as np


class PositionReporter:
    '''
    Reports the position(s) of a human in a given room. Requires a camera model to instantiate it
    '''

    def __init__(self, layout: np.ndarray) -> None:
        self.layout = layout
        pass

    def get_positions(self) -> list:
        pass


#-------------------------------------------------------------------#
import random


class RandomPositionReporter(PositionReporter):
    def __init__(self, layout: np.ndarray) -> None:
        super().__init__(layout)

    def get_positions(self) -> list:
        reported = []
        num_points = random.randint(0, 5)
        for _ in range(num_points):
            x = random.random() * (self.layout.shape[1] + 6) - 3
            y = random.random() * (self.layout.shape[0] + 6) - 3
            reported.append((x, y))
        return reported


#-------------------------------------------------------------------#
import cv2


class CameraPositionReporter(PositionReporter):
    # out = cv2.VideoWriter(
    #     'output.avi',
    #     cv2.VideoWriter_fourcc(*'MJPG'),
    #     15.,
    #     (640, 480)
    # )

    def __init__(self, camera_id, layout: np.ndarray, image_points: np.ndarray, world_points: np.ndarray) -> None:
        super().__init__(layout)
        self.frame_num = 1
        self.feed = cv2.VideoCapture(camera_id)
        self.camera_model, _ = cv2.findHomography(
            image_points, world_points, method=cv2.RANSAC)

        # initialize the HOG descriptor/person detector
        self.__hog = cv2.HOGDescriptor()
        self.__hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def get_positions(self) -> list:
        ret, frame = self.feed.read()
        print("Frame Number: ", self.frame_num)
        if ret:
            # resizing for faster detection
            frame = cv2.resize(frame, (640, 480))

            # using a greyscale picture, also for faster detection
            # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            # detect people in the image
            # returns the bounding boxes for the detected objects
            boxes, weights = self.__hog.detectMultiScale(
                frame, winStride=(8, 8))

            boxes = np.array([[x + 0.75 * w, y, x + w, y + h]
                             for (x, y, w, h) in boxes])

            positions = []
            for (xA, yA, xB, yB) in boxes:
                xM, yM = np.mean([xA, xB]), np.mean([yA, yB])
                cv2.circle(frame, center=(int(xM), int(yM)),
                           radius=10, thickness=-1, color=(0, 255, 0))
                # CameraPositionReporter.out.write(frame.astype('uint8'))
                homog_pt = np.array([xM, yM, 1]).reshape((3, 1))
                transformed = self.camera_model @ homog_pt
                positions.append(
                    ((transformed[1] / transformed[-1])[0],
                     (transformed[0] / transformed[-1])[0]))
            self.frame_num += 1
            return positions
        else:
            return False


import time
import matplotlib.pyplot as plt
if __name__ == "__main__":
    image_points = np.loadtxt(
        "./resources/image_points.csv", dtype=np.float32, delimiter=",")
    world_points = np.loadtxt(
        "./resources/world_points.csv", dtype=np.float32, delimiter=",")
    # plt.scatter(world_points[:, 0], world_points[:, 1], marker='s')
    # plt.show()
    cpr = CameraPositionReporter(
        "C:/Users/bunch/Projects/Managed_Projects/AutoBulb/resources/ryan_video.mp4",
        np.ones((3, 4)),
        image_points, world_points)
    while cpr.get_positions() != False:
        pass
    # homogeneous = np.hstack(
    #     (image_points, np.ones((image_points.shape[0], 1))))
    # transformed = np.apply_along_axis(
    #     lambda row: cpr.camera_model @ row, axis=1, arr=homogeneous)
    # plt.scatter(world_points[:, 0], world_points[:, 1], marker='s')
    # plt.scatter(transformed[:, 0] / transformed[:, -1],
    #             transformed[:, 1] / transformed[:, -1], marker='o')
    # plt.show()
