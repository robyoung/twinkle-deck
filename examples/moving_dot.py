# Moving Dot
# ==========
#
# This example tests moving a dot with a dial.
#
# Dial1 controls the dot position
# Dial2 controls the size of the skirt
# Dial3 controls the colour of the dot
#
# Button1 pulses the dot bright as one
# Button2 pulses the dot bright from the middle
# Button3 pulses the dot dim as one
import twinkledeck.hal as td
from twinkledeck.pulse import Pulser, PULSE_START_BRIGHT, PULSE_START_DIM, PULSE_AS_ONE, PULSE_FROM_CENTER
import time

NUM_LEDS = td.constants.NUM_LEDS
MAX_SKIRT_SIZE = 5

def main():
    pulser = Pulser(duration=2000, max_period=300)
    prev_dials = (None, None, None)
    while True:
        position = int(td.dial1.value * NUM_LEDS)
        skirt_size = int(td.dial2.value * MAX_SKIRT_SIZE)
        hue = round(td.dial3.value, 2)

        if td.button1.read():
            pulser.pulse(PULSE_START_BRIGHT | PULSE_AS_ONE)
        elif td.button2.read():
            pulser.pulse(PULSE_START_BRIGHT | PULSE_FROM_CENTER)
        elif td.button3.read():
            pulser.pulse(PULSE_START_DIM | PULSE_AS_ONE)

        if pulser.pulsing or (position, skirt_size, hue) != prev_dials:
            pulser.tick()
            for i in range(td.constants.NUM_LEDS):
                offset = abs(position - i)
                if offset <= skirt_size:
                    value = pulser.value(offset, skirt_size) 
                    td.lights.set_hsv(i, hue, 1, value)
                else:
                    td.lights.set_hsv(i, 0, 0, 0)
            
            prev_dials = (position, skirt_size, hue)

        time.sleep(1.0 / 60)

main()
