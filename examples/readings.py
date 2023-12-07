"""Readings from the TwinkleDeck

This example tests out all the buttons and dials on the interface.
All values are printed to serial.
"""
import twinkledeck.hal as td
import time


def minmax(val, min, max):
    if val < min:
        min = val
    if val > max:
        max = val
    return min, max

d1min = d1max = td.dial1.value
d2min = d2max = td.dial2.value
d3min = d3max = td.dial3.value

while True:
    d1val = td.dial1.value
    d2val = td.dial2.value
    d3val = td.dial3.value
    d1min, d1max = minmax(d1val, d1min, d1max)
    d2min, d2max = minmax(d2val, d2min, d2max)
    d3min, d3max = minmax(d3val, d3min, d3max)
    
    print(f"D1 {d1val}  {d1min}  {d1max}")
    print(f"D2 {d2val}  {d2min}  {d2max}")
    print(f"D3 {d3val}  {d3min}  {d3max}")

    print(f"B1 {td.button1.read()}")
    print(f"B2 {td.button2.read()}")
    print(f"B3 {td.button3.read()}")

    time.sleep(1)
