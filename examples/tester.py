# HSV test
# ========
#
# This example tests out all the buttons and knobs on the interface.
# The knobs control Hue, Saturation and Value.
import twinkledeck as td
import time

ALL_ON = 1 << 2
TWOS_OFF = 1 << 1
THREES_OFF = 1 << 0

light_flags = ALL_ON
prev_light_flags = None
prev_hue = None
prev_sat = None
prev_val = None

while True:
    hue = (td.knob1.value / 100) * 360
    sat = td.knob2.value
    val = td.knob3.value

    if td.button1.read():
        light_flags = ALL_ON
    elif td.button2.read():
        light_flags |= TWOS_OFF
        light_flags ^= ALL_ON
    elif td.button3.read():
        light_flags |= THREES_OFF
        light_flags ^= ALL_ON

    if (
        light_flags != prev_light_flags
        or hue != prev_hue
        or sat != prev_sat
        or val != prev_val
    ):
        for i in range(td.constants.NUM_LEDS):
            if i % 2 == 0 and light_flags & TWOS_OFF:
                should_show = False
            elif i % 3 == 0 and light_flags & THREES_OFF:
                should_show = False
            else:
                should_show = True

            if should_show:
                td.lights.set_hsv(i, hue, sat, val)
            else:
                td.lights.set_hsv(i, 0, 0, 0)

    prev_light_flags = light_flags
    prev_hue = hue
    prev_sat = sat
    prev_val = val

    time.sleep(1.0 / 60)
