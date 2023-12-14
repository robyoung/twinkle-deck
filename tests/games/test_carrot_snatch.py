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


@pytest.fixture
def santa(game):
    return game.santa


class TestGame:
    def test_game_win_shows_green(self, game, td):
        # Given
        game.state = GAME_STATE_WIN

        # When
        game.tick(td)

        # Then
        assert td.lights.set_rgb.call_count == 50
        assert td.lights.set_rgb.call_args == ((49, *colours.GREEN),)

    def test_game_lose_shows_red(self, game, td):
        # Given
        game.state = GAME_STATE_LOSE

        # When
        game.tick(td)

        # Then
        assert td.lights.set_rgb.call_count == 50
        assert td.lights.set_rgb.call_args == ((49, *colours.BRIGHT_RED),)

    def test_game_state_reverts_to_play_on_button_press(self, game, td):
        # Given
        game.state = GAME_STATE_LOSE
        td.button1.read.return_value = True

        # When
        game.tick(td)

        # Then
        assert game.state == GAME_STATE_PLAY


class TestSanta:

    def test_set_state(self, santa):
        # When
        santa.set_alert()

        # Then
        assert santa.state == SANTA_STATE_ALERT

    def test_santa_wakes_up_if_rudolf_is_close_and_fast(self, santa, rudolf):
        # Given
        time.ticks_diff.return_value = 1001
        rudolf.speed = 2
        rudolf.position = 35

        # When
        santa.tick()

        # Then
        assert santa.state == SANTA_STATE_ALERT


    def test_state_changes_cannot_happen_too_close_to_each_other(self, santa, rudolf):
        # Given
        time.ticks_diff.return_value = 1000
        rudolf.speed = 2
        rudolf.position = 35

        # When
        santa.tick()

        # Then
        assert santa.state == SANTA_STATE_AWAKE

    def test_noisy_on_an_alert_santa_is_game_over(self, game, santa, rudolf):
        # Given
        santa.set_alert()
        time.ticks_diff.return_value = 1001
        rudolf.speed = 2
        rudolf.position = 35
        
        # When
        santa.tick()

        # Then
        assert santa.state == SANTA_STATE_ALERT
        assert game.state == GAME_STATE_LOSE


    def test_show_santa_with_all_carrots(self, santa, lights):
        # When
        santa.show(lights)

        # Then
        assert lights.set_hsv.call_args_list == [
            mock.call(47, 0, 1, 0.3014),
            mock.call(48, 0, 1, 0.3014),
            mock.call(49, 0, 0, 0.5),
        ]
        assert lights.set_rgb.call_args_list == [
            mock.call(46, *colours.ORANGE),
            mock.call(45, *colours.ORANGE),
            mock.call(44, *colours.ORANGE),
        ]


class TestRudolf:
    def test_rudolf_default_speed(self, rudolf):
        assert rudolf.speed == 0

    def test_rudolf_speed_drops_over_time(self, game, rudolf, dial1):
        # Given
        dial1.value = 1

        # When
        for _ in range(game.frame_rate * 2):
            rudolf.tick(dial1)

        # Then
        assert rudolf.speed == pytest.approx(0.135, abs=0.001)

    def test_rudolf_is_two_red_lights(self, rudolf, lights, dial1):
        # Given
        dial1.value = 0

        # When
        rudolf.tick(dial1)
        rudolf.show(lights)

        # Then
        assert lights.set_hsv.call_args_list == [
            ((0, 0, 1, 0.5),),
            ((1, 0, 1, 0.5),),
        ]

    def test_rudolf_max_position_is_before_santa(self, rudolf, lights, dial1):
        # Given
        dial1.value = 1

        # When
        rudolf.tick(dial1)
        rudolf.show(lights)

        # Then
        assert lights.set_hsv.call_args_list == [
            ((43, 0, 1, 0.5),),
            ((44, 0, 1, 0.5),),
        ]

    def test_rudolf_snatches_a_carrot(self, dial1, rudolf, santa):
        # Given
        dial1.value = 1

        # When
        rudolf.tick(dial1)

        # Then
        assert rudolf.carrot_in_hand == 1 and santa.num_carrots == 2

    def test_rudolf_deposits_a_carrot(self, dial1, rudolf, santa):
        # Given
        dial1.value = 0
        rudolf.carrot_in_hand = 1
        rudolf.num_carrots = 0
        santa.num_carrots = 2

        # When
        rudolf.tick(dial1)

        # Then
        assert rudolf.carrot_in_hand == 0 and rudolf.num_carrots == 1

    def test_rudolf_if_santa_has_no_carrots_then_win(self, dial1, rudolf, santa, game):
        # Given
        dial1.value = 0
        rudolf.carrot_in_hand = 1
        rudolf.num_carrots = 0
        santa.num_carrots = 0

        # When
        rudolf.tick(dial1)

        # Then
        assert (
            rudolf.carrot_in_hand, rudolf.num_carrots, santa.num_carrots, game.state
        ) == (
            0, 1, 0, GAME_STATE_WIN
        )

    def test_carrot_in_hand_is_shown(self, rudolf, dial1, lights):
        # Given
        dial1.value = 0.5
        rudolf.carrot_in_hand = 1
        rudolf.num_carrots = 0
        
        # When
        rudolf.tick(dial1)
        rudolf.show(lights)

        # Then
        lights.set_rgb.assert_called_with(23, *colours.ORANGE)


    def test_rudolf_owned_carrots_are_shown(self, rudolf, dial1, lights):
        # Given
        dial1.value = 0.5
        rudolf.carrot_in_hand = 0
        rudolf.num_carrots = 2

        # When
        rudolf.tick(dial1)
        rudolf.show(lights)
    
        # Then
        lights.set_rgb.assert_any_call(0, *colours.ORANGE)
        lights.set_rgb.assert_any_call(1, *colours.ORANGE)


