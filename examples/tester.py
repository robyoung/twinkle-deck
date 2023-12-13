"""HSV test

This example tests out all the buttons and dials on the interface.
The dials control Hue, Saturation and Value.
The buttons control which lights are on.
"""
import twinkledeck.hal as td
import time

ALL_ON = 1 << 0
TWOS_OFF = 1 << 1

RGB = 0 << 2
HSV = 1 << 2

light_flags = ALL_ON
prev_light_flags = None
prev_dial1 = None
prev_dial2 = None
prev_dial3 = None


def get_colour(light_flags, dial1, dial2, dial3):
    if light_flags & HSV:
        return dial1, dial2, dial3
    else:
        return int(dial1 * 255), int(dial2 * 255), int(dial3 * 255)

while True:
    dial1 = round(td.dial1.value, 2)
    dial2 = round(td.dial2.value, 2)
    dial3 = round(td.dial3.value, 2)

    if td.button1.read():
        light_flags = ALL_ON
    elif td.button2.read():
        light_flags |= TWOS_OFF
        light_flags ^= ALL_ON
    elif td.button3.read():
        light_flags ^= HSV  # toggle between RGB and HSV

    if (
        light_flags != prev_light_flags
        or dial1 != prev_dial1
        or dial2 != prev_dial2
        or dial3 != prev_dial3
    ):
        colour = get_colour(light_flags, dial1, dial2, dial3)
        if light_flags & HSV:
            print(f"H({dial1}) S({dial2}) V({dial3})")
        else:
            print(f"R({colour[0]}) G({colour[1]}) B({colour[2]})")
        for i in range(td.NUM_LEDS):
            if i % 2 == 0 and light_flags & TWOS_OFF:
                should_show = False
            else:
                should_show = True

            if should_show:
                if light_flags & HSV:
                    td.lights.set_hsv(i, *colour)
                else:
                    td.lights.set_rgb(i, *colour)
            else:
                td.lights.set_hsv(i, 0, 0, 0)

    prev_light_flags = light_flags
    prev_dial1 = dial1
    prev_dial2 = dial2
    prev_dial3 = dial3

    time.sleep(1.0 / 60)
