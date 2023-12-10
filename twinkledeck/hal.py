"""Hardware Abstraction Layer for TwinkleDeck

This module provides the interface to the TwinkleDeck hardware. Try to
keep all hardware specific code in this module. This will make it easier
to test non-hardware specific code.
"""
from pimoroni import Button
from plasma import plasma2040
import plasma
from machine import ADC

from twinkledeck.dial import Dial

ADC2 = KNOB1 = 28
ADC1 = KNOB2 = 27
ADC0 = KNOB3 = 26

KNOB1_MIN = 144
KNOB1_MAX = 65247

KNOB2_MIN = 65359
KNOB2_MAX = 192

KNOB3_MIN = 65327
KNOB3_MAX = 176

I2C_SCL = BUTTON1 = 21
I2C_INT = BUTTON2 = 19
I2C_SDA = BUTTON3 = 20

NUM_LEDS = 50


button1 = Button(BUTTON1)
button2 = Button(BUTTON2)
button3 = Button(BUTTON3)

dial1 = Dial(ADC(KNOB1), KNOB1_MIN, KNOB1_MAX)
dial2 = Dial(ADC(KNOB2), KNOB2_MIN, KNOB2_MAX)
dial3 = Dial(ADC(KNOB3), KNOB3_MIN, KNOB3_MAX)

lights = plasma.WS2812(
    NUM_LEDS, 0, 0, plasma2040.DAT, rgbw=False, color_order=plasma.COLOR_ORDER_RGB
)
lights.start()
