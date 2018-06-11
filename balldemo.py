#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 924      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) &  255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(64):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 256))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def windowCycle(strip, color, wait_ms=200, iterations=5):
    """Light each window in sequence"""
    for i in range(iterations):
        for j in range(5):
            for p in range(90):
                if p//18 == j:
                    strip.setPixelColor(p, color)
                else:
                    strip.setPixelColor(p, 0)
            strip.show()
            time.sleep(wait_ms/1000.0)

def halfWindowsSync(strip, color, wait_ms=50, iterations=10):
    """Light half of each window, turning around synchronously"""
    for i in range(iterations):
        for j in range(18):
            for p in range(90):
                if ((p+j) % 18) > 9:
                    strip.setPixelColor(p, color)
                else:
                    strip.setPixelColor(p, 0)
            strip.show()
            time.sleep(wait_ms/1000.0)

def halfWindowsAsync(strip, color, wait_ms=10, iterations=10):
    """Light half of each window, turning around in a wave motion"""
    for i in range(18*iterations):
        for j in range(5):
            for p in range(18):
                if (p * 5 + i + j * 18) % 90 > 45:
                    strip.setPixelColor(p+18*j, color)
                else:
                    strip.setPixelColor(p+18*j, 0)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbowDouble(strip, wait_ms=50):
    """Double pixel size"""
    for j in range(64):
        for q in range(6):
            for i in range(0, strip.numPixels(), 6):
                strip.setPixelColor(i+q, wheel((i-j*4) % 256))
                strip.setPixelColor(i+q+1, wheel((i-j*4+1) % 256))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 6):
                strip.setPixelColor(i+q, 0)
                strip.setPixelColor(i+q+1, 0)

def window(strip, number, color):
    for p in range(18):
        strip.setPixelColor(p+18*number, color)

def leg(strip, number, bottom, top, color):
    for p in range(bottom, top):
        strip.setPixelColor(114-p+50*number, color)
        strip.setPixelColor(115+p+50*number, color)
        strip.setPixelColor(340+p+32*number, color)

def legsAll(strip, bottom, top, color):
    for number in range(5):
        leg(strip, number, bottom, top, color)

def clear(strip):
    for p in range(strip.numPixels()):
        strip.setPixelColor(p, 0)
    strip.show()

def rotate(strip, color, wait_ms=50, iterations=50):
    clear(strip)
    for i in range(iterations):
        leg(strip, i%5, 0, 25, color)
        leg(strip, (i-1)%5, 0, 25, 0)
        strip.show()
        time.sleep(wait_ms/1000.0)
        window(strip, i%5, color)
        window(strip, (i-1)%5, 0)
        strip.show()
        time.sleep(wait_ms/1000.0)

def fireColor(intensity):
    i = int(intensity)
    if i < 0:
        return Color(0, 0, 0)
    elif i < 256:
        return Color(0, i, 0)
    elif i < 510:
        return Color(0, 255, i-255)
    elif i < 765:
        return Color(i, 255, 255)
    else:
        return Color(255, 255, 255)

def fireLegs(strip, wait_ms=10):
    for i in range(250):
        for p in range(25):
            legsAll(strip, p, p+1, fireColor(i*4-p*30))
        strip.show()
        time.sleep(wait_ms/1000.0)


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
        clear(strip)
        time.sleep(30)
        while True:

          #  print ('Color wipe animations.')
          #  colorWipe(strip, Color(255, 0, 0))  # Blue wipe
          #  colorWipe(strip, Color(0, 255, 0))  # red wipe
          #  colorWipe(strip, Color(0, 0, 255))  # Green wipe
          #  print ('Theater chase animations.')
          #  theaterChase(strip, Color(127, 127, 127))  # White theater chase
          #  theaterChase(strip, Color(127,   0,   0))  # Red theater chase
          #  theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
          #  print ('Rainbow animations.')
          #  rainbow(strip)
          #  rainbowCycle(strip)
          #  theaterChaseRainbow(strip)
            print('windowcycle blue')
            windowCycle(strip, Color(255, 0, 0))
            print('windowcycly green')
            windowCycle(strip, Color(0, 0, 255))
            print('windowcycle white')
            windowCycle(strip, Color(255, 255, 255))
            print('half window synchronous')
            halfWindowsSync(strip, Color(0, 255, 0))
            print('half window asynch')
            halfWindowsAsync(strip, Color(255, 255, 255))
            print('firelegs')
            fireLegs(strip)
            print('theater chase rainbow')
            theaterChaseRainbow(strip)
            print('rainbow')
            rainbow(strip)
            print('theaterchase rainbow doube')
            theaterChaseRainbowDouble(strip)
            clear(strip)
            print('rotate')
            rotate(strip, Color(255, 255, 0))
            print('firelegs fast')
            fireLegs(strip, 0)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
