import board
import digitalio
from time import sleep

class Button:
    ''' generic pushbutton '''

    def __init__( self, pin ):
        self.button_pin = pin
        self.button = digitalio.DigitalInOut( self.button_pin )
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.DOWN

    @property
    def val( self ):
        return self.button.value

    def __bool__( self ):
        return self.button.value

def main():
    # button
    button_pin = board.GP17
    button = Button( button_pin )
    
    # indicator led
    led = digitalio.DigitalInOut( board.GP16 )
    led.direction = digitalio.Direction.OUTPUT
    led.value = False

    while True:
        if button:
            print("Button was pressed!")
            if led.value == False:
                led.value = True
            else:
                led.value = False
        sleep(0.1)

if __name__ == '__main__':
    main()
