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
from twinkledeck.pulse import (
    ErraticPulser,
    RegularPulser,
    FlatPulser,
)
import time

NUM_LEDS = td.NUM_LEDS
MAX_SKIRT_SIZE = 5


def main():
    pulser = FlatPulser(current_value=1.0)
    prev_dials = (None, None, None)
    while True:
        position = int(td.dial1.value * NUM_LEDS)
        skirt_size = int(td.dial2.value * MAX_SKIRT_SIZE)
        hue = round(td.dial3.value, 2)

        if td.button1.read():
            pulser = RegularPulser(
                current_value=pulser.current_value,
                duration=5000,
            )
        elif td.button2.read():
            pulser = FlatPulser(current_value=1.0)
        elif td.button3.read():
            pulser = ErraticPulser(
                current_value=pulser.current_value,
                max_duration=5000,
            )

        if (position, skirt_size, hue) != prev_dials or isinstance(
            pulser, (ErraticPulser, RegularPulser)
        ):
            for i in range(td.NUM_LEDS):
                offset = abs(position - i)
                if offset <= skirt_size:
                    td.lights.set_hsv(i, hue, 1, pulser.value())
                else:
                    td.lights.set_hsv(i, 0, 0, 0)

            prev_dials = (position, skirt_size, hue)

        time.sleep(1.0 / 60)


main()
