from abc import ABCMeta, abstractmethod


try:
    import shims.time as time
    import shims.random as random
except ImportError:
    import time
    import random

PULSE_START_BRIGHT = 0
PULSE_START_DIM = 1

PULSE_AS_ONE = 0
PULSE_FROM_CENTER = 1 << 1

HSV_MAX_VALUE = 0.9
HSV_MIN_VALUE = 0.3
HSV_DEFAULT_VALUE = 0.6

PULSE_DURATION = 1000


class BasePulser(metaclass=ABCMeta):
    def __init__(self, current_value=0.0, min_value=0.0, max_value=1.0):
        self._previous_time = time.ticks_ms()
        self._current_value = current_value
        self.min_value = min_value
        self.max_value = max_value

    def _time_diff(self):
        current_time = time.ticks_ms()
        time_diff = time.ticks_diff(self._previous_time, current_time)
        self._previous_time = current_time
        return time_diff

    @abstractmethod
    def value(self):
        ...


class RegularPulser(BasePulser):
    def __init__(
        self,
        current_value=0.0,
        min_value=0.0,
        max_value=1.0,
        duration=PULSE_DURATION,
    ):
        super().__init__(current_value, min_value, max_value)
        self.duration = duration
        self._direction = 1

    def value(self):
        time_diff = self._time_diff()

        step = ((self.max_value - self.min_value) / self.duration) * 2
        movement = time_diff * step * self._direction
        new_value = self._current_value + movement

        while new_value < self.min_value or new_value > self.max_value:
            if new_value > self.max_value:
                new_value = self.max_value - (new_value - self.max_value)
                self._direction *= -1
            elif new_value < self.min_value:
                new_value = self.min_value + (self.min_value - new_value)
                self._direction *= -1

        self._current_value = new_value
        return self._current_value


class ErraticPulser(BasePulser):
    def __init__(
        self,
        current_value=0.0,
        min_value=0.0,
        max_value=1.0,
        min_movement=0.5,
        min_duration=200,
        max_duration=2000,
    ):
        super().__init__(current_value, min_value, max_value)
        self.min_movement = min_movement
        self.min_duration = min_duration
        self.max_duration = max_duration

    def value(self):
        time_diff = self._time_diff()
        if time_diff < self.min_duration or (
            time_diff < self.max_duration and random.getrandbits(1) == 0
        ):
            return self._current_value

        step = random.randrange(self.min_movement, self.max_value - self.min_value)

        new_value = self._current_value + step
        if new_value > self.max_value:
            new_value = self.min_value + (new_value - self.max_value)

        self._current_value = new_value
        return self._current_value


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
                return (
                    value_range * (time_available - time_used) / time_available
                    + HSV_DEFAULT_VALUE
                )
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
