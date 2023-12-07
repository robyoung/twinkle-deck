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
    d1min, d1max = minmax(td.dial1.value, d1min, d1max)
    d2min, d2max = minmax(td.dial2.value, d2min, d2max)
    d3min, d3max = minmax(td.dial3.value, d3min, d3max)
    
    print(f"D1 {d1min}  {d1max}")
    print(f"D2 {d2min}  {d2max}")
    print(f"D3 {d3min}  {d3max}")

    time.sleep(1)
