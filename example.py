import twinkledeck as td
import time

while True:
    print(f"Knob1: {td.knob1.value}, Knob2: {td.knob2.value}, Knob3: {td.knob3.value}")
    print(
        f"B1: {td.button1.is_pressed}, B2: {td.button2.is_pressed}, B3: {td.button3.is_pressed}"
    )
    time.sleep(0.3)
