"""Carrot snatch

You play as Rudolf the Red Nosed Reindeer. Santa has a box of juicy carrots but he has
said that they cannot be eaten until after the presents have been delivered.
You cannot wait!

Santa is at the far end of the string. He is a red light and a white light.
In front of Santa are 3 orange carrots.
You are Rudolf, a red dot at the other end of the string.
You must slowly up to the carrots and take one back to the start.
"""
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
        td.lights.set_hsv(47, 0, 1, value)  # santa
        td.lights.set_hsv(48, 0, 1, value)  # santa
        td.lights.set_hsv(49, 0, 0, 0.5)  # hat


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
