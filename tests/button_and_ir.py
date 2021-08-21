import pulseio
import board
import adafruit_irremote
import digitalio
from time import sleep

# define our remote codes
remote_codes = {
    'power_67': [604, 540, 594, 542, 591, 543, 591, 541, 593, 541, 567, 541, 593, 541, 581, 542, 592, 1637, 605, 1637, 605, 1637, 606, 1603, 585, 1598, 604, 1638, 606, 1637, 605, 1601, 604, 1592, 606, 538, 595, 1637, 606, 521, 597, 541, 593, 541, 592, 1637, 605, 541, 594, 518, 589, 1617, 606, 539, 594, 1637, 605, 1637, 597, 1636, 605, 539, 594, 1637, 605, 2218, 605],
    'power_65': [605, 531, 602, 534, 599, 535, 599, 536, 597, 534, 599, 536, 597, 537, 598, 529, 600, 1637, 603, 1639, 606, 1636, 605, 1523, 604, 1638, 605, 1637, 590, 1637, 604, 1638, 605, 1637, 605, 533, 603, 1635, 604, 533, 601, 538, 568, 534, 602, 1610, 604, 536, 596, 537, 600, 1637, 604, 532, 601, 1639, 604, 1638, 605, 1557, 604, 532, 602, 1637, 603],
}

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
    
class LED:
    '''generic led'''
    
    def __init__( self, pin ):
        self.led_pin = pin
        self.led = digitalio.DigitalInOut( self.led_pin )
        self.led.direction = digitalio.Direction.OUTPUT
        self.led.value = False
        self.is_on = False
        
    def on( self ):
        ''' turn the led on '''
        if not self.is_on:
            self.led.value = True
            self.is_on = True
            
            
    def off( self ):
        ''' turn off the led '''
        if self.is_on:
            self.led.value = False
            self.is_on = False
    
    def cycle( self ):
        ''' turns it on if its off, turns it off if it is on '''
        if self.is_on:
            self.off()
        else:
            self.on()

class IR_Receiver:
    ''' generic ir receiver class'''
    
    def __init__( self, pin , maxlen=200, idle_state=True):
        self.pin = pin
        self.pulsein = pulseio.PulseIn( self.pin, maxlen=maxlen, idle_state=idle_state )
        self.pulsein.clear()
        self.pulsein.resume()
        self.decoder = adafruit_irremote.GenericDecode()
    
    def get_pulses( self ):
        ''' returns the pulses '''
        return self.decoder.read_pulses( self.pulsein )

def is_same_signal( pulse1, pulse2, fuzzyness=0.2 ):
    # compares 2 signals with a given margin of error (fuzzyness)
    if len( pulse1 ) != len( pulse2 ):
        return False
    for i in range( len( pulse1 ) ):
        threshold = int( pulse2[ i ] * fuzzyness )
        if abs( pulse1[ i ] - pulse2[ i ] ) > threshold:
            return False
    return True

def is_power_signal( pulse ):
    # compares a pulse to the power_67 and power_65 commands, returns true if pulse is a power signal
    for power_signal in [ 'power_67', 'power_65' ]:
        if is_same_signal( pulse, remote_codes[ power_signal ], 0.4 ):
            return True
    return False

def average_pulse( pulse_list ):
    # takes a list of pulses, which are all of same length, and returns the average of the lists (in integers)
    avg_pulse = []
    n_pulses = len(pulse_list[0])
    
    for i in range(n_pulses):
        avg_pulse.append(int(sum([ pulse[i] for pulse in pulse_list]) / len(pulse_list)))
    
    return avg_pulse

def main():
    # button
    button_pin = board.GP17
    button = Button( button_pin )
    
    # led
    led_pin = board.GP16
    led = LED( led_pin )
    
    # ir_receiver
    ir_receiver_pin = board.GP14
    ir_receiver = IR_Receiver( ir_receiver_pin )
    
    # Loop forever
    while True:
        pulses = ir_receiver.get_pulses() # get the pulses from the remote
        
        if len(pulses) != 0: # skip if no pulses, but we'll check the button
            if is_power_signal( pulses ):
                print( "Heard an ir power signal" )
                led.cycle()
        
        if button.val:
            print("Pressed the button")
            led.cycle()
            sleep( 0.5 )
    
if __name__ == '__main__':
    main()