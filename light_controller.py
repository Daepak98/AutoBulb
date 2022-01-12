class LightController:
    def __init__(self) -> None:
        self.lights = {}

    def update_lights(self, *positions: tuple) -> None:
        if positions:
            for position in positions:
                for light in self.lights:
                    # TODO: Can update to handle variable lighting
                    if self.in_sector(light, position):
                        self.set_light_state(light, True)
                    else:
                        self.set_light_state(light, False)
        else:
            for light in self.lights:
                self.set_light_state(light, False)

    def in_sector(self, light_id: int, position: tuple) -> bool:
        if position[0] >= self.lights[light_id]['width'][0] and position[0] <= self.lights[light_id]['width'][1] + 1:
            if position[1] >= self.lights[light_id]['height'][0] and position[1] <= self.lights[light_id]['height'][1] + 1:
                return True

    def set_light_state(self, light_id: int, end_state: bool) -> None:
        self.lights[light_id]['status'] = end_state


import numpy as np


class RectMatrixLightController(LightController):
    def __init__(self, layout: np.ndarray) -> None:
        self.lights = {}
        class_vals = np.unique(layout)
        for class_val in class_vals:  # Segmentation of Matrix Data
            masked = layout == class_val
            indices = np.where(masked == True)
            self.lights[class_val] = {}
            self.lights[class_val]['height'] = (indices[0][0], indices[0][-1])
            self.lights[class_val]['width'] = (indices[1][0], indices[1][-1])
            self.lights[class_val]['status'] = False


import random
if __name__ == "__main__":
    layout = np.array([[1, 1, 1, 1, 2, 2],
                       [1, 1, 1, 1, 2, 2],
                       [1, 1, 1, 1, 3, 3],
                       [1, 1, 1, 1, 3, 3]])
    m = RectMatrixLightController(layout)
    for _ in range(10):
        pos = (layout.shape[0] * random.random(),
               layout.shape[1] * random.random())
        m.update_lights(pos)
        print(pos)
        print(m.lights)
