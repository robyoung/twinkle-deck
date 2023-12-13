"""Carrot snatch

You play as Rudolf the Red Nosed Reindeer. Santa has a box of juicy carrots but he has
said that they cannot be eaten until after the presents have been delivered.
You cannot wait!

Santa is at the far end of the string. He is a red light and a white light.
In front of Santa are 3 orange carrots.
You are Rudolf, a red dot at the other end of the string.
You must slowly up to the carrots and take one back to the start.
"""
import time

import twinkledeck.hal as td
from twinkledeck.games.carrot_snatch import Game


def main():
    game = Game(td.NUM_LEDS)

    while True:
        game.tick(td)
        time.sleep(1.0 / 60)


main()
