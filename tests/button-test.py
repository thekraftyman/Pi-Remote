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
    button_pin = GP14
    button = Button( button_pin )

    while True:
        if button:
            print("Button was pressed!")
        sleep(0.1)

if __name__ == '__main__':
    main()
