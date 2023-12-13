import time

import twinkledeck.hal as td
from twinkledeck.pulse import RegularPulser, ErraticPulser

SANTA_STATE_ALERT = 0
SANTA_STATE_AWAKE = 1
SANTA_STATE_SLEEP = 2

class Santa:
    def __init__(self):
        self.set_awake()

    def set_awake(self):
        self.state = SANTA_STATE_AWAKE
        self.pulser = RegularPulser(min_value=0.3, duration=1000)

    def set_alert(self):
        self.state = SANTA_STATE_ALERT
        self.pulser = ErraticPulser(min_value=0.3, max_duration=1000)

    def set_sleep(self):
        self.state = SANTA_STATE_SLEEP
        self.pulser = RegularPulser(min_value=0.1, max_value=0.6, duration=3000)


    def show(self):
        value = self.pulser.value()
        td.lights.set_hsv(47, 0, 1, value) # santa
        td.lights.set_hsv(48, 0, 1, value) # santa
        td.lights.set_hsv(49, 0, 0, 0.5) # hat
        

class Carrot:
    def __init__(self, position):
        self.position = position

    def show(self):
        td.lights.set_hsv(self.position)


class Rudolf:
    position = 0
    speed = 0

    def __init__(self):
        self.position = 0
        self.speed = 0

    def show(self):
        position = int(self.position * (td.NUM_LEDS - 3))
        pass

def main():
    while True:

        time.sleep(1.0 / 60)


main()
