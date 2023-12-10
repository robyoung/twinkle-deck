from twinkledeck.pulse import ErraticPulser
from shims import time, random
import pytest


@pytest.fixture
def pulser():
    return ErraticPulser()


def test_erratic_pulser_does_not_change_within_min_duration(pulser):
    time.ticks_diff.return_value = 100

    assert pulser.value() == 0.0


def test_erratic_pulser_may_not_change_below_max_duration(pulser):
    time.ticks_diff.return_value = 300
    random.getrandbits.return_value = 0

    assert pulser.value() == 0.0


def test_erratic_pulser_may_change_below_max_duration(pulser):
    time.ticks_diff.return_value = 300
    random.getrandbits.return_value = 1
    random.uniform.return_value = 1.0

    assert pulser.value() == 1.0


def test_erratic_pulser_must_change_above_max_duration(pulser):
    time.ticks_diff.return_value = 2100
    random.getrandbits.return_value = 0
    random.uniform.return_value = 1.0

    assert pulser.value() == 1.0


def test_erratic_pulser_wraps_to_bottom(pulser):
    time.ticks_diff.return_value = 1000
    random.getrandbits.return_value = 1
    random.uniform.return_value = 0.8

    assert pulser.value() == 0.8
    assert round(pulser.value(), 2) == 0.6
