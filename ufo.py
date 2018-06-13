#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

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
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def fireColor(intensity): #make a color palete going from red through yellow to white
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
    
def leg(strip, number, bottom, top, color): #set value for a range of pixels on a given leg
    for p in range(bottom, top):
        strip.setPixelColor(114-p+50*number, color)
        strip.setPixelColor(115+p+50*number, color)
        strip.setPixelColor(340+p+32*number, color)

def window(strip, number, color): #set pixels in a given window 
    for p in range(18):
        strip.setPixelColor(p+number*18, color)


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


def fireLegs(strip, wait_ms=10):
    for i in range(250):
        for p in range(25):
            legsAll(strip, p, p+1, fireColor(i*4-p*30))
        strip.show()
        time.sleep(wait_ms/1000.0)

def sparkle(strip, wait_ms = 10, iterations = 200):
    spark = [0]*924
    for i in range(iterations):
        if random.random() < 0.2:
            spark[random.randint(0,923)] = 255.0
        if random.random() < 0.2:
            spark[random.randint(0,923)] = 255.0
        spark[:] = [x*0.9 for x in spark]
        for p in range(924):
            strip.setPixelColor(p, Color(int(spark[p]), int(spark[p]), int(spark[p])))
        strip.show()
        time.sleep(wait_ms/1000.0)
  
def rotationMatrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])
                     
def fillUp(strip, color, ordering, wait_ms = 10):
    for h in range(int(min(ordering)),int(max(ordering)),int((max(ordering)-min(ordering)/100.0))):
        for p in range(924):
            if ordering[p] < h:
                strip.setPixelColor(p, color)
            else:
                strip.setPixelColor(p, 0)
        strip.show()
        time.sleep(wait_ms/1000.0)
        
def fillUpFire(strip, ordering, wait_ms=10):
    for h in range(int(min(ordering)),int(max(ordering)),int((max(ordering)-min(ordering)/100.0))):
        for p in range(924):
            strip.setPixelColor(p, fireColor((h-ordering[p])*1500/(max(ordering)-min(ordering))))
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
        
         #calculate pixel positions on startup to speed up program later
        X = [0]*924
        Y = [0]*924
        Z = [0]*924
        v = -1.10714871779  #tilt angle of the tilted great circles (pi/2-arctan(1/2))
        vz = -math.pi*2/5 #72 degrees rotation symmetry about z-axis
        
        z_matrix = rotationMatrix([0,0,1],vz)
        print(z_matrix)
        tilt_matrix = rotationMatrix([1,0,0], v) 
        print(v)
        print(tilt_matrix)
        
        for number in range(5): 
            
            for p in range(25): #legs
                X[114-p+50*number] = (2.75-0.07*p)*math.sin((0.5-number)*vz)-(0.008*p+0.1)*math.cos((0.5-number)*vz)
                Y[114-p+50*number] = (2.75-0.07*p)*math.cos((0.5-number)*vz)+(0.008*p+0.1)*math.sin((0.5-number)*vz)
                Z[114-p+50*number] = 0.07*p
                X[115+p+50*number] = (2.75-0.07*p)*math.sin((0.5-number)*vz)+(0.008*p+0.1)*math.cos((0.5-number)*vz)
                Y[115+p+50*number] = (2.75-0.07*p)*math.cos((0.5-number)*vz)-(0.008*p+0.1)*math.sin((0.5-number)*vz)
                Z[115+p+50*number] = 0.07*p
                X[340+p+32*number] = (2.65-0.08*p)*math.sin((0.5-number)*vz)
                Y[340+p+32*number] = (2.65-0.08*p)*math.cos((0.5-number)*vz)
                Z[340+p+32*number] = 0.06*p
                
            for p in range(7): #lower ring
                vector = [1.25*math.sin((p-3)*math.pi*2/78.5),1.25*math.cos((p-3)*math.pi*2/78.5),0]
                vector = np.dot(tilt_matrix, vector)
                for i in range(number):
                    vector = np.dot(z_matrix, vector)
                X[365+p+32*number] = vector[0]
                Y[365+p+32*number] = vector[1]
                Z[365+p+32*number] = vector[2] + 2.5
            
            for p in range(69): #great circles
                vector = [1.25*math.sin((p+5)*math.pi*2/78.5),1.25*math.cos((p+5)*math.pi*2/78.5),0]
                vector = np.dot(tilt_matrix, vector)
                for i in range(4-number):
                    vector = np.dot(z_matrix, vector)
                X[500+p+69*number] = vector[0]
                Y[500+p+69*number] = vector[1]
                Z[500+p+69*number] = vector[2] + 2.5 
        
            for p in range(18): #windows
                vector = [0.3*math.sin(p*math.pi*2/18),-0.3*math.cos(p*math.pi*2/18),1.25]
                vector = np.dot(tilt_matrix, vector)
                for i in range(number):
                    vector = np.dot(z_matrix, vector)
                X[p+18*number] = vector[0]
                Y[p+18*number] = vector[1]
                Z[p+18*number] = vector[2] + 2.5
               
        for p in range(79): #equator (only one of these)
            
            X[845+p] = 1.25*math.sin(math.pi*p/78.5*2)
            Y[845+p] = 1.25*math.cos(math.pi*p/78.5*2)
            Z[845+p] = 2.5
        
   #     with open('ufo.csv', 'wb') as csvfile:
   #         spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)    
   #         for p in range(924):
   #             print(X[p])
   #             print(Y[p])
   #             print(Z[p])
   #             spamwriter.writerow([X[p], Y[p], Z[p]])
                
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
            clear(strip)
            print('sparkle')
            sparkle(strip)
            print('Fill up')
            fillUp(strip, Color(255, 0, 0), X[:])
            fillUp(strip, Color(255, 0, 0), Y[:])
            fillUp(strip, Color(255, 0, 0), Z[:])
            print('Fire fill up')
            fillUpFire(strip, X[:])
            print('windowcycle blue')
            windowCycle(strip, Color(255, 0, 0))
           # print('windowcycly green')
           # windowCycle(strip, Color(0, 0, 255))
            print('windowcycle white')
            windowCycle(strip, Color(255, 255, 255))
            print('half window synchronous')
            halfWindowsSync(strip, Color(0, 255, 0))
          #  print('half window asynch')
          #  halfWindowsAsync(strip, Color(255, 255, 255))
            print('firelegs')
            fireLegs(strip)
           # print('theater chase rainbow')
           # theaterChaseRainbow(strip)
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

