from twinkledeck.pulse import RegularPulser
from shims import time
import pytest


@pytest.fixture
def pulser():
    return RegularPulser(duration=1000)


def test_regular_pulse(pulser):
    time.ticks_diff.return_value = 100

    assert pulser.value() == 0.2


def test_regular_pulse_wraps_to_start(pulser):
    time.ticks_diff.return_value = 1000

    assert pulser.value() == 0.0


def test_regular_pulser_wraps_top(pulser):
    time.ticks_diff.return_value = 600

    assert pulser.value() == 0.8


def test_regular_pulser_wraps_bottom(pulser):
    time.ticks_diff.return_value = 1100

    assert round(pulser.value(), 2) == 0.2
