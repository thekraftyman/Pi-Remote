import pulseio
import board
import adafruit_irremote
import digitalio

# define our remote codes
remote_codes = {
    'power_67': [604, 540, 594, 542, 591, 543, 591, 541, 593, 541, 567, 541, 593, 541, 581, 542, 592, 1637, 605, 1637, 605, 1637, 606, 1603, 585, 1598, 604, 1638, 606, 1637, 605, 1601, 604, 1592, 606, 538, 595, 1637, 606, 521, 597, 541, 593, 541, 592, 1637, 605, 541, 594, 518, 589, 1617, 606, 539, 594, 1637, 605, 1637, 597, 1636, 605, 539, 594, 1637, 605, 2218, 605],
    'power_65': [605, 531, 602, 534, 599, 535, 599, 536, 597, 534, 599, 536, 597, 537, 598, 529, 600, 1637, 603, 1639, 606, 1636, 605, 1523, 604, 1638, 605, 1637, 590, 1637, 604, 1638, 605, 1637, 605, 533, 603, 1635, 604, 533, 601, 538, 568, 534, 602, 1610, 604, 536, 596, 537, 600, 1637, 604, 532, 601, 1639, 604, 1638, 605, 1557, 604, 532, 602, 1637, 603],
}

def main():
    # init the ir receiver and decoder
    pulsein = pulseio.PulseIn(board.GP14, maxlen=200, idle_state=True)
    pulsein.clear()
    pulsein.resume()
    decoder = adafruit_irremote.GenericDecode()
    
    # specify indicator led
    led = digitalio.DigitalInOut( board.GP16 )
    led.direction = digitalio.Direction.OUTPUT
    led.value = False

    # loop forever and decode stuff
    while True:
        pulses = decoder.read_pulses(pulsein) # get the pulses from the remote
        if len(pulses) == 0: # skip if no pulses
            continue
        
        if is_power_signal( pulses ):
            print( "Heard a power signal" )
            if led.value == False:
                led.value = True
            else:
                led.value = False

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

# run the program on start
if __name__ == '__main__':
    main()