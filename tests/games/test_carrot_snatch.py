import pytest
from unittest import mock
from twinkledeck import colours
from twinkledeck.games.carrot_snatch import (
    GAME_STATE_LOSE,
    GAME_STATE_PLAY,
    GAME_STATE_WIN,
    SANTA_STATE_ALERT,
    SANTA_STATE_AWAKE,
    Game,
    Santa,
    Rudolf,
)
from shims import time


@pytest.fixture
def td():
    return mock.Mock()


@pytest.fixture
def dial1(td):
    return td.dial1

@pytest.fixture
def lights(td):
    return td.lights


@pytest.fixture
def game():
    return Game(num_leds=50, frame_rate=10)


@pytest.fixture
def rudolf(game):
    return game.rudolf


class TestGame:
    def test_game_win_shows_green(self, game, td):
        game.state = GAME_STATE_WIN
        game.tick(td)
        assert td.lights.set_rgb.call_count == 50
        assert td.lights.set_rgb.call_args == ((49, *colours.GREEN),)

    def test_game_lose_shows_red(self, game, td):
        game.state = GAME_STATE_LOSE
        game.tick(td)
        assert td.lights.set_rgb.call_count == 50
        assert td.lights.set_rgb.call_args == ((49, *colours.BRIGHT_RED),)

    def test_game_state_reverts_to_play_on_button_press(self, game, td):
        game.state = GAME_STATE_LOSE
        td.button1.read.return_value = True
        game.tick(td)
        assert game.state == GAME_STATE_PLAY


class TestSanta:
    @pytest.fixture
    def santa(self, game):
        return game.santa

    def test_set_state(self, santa):
        santa.set_alert()
        assert santa.state == SANTA_STATE_ALERT

    def test_santa_wakes_up_if_rudolf_is_close_and_fast(self, santa, rudolf):
        time.ticks_diff.return_value = 1001
        rudolf.speed = 2
        rudolf.position = 35
        santa.tick()
        assert santa.state == SANTA_STATE_ALERT


    def test_state_changes_cannot_happen_too_close_to_each_other(self, santa, rudolf):
        time.ticks_diff.return_value = 1000
        rudolf.speed = 2
        rudolf.position = 35
        santa.tick()
        assert santa.state == SANTA_STATE_AWAKE

    def test_noisy_on_an_alert_santa_is_game_over(self, game, santa, rudolf):
        santa.set_alert()
        time.ticks_diff.return_value = 1001
        rudolf.speed = 2
        rudolf.position = 35
        santa.tick()
        assert santa.state == SANTA_STATE_ALERT
        assert game.state == GAME_STATE_LOSE


class TestRudolf:
    def test_rudolf_default_speed(self, rudolf):
        assert rudolf.speed == 0

    def test_rudolf_speed_drops_over_time(self, game, rudolf, dial1):
        dial1.value = 1
        for _ in range(game.frame_rate * 2):
            rudolf.tick(dial1)
        assert rudolf.speed == pytest.approx(0.135, abs=0.001)

    def test_rudolf_is_two_red_lights(self, rudolf, lights, dial1):
        dial1.value = 0
        rudolf.tick(dial1)
        rudolf.show(lights)
        assert lights.set_hsv.call_args_list == [
            ((0, 0, 1, 0.5),),
            ((1, 0, 1, 0.5),),
        ]

    def test_rudolf_max_position_is_before_santa(self, rudolf, lights, dial1):
        dial1.value = 1
        rudolf.tick(dial1)
        rudolf.show(lights)
        assert lights.set_hsv.call_args_list == [
            ((45, 0, 1, 0.5),),
            ((46, 0, 1, 0.5),),
        ]
