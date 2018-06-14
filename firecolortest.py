import time
from neopixel import *
import argparse
import random
import math
import numpy as np
# import csv

# LED strip configuration:
LED_COUNT      = 924      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def fireColor(intensity, debug=0): #make a color palete going from red through yellow to white
    i = int(intensity)
    if i < 0:
        return Color(0,0,0)
    elif i < 255:
        return Color(0, i, 0)
    elif i < 510:
        return Color(0, 255, i-255)
    elif i < 765:
        return Color(i-510, 255, 255)
    else:
        return Color(255, 255, 255)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        
      
        while True:
            
            for i in range(750):
                for p in range(strip.numPixels()):
                    strip.setPixelColor(p, fireColor(i))
                time.sleep(0.01)
                strip.show()



    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
    