from pimoroni import Button
from machine import ADC

import .constants

class TwinkleKnob:
    def __init__(self, pin, factor, offset):
        self.adc = ADC(pin)
        self.factor = factor
        self.offset = offset

    @property
    def value(self):
        return (self.adc.read_u16() * self.factor) + self.offset

button1 = Button(constants.BUTTON1)
button2 = Button(constants.BUTTON2)
button3 = Button(constants.BUTTON3)

knob1 = TwinkleKnob(constants.KNOB1, 1, 0)
knob2 = TwinkleKnob(constants.KNOB2, 1, 0)
knob3 = TwinkleKnob(constants.KNOB3, 1, 0)
