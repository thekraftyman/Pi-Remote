import RPI.GPIO as GPIO
import time
import subprocess

# we will use the pin numbering to match the pins on the Pi, instead
#   of the GPIO pin outs

GPIO.setmode(GPIO.BOARD)

# Some globals
BUTTON_PIN = 5

# Use the same pin that is used for the reset button
GPIO.setup( BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP )

# pre-set state for comparison later
old_button_state = True

# loop forever, listening for the off command
while True:
    # grab current button state
    button_state = GPIO.input( BUTTON_PIN )

    # check to see if it has been pushed
    if button_state != old_button_state and button_state == FALSE:
        subprocess.call(
            "shutdown -h now",
            shell  = True,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        old_button_state = button_state # prevent second press during shutdown

    sleep( 0.1 )
