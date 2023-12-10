"""Guess the number

A random number of lights will quickly flash on and then off again.
You must then turn the dial until the same number of lights is showing.
"""
import twinkledeck.hal as td
import random
import time

MAX_LIGHTS = 10
MAX_FLASH_TIME = 0.8
MIN_FLASH_TIME = 0.1
DEFAULT_FLASH_TIME = 0.5

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)

STATE_SETTING_MAX_LIGHTS = 1
STATE_SETTING_TIME = 2
STATE_SHOWING = 3
STATE_GUESSING = 4
STATE_RESULTS = 5


def show_number(number, flash_time):
    step = int(td.NUM_LEDS / (number + 1))

    td.lights.clear()
    for i in range(number):
        td.lights.set_rgb((i + 1) * step, *WHITE)

    time.sleep(flash_time)
    td.lights.clear()


def guessing(max_lights, last_guess):
    guess = round(td.dial1.value * max_lights)
    if guess != last_guess:
        td.lights.clear()
        for i in range(guess):
            td.lights.set_rgb(i, *WHITE)
    return guess


def get_max_lights_setting(current_max_lights, is_new_state):
    new_max_lights = round(td.dial1.value * (MAX_LIGHTS - 1)) + 1
    if new_max_lights != current_max_lights or is_new_state:
        td.lights.clear()
        td.lights.set_rgb(0, *ORANGE)
        val = new_max_lights / MAX_LIGHTS
        red = 255 * val
        green = 255 - red
        for i in range(new_max_lights):
            td.lights.set_rgb(i + 1, int(red), int(green), 0)
    return new_max_lights


def get_flash_time(current_flash_time, is_new_state):
    new_flash_time = round(
        (MAX_FLASH_TIME - MIN_FLASH_TIME) * (1 - td.dial1.value) + MIN_FLASH_TIME, 2
    )
    if new_flash_time != current_flash_time or is_new_state:
        td.lights.clear()
        td.lights.set_rgb(0, *PURPLE)

        val = 1 - (new_flash_time - MIN_FLASH_TIME) / (MAX_FLASH_TIME - MIN_FLASH_TIME)
        red = 255 * val
        green = 255 - red
        for i in range(round(val * 10)):
            td.lights.set_rgb(i + 1, int(red), int(green), 0)

    return new_flash_time


def is_new_state(_state, _previous_state):
    if _state != _previous_state:
        return _state


def show_result(number, guess):
    colour = GREEN if guess == number else RED
    for i in range(td.NUM_LEDS):
        td.lights.set_rgb(i, *colour)


def advance_state(state):
    if state == STATE_SETTING_MAX_LIGHTS:
        return STATE_SETTING_TIME
    if state == STATE_SETTING_TIME:
        return STATE_SHOWING
    if state == STATE_SHOWING:
        return STATE_GUESSING
    if state == STATE_GUESSING:
        return STATE_RESULTS
    if state == STATE_RESULTS:
        return STATE_SHOWING


def main():
    _previous_state = None
    _state = STATE_SETTING_MAX_LIGHTS
    _max_lights = MAX_LIGHTS
    _flash_time = DEFAULT_FLASH_TIME
    number = None
    guess = None

    while True:
        if td.button3.read():
            _state = STATE_SETTING_MAX_LIGHTS

        _new_state = _state
        if _state == STATE_SETTING_MAX_LIGHTS:
            _max_lights = get_max_lights_setting(_max_lights, _state != _previous_state)
        elif _state == STATE_SETTING_TIME:
            _flash_time = get_flash_time(_flash_time, _state != _previous_state)
        elif _state == STATE_SHOWING:
            number = random.randrange(1, _max_lights)
            show_number(number, _flash_time)
            _new_state = advance_state(_state)
        elif _state == STATE_GUESSING:
            guess = guessing(_max_lights, guess)

        if td.button1.read():
            if _state in (STATE_SETTING_MAX_LIGHTS, STATE_SETTING_TIME):
                _new_state = advance_state(_state)
            elif _state == STATE_GUESSING:
                show_result(number, guess)
                guess = None
                _new_state = advance_state(_state)
            elif _state == STATE_RESULTS:
                _new_state = advance_state(_state)

        _previous_state = _state
        _state = _new_state

        time.sleep(1.0 / 60)


main()
