"""Carrot snatch library code"""
from twinkledeck.pulse import RegularPulser, ErraticPulser
from twinkledeck import colours

try:
    from shims import time
except ImportError:
    import time

GAME_STATE_PLAY = 0
GAME_STATE_WIN = 1
GAME_STATE_LOSE = 2


class Game:
    def __init__(self, num_leds, frame_rate = 60):
        self.state = GAME_STATE_PLAY
        self.state_prev = None
        self.num_leds = num_leds
        self.santa = Santa(self)
        self.rudolf = Rudolf(self)
        self.frame_rate = frame_rate

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

        self.santa.show(lights)
        self.rudolf.show(lights)

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
        self.num_carrots = 3
        self.set_awake()

    def set_awake(self):
        self.state = SANTA_STATE_AWAKE
        self.pulser = RegularPulser(min_value=0.3, duration=1000)
        self.last_state_change = time.ticks_ms()

    def set_alert(self):
        self.state = SANTA_STATE_ALERT
        self.pulser = ErraticPulser(min_value=0.3, max_duration=1000)
        self.last_state_change = time.ticks_ms()

    def set_sleep(self):
        self.state = SANTA_STATE_SLEEP
        self.pulser = RegularPulser(min_value=0.1, max_value=0.6, duration=3000)
        self.last_state_change = time.ticks_ms()

    def tick(self):
        now = time.ticks_ms()
        ticks_diff = time.ticks_diff(now, self.last_state_change)
        if ticks_diff > 1000:
            if self.game.rudolf.is_noisy:
                if self.state == SANTA_STATE_SLEEP:
                    self.set_awake()
                elif self.state == SANTA_STATE_AWAKE:
                    self.set_alert()
                else:
                    self.game.state = GAME_STATE_LOSE
            elif self.game.rudolf.is_quiet and ticks_diff > 2000:
                if self.state == SANTA_STATE_ALERT:
                    self.set_awake()
                elif self.state == SANTA_STATE_AWAKE:
                    self.set_sleep()

    def show(self, lights):
        value = self.pulser.value()
        # show santa
        lights.set_hsv(47, 0, 1, value)  # santa
        lights.set_hsv(48, 0, 1, value)  # santa
        lights.set_hsv(49, 0, 0, 0.5)  # hat
        # show santa's carrots
        for i in range(self.num_carrots):
            lights.set_rgb(46 - i, *colours.ORANGE)


class Rudolf:
    size = 2

    def __init__(self, game, speed_reduction=0.9):
        self.game = game
        self.position = 0
        self.speed = 0
        self.speed_reduction = speed_reduction
        self.num_carrots = 0
        self.carrot_in_hand = 0

    @property
    def is_close(self):
        return self.position >= 35

    @property
    def is_fast(self):
        return self.speed >= 2

    @property
    def is_noisy(self):
        return self.is_close and self.is_fast

    @property
    def is_far(self):
        return self.position <= 15

    @property
    def is_slow(self):
        return self.speed <= 0.1

    @property
    def is_quiet(self):
        return self.is_far and self.is_slow

    def tick(self, dial1):
        new_position = dial1.value
        speed = abs(new_position - self.position)
        self.speed = speed + self.speed * self.speed_reduction
        self.position = new_position

        if self.carrot_in_hand == 0 and self.position > 0.9:
            self.carrot_in_hand = 1
            self.game.santa.num_carrots -= 1

        if self.carrot_in_hand == 1 and self.position < 0.1:
            self.carrot_in_hand = 0
            self.num_carrots += 1
            if self.game.santa.num_carrots == 0:
                self.game.state = GAME_STATE_WIN

    @property
    def _max_position(self):
        return self.game.num_leds - self.game.santa.size - self.size - self.game.santa.num_carrots

    def show(self, lights):
        position = int(self.position * self._max_position)
        lights.set_hsv(position, 0, 1, 0.5)
        lights.set_hsv(position + 1, 0, 1, 0.5)

        for i in range(self.num_carrots):
            lights.set_rgb(i, *colours.ORANGE)
        
        if self.carrot_in_hand:
            lights.set_rgb(position + 2, *colours.ORANGE)
