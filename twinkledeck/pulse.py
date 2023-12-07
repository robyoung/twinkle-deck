try:
    import shims.time as time
except ImportError:
    import time

PULSE_START_BRIGHT = 0
PULSE_START_DIM = 1

PULSE_AS_ONE = 0
PULSE_FROM_CENTER = 1 << 1

HSV_MAX_VALUE = 0.9
HSV_MIN_VALUE = 0.3
HSV_DEFAULT_VALUE = 0.6

PULSE_DURATION = 3000

class Pulser:
    state = -1
    pulsing = False
    pulse_start = None


    def pulse(self, pulse_type):
        if self.pulsing:
            return

        assert 0 <= pulse_type <= PULSE_START_DIM | PULSE_FROM_CENTER

        self.pulsing = True
        self.state = pulse_type
        self.pulse_start = time.ticks_ms()
        # print(f"pulse_start: {self.pulse_start}")

    def tick(self):
        if not self.pulsing:
            return
        self.current_tick = time.ticks_ms()
        self.time_since_start = time.ticks_diff(self.current_tick, self.pulse_start)
        if self.time_since_start > PULSE_DURATION:
            self.pulsing = False
            self.state = -1
            self.pulse_start = None

        # print(f"main_value: {self.main_value()}")

    def main_value(self):
        if not self.pulsing:
            return HSV_DEFAULT_VALUE

        if self.state & PULSE_START_BRIGHT == PULSE_START_BRIGHT:
            if self.time_since_start < 1000:
                return HSV_MAX_VALUE
            else:
                time_available = PULSE_DURATION - 1000
                time_used = self.time_since_start - 1000
                value_range = HSV_MAX_VALUE - HSV_DEFAULT_VALUE
                return value_range * (time_available - time_used) / time_available + HSV_DEFAULT_VALUE
        else:
            if self.time_since_start < 1000:
                return HSV_MIN_VALUE
            else:
                time_available = PULSE_DURATION - 1000
                time_used = self.time_since_start - 1000
                value_range = HSV_DEFAULT_VALUE - HSV_MIN_VALUE
                return value_range * time_used / time_available + HSV_MIN_VALUE

    def value(self, offset, size):
        if not self.pulsing:
            return HSV_DEFAULT_VALUE

        value = self.main_value()

        if self.state & PULSE_FROM_CENTER == PULSE_FROM_CENTER:
            return value - value / size * offset
        else:
            return value
