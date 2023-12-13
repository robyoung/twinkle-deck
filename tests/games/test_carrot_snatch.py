import pytest
from unittest import mock
from twinkledeck import colours
from twinkledeck.games.carrot_snatch import (
    GAME_STATE_LOSE,
    GAME_STATE_PLAY,
    GAME_STATE_WIN,
    SANTA_STATE_ALERT,
    Game,
    Santa,
    Rudolf,
)


@pytest.fixture
def td():
    return mock.Mock()


@pytest.fixture
def dial1(td):
    return td.dial1


@pytest.fixture
def game():
    return Game(50)


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
        return Santa(game)

    def test_set_state(self, santa):
        santa.set_alert()
        assert santa.state == SANTA_STATE_ALERT


class TestRudolf:
    @pytest.fixture
    def rudolf(self, game):
        return Rudolf(game)

    def test_rudolf_default_speed(self, rudolf):
        assert rudolf.speed == 0

    def test_calculate_rudolf_speed(self, rudolf, dial1):
        # TODO @robyoung calculate speed in terms of ticks
        # TODO @robyoung calculate a very slow ewma
        dial1.value = 1
        rudolf.tick(dial1)
