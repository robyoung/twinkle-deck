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

    @property
    def current_value(self):
        return self._current_value

    @abstractmethod
    def value(self):
        ...


class FlatPulser(BasePulser):
    def __init__(self, current_value=0.0):
        super().__init__(current_value)

    def value(self):
        return self._current_value


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
