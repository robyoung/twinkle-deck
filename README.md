# Twinkle Deck

Forget the Steam Deck, this Christmas's gaming sensetion is the Twinkle Deck!

## Hardware

The Twinkle Deck is based on a [Plasma 2040 LED strip driver](https://shop.pimoroni.com/products/plasma-2040).
Which is based on the popular [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)
microcontroller. The chip has been loaded with Pimoroni's [Pirate brand MicroPython](https://github.com/pimoroni/pimoroni-pico/releases)
along with some custom Twikle Deck libraries (described below).

It is connected to a whopping _50_ RGB LEDs and the control pad has three dials _and_ three buttons.

## Getting started

In order to connect to the Twinkle Deck you will need some software that can connect to it's serial interface.
The following examples will use `rshell` but you can also use the [Thonny IDE](https://thonny.org/) (recommmended by
the Raspberry Pi foundation and Pimoroni). You may also be able to get VSCode to talk to it but I have not tested this method.
Check section 4.2 of the [RP2040 datasheet](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf) for more
details.

### 1. Install python dependencies

In this repo create a virtualenv and install the local dependencies.

```
python -m venv venv
pip install -r requirements.txt
```

### 2. Plug in the Twinkle Deck

Plug a USB-C cable into the Twinkle Deck and into your computer.

### 3. Run the repl

Run the rshell repl against the rp2040 chip.

```
rshell repl
```

### 4. Write some example code

Test that everything is working by switching on an LED. The following code should
set the first LED in the strip to RED.

```python
import twinkledeck.hal as td

td.lights.set_rgb(0, 255, 0, 0)
```

To exit the repl press `CTRL+x`

### 5. Upload a program

If you want a program to run when the Twinkle Deck starts up you will need to upload it
to the device as a file called `main.py`. The following will upload the tester example.

```
rshell cp examples/tester.py /pyboard/main.py
```

In order to tell the device to run the code we need to restart it. This can be done by
power cycling (unplug and plug it back in again) or by 'soft rebooting'. To soft reboot
connect to the repl and and press `CTRL+d`.

## Libraries

### Hardware Abstraction Layer

This module provides the interface to the Twinkle Deck hardware. It provides three main
types of component; buttons, dials and lights.

A button can be pressed and have it's value read; `True` means it is pressed, `False` means it is not.

```python
import twinkledeck.hal as td

td.button1.read()
```

A dial can be rotated and have it's value read; it will be a `float` between `0` and `1` (approximately).

```python
import twinkledeck.hal as td

td.dial1.value
```

The lights can be individually set to an RGB or HSV value. The number of lights is in `twinkledeck.constants.NUM_LEDS`
(which is also imported in the HAL).

```python
import twinkledeck.hal as td

# set all LEDs red
for i in range(td.constants.NUM_LEDS):
    td.lights.set_hsv(i, 0, 1, 1)
    td.lights.set_rgb(i, 255, 0, 0)
```
