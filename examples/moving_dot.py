# Moving Dot
# ==========
#
# This example tests moving a dot with a knob.
#
# Knob1 controls the dot position
# Knob2 controls the size of the skirt
# Knob3 controls the colour of the dot
#
# Button1 pulses the dot bright as one
# Button2 pulses the dot bright from the middle
# Button3 pulses the dot dim as one
#
# Pulsing should take 3 seconds
# Pulsing should affect the value from 100% to 50%
import twinkledeck as td
import time

NUM_LEDS = td.constants.NUM_LEDS
MAX_SKIRT_SIZE = 5

DEFAULT_HSV_VALUE = 60
MAX_HSV_VALUE = 100
MIN_HSV_VALUE = 30
PULSE_DURATION_MS = 3000

PULSE_START_BRIGHT = 1
PULSE_START_DIM = 1 << 1
PULSE_AS_ONE = 1 << 2
PULSE_FROM_MIDDLE = 1 << 3

prev_knobs = (None, None, None)
pulsing = False
pulse_start = None


def calculate_pulse(pulse_type, pulse_since_start, size):
    pulse_time_proportion = pulse_since_start / PULSE_DURATION_MS
    if pulse_type | PULSE_START_BRIGHT:
        value_range = MAX_HSV_VALUE - DEFAULT_HSV_VALUE
        current_value = value_range * (1.0 - pulse_time_proportion) + DEFAULT_HSV_VALUE
    else:
        value_range = DEFAULT_HSV_VALUE - MIN_HSV_VALUE
        current_value = value_range * (pulse_time_proportion) + MIN_HSV_VALUE

    if pulse_type | PULSE_AS_ONE:
        return [current_value] * (size + 1)
    else:
        # TODO
        return [current_value] * (size + 1)


def calculate_pulse_value(position, values):
    if values is None:
        return 1.0
    else:
        return values[position]


while True:
    position = int((td.knob1.value / 100) * NUM_LEDS)
    size = int((td.knob2.value / 100) * MAX_SKIRT_SIZE)
    hue = int((td.knob3.value / 100) * 360)

    if td.button1.read():
        pulse = PULSE_START_BRIGHT | PULSE_AS_ONE
    elif td.button2.read():
        pulse = PULSE_START_BRIGHT | PULSE_FROM_MIDDLE
    elif td.button3.read():
        pulse = PULSE_START_DIM | PULSE_AS_ONE
    else:
        pulse = None

    if pulsing or (position, size, hue) != prev_knobs or pulse is not None:
        pulse_value = None
        if pulsing:
            pulse_since_start = time.ticks_diff(pulse_start, time.ticks_ms())
            if pulse_since_start > PULSE_DURATION_MS:
                pulsing = False
            else:
                pulse_value = calculate_pulse(pulse, pulse_since_start, size)

        for i in range(td.constants.NUM_LEDS):
            if (position - size) <= i <= (position + size):
                td.lights.set_hsv(
                    i,
                    hue,
                    1.0,
                    calculate_pulse_value(abs(position - i), pulse_value),
                )
            else:
                td.lights.set_hsv(i, 0, 0, 0)

    prev_knobs = (position, size, hue)

    time.sleep(1.0 / 60)
