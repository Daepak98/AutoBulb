from light_controller import LightController


class LightHardwareInterface:
    def __init__(self):
        pass

    def listen_to_light_model():
        pass


import time
import RPi.GPIO as GPIO


class PiLEDHardwareInterface(LightHardwareInterface):
    def __init__(self, light_model: dict, GPIO_pins: list, change_delay: int):
        self.LED_pins = GPIO_pins
        GPIO.setmode(GPIO.BCM)
        for LED_PIN in self.LED_pins:
            GPIO.setup(LED_PIN, GPIO.OUT)
        self.max_delay = change_delay
        self.delay_timer = {k: change_delay for k in light_model}

    def listen_to_light_model(self, light_model: dict):
        for lid in light_model:
            if self.delay_timer[lid] == 0:
                if light_model[lid]['status'] == True:
                    GPIO.output(self.LED_pins[lid - 1], GPIO.HIGH)
                else:
                    GPIO.output(self.LED_pins[lid - 1], GPIO.LOW)
                self.delay_timer[lid] = self.max_delay
            else:
                self.delay_timer[lid] -= 1

    def __del__(self):
        print("Cleaning Up GPIO channels")
        GPIO.cleanup()
