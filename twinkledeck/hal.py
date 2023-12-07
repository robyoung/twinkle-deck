from pimoroni import Button
from plasma import plasma2040
import plasma
from machine import ADC

from twinkledeck import constants
from twinkledeck.dial import Dial



button1 = Button(constants.BUTTON1)
button2 = Button(constants.BUTTON2)
button3 = Button(constants.BUTTON3)

dial1 = Dial(ADC(constants.KNOB1), constants.KNOB1_MIN, constants.KNOB1_MAX)
dial2 = Dial(ADC(constants.KNOB2), constants.KNOB2_MIN, constants.KNOB2_MAX)
dial3 = Dial(ADC(constants.KNOB3), constants.KNOB3_MIN, constants.KNOB3_MAX)

lights = plasma.WS2812(constants.NUM_LEDS, 0, 0, plasma2040.DAT)
lights.start()
