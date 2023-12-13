"""Carrot snatch library code"""
from twinkledeck.pulse import RegularPulser, ErraticPulser
from twinkledeck import colours

GAME_STATE_PLAY = 0
GAME_STATE_WIN = 1
GAME_STATE_LOSE = 2


class Game:
    def __init__(self, num_leds):
        self.state = GAME_STATE_PLAY
        self.state_prev = None
        self.num_leds = num_leds
        self.santa = Santa(self)
        self.rudolf = Rudolf(self)
        self.carrots = [Carrot(num_leds - self.santa.size - (i + 1)) for i in range(3)]

    def tick(self, td):
        if self.state == GAME_STATE_PLAY:
            self.tick_play(td.lights, td.dial1)

        if self.state != GAME_STATE_PLAY:
            self.tick_outcome(td.lights, td.button1)

        self.state_prev = self.state

    def tick_play(self, lights, dial1):
        self.rudolf.tick(dial1)
        self.santa.tick()

        if self.state != GAME_STATE_PLAY:
            # fall back to displaying outcome
            return

    def tick_outcome(self, lights, button1):
        if self.state != self.state_prev:
            colour = (
                colours.GREEN if self.state == GAME_STATE_WIN else colours.BRIGHT_RED
            )

            for i in range(self.num_leds):
                lights.set_rgb(i, *colour)

        if button1.read():
            self.state = GAME_STATE_PLAY


SANTA_STATE_ALERT = 0
SANTA_STATE_AWAKE = 1
SANTA_STATE_SLEEP = 2


class Santa:
    size = 3

    def __init__(self, game):
        self.game = game
        self.set_awake()

    def set_awake(self):
        self.state = SANTA_STATE_AWAKE
        self.pulser = RegularPulser(min_value=0.3, duration=1000)

    def set_alert(self):
        self.state = SANTA_STATE_ALERT
        self.pulser = ErraticPulser(min_value=0.3, max_duration=1000)

    def set_sleep(self):
        self.state = SANTA_STATE_SLEEP
        self.pulser = RegularPulser(min_value=0.1, max_value=0.6, duration=3000)

    def tick(self):
        ...

    def show(self, lights):
        value = self.pulser.value()
        lights.set_hsv(47, 0, 1, value)  # santa
        lights.set_hsv(48, 0, 1, value)  # santa
        lights.set_hsv(49, 0, 0, 0.5)  # hat


class Carrot:
    def __init__(self, position):
        self.position = position

    def show(self, lights):
        lights.set_hsv(self.position)


class Rudolf:
    position = 0
    speed = 0

    def __init__(self, game):
        self.game = game
        self.position = 0
        self.speed = 0

    def tick(self, dial1):
        ...

    def show(self, lights):
        position = int(self.position * (td.NUM_LEDS - 3))
