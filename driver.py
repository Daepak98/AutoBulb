import numpy as np
import time
import threading

from light_controller import RectMatrixLightController
from position_reporter import CameraPositionReporter
from hw_interface import LightHardwareInterface, PiLEDHardwareInterface

if __name__ == "__main__":
    # layout = np.ones((3, 4))
    layout = np.array([[1, 1, 1, 1],
                       [2, 2, 2, 2],
                       [3, 3, 3, 3]])
    image_points = np.loadtxt(
        "./resources/image_points.csv", dtype=np.float32, delimiter=",")
    world_points = np.loadtxt(
        "./resources/world_points.csv", dtype=np.float32, delimiter=",")

    lc = RectMatrixLightController(layout)
    pr = CameraPositionReporter("/home/pi/AutoBulb/resources/ryan_video.mp4",
                                layout,
                                image_points,
                                world_points)
    lm = PiLEDHardwareInterface(light_model=lc.lights,
                                GPIO_pins=[17, 27, 22],
                                change_delay=10)

    positions = pr.get_positions()
    while positions != False:
        lc.update_lights(*positions)
        lm.listen_to_light_model(lc.lights)
    # if positions:
        print(positions)
        print(lc.lights)
        print(lm.delay_timer)
        print()
        positions = pr.get_positions()
