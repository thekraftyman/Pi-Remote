# Pi Remote

The Raspberry Pi is a great tool for many projects, but one of its major problems (IMO) is the fact that it doesn't have a simple power button to put it into a low-energy state. This repo attempts to address that problem by creating an on/off switch that can be activated via a button or remote, using the Raspberry Pi Pico as an external controller. This interfaces with the pi's GPIO pins to run the power-up/power-down scripts.

## Requirements

- python3
- python3-pip
- gcc

## Raspberry Pi 3/4 Installation

1. Run the `pi-scripts/install.sh` script to install on the raspberry pi

## Raspberry Pi Pico Installation

1. Install the latest circuitpython [.UF2 file from Adafruit](https://circuitpython.org/board/raspberry_pi_pico/).
2. Wire up your pico as shown.
3. Upload the contents of pico-reciever to the board.
