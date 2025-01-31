
# Goal

My Wife works as a Psych NP and meets with clients in her office. I have had the tendency of walking in and asking odd questions in weird accents. Everyone finds it funny but its very inappropriate so there had to be a way to alert everyone that she cant be disturbed. We got a nice little RGB lamp outside of her office that's key'd to a button through home assistant and it works perfectly. Only problem is she cant see what color it is so shell leave it on RED all day.

## Solution

I thought having a small cube of light on her desk that's the same as the lamp outside would be a perfect solution. I found nothing and anything that was even remotely close was very expensive and still very large. I figured it cant be that hard to make what i want. I got to jerry rigging and came up with an esp32 (what i had on hand) and a RGB led diode and a button. wrote a circuit python script that would use the exact same functions as the button in Home Assistant. 

# requirements 

- ESP32 Board
- Push Button connected to GPIO 0 (or any preferred GPIO)
- RGB LED connected to GPIOs 25, 26, and 27 (or any preferred GPIOs)
-  MicroPython Firmware Installed

# GPIO pinout

- Single Press - Blue LED (D4)
- Long Press (800ms+) - Green LED (D3)
- Double Tap (within 500ms) - Red LED (D2)
``` python
import board
import digitalio
import time

# Pin assignments (adjust as needed)
button_pin = board.D0  # Button connected to GPIO 0
red_pin = board.D2    # Red LED
green_pin = board.D3  # Green LED
blue_pin = board.D4   # Blue LED

# Setup LED pins as outputs
red = digitalio.DigitalInOut(red_pin)
red.direction = digitalio.Direction.OUTPUT

green = digitalio.DigitalInOut(green_pin)
green.direction = digitalio.Direction.OUTPUT

blue = digitalio.DigitalInOut(blue_pin)
blue.direction = digitalio.Direction.OUTPUT\
                 

# Setup button as input with pull-up resistor
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Variables for press tracking
press_time = None
release_time = None
click_count = 0
long_press_detected = False

def turn_off_leds():
    red.value = False
    green.value = False
    blue.value = False

def set_color(r, g, b):
    red.value = r
    green.value = g
    blue.value = b

def detect_button_press():
    global press_time, release_time, click_count, long_press_detected
    
    if not button.value:  # Button pressed
        press_time = time.monotonic()  # Record press time
        while not button.value:  # Wait for release
            if time.monotonic() - press_time >= 0.8:  # Long press threshold
                long_press_detected = True
                set_color(0, 0, 1)  # Blue LED for long press
                time.sleep(0.5)  # Avoid repeated detection
                return
    
        release_time = time.monotonic()
        press_duration = release_time - press_time

        if press_duration < 0.8:
            click_count += 1
            check_double_tap()

def check_double_tap():
    global click_count, long_press_detected
    start_time = time.monotonic()
    
    while time.monotonic() - start_time < 0.25:  # Wait up to 250ms for a second tap
        if not button.value:  # If pressed again within this time
            while not button.value:  # Wait for release
                pass
            click_count += 1
            break
    
    if long_press_detected:
        long_press_detected = False
        click_count = 0
        return

    if click_count == 1:
        set_color(0, 1, 0)  # Green LED for single press
    elif click_count == 2:
        set_color(1, 0, 0)  # Red LED for double tap
    
    click_count = 0  # Reset tap count

# Main loop
turn_off_leds()
while True:
    detect_button_press()
    time.sleep(0.01)  # Small delay to avoid excessive CPU usage



```


After I breadboarded the controller and LED, i started to think about form factor. At fist i thought i would just use a button and have it wedged in-between the HA button and the ESP32, then i figured "the HA button as a button in it, why not just steal that signal". After soldering a line and checking polarity, i figured id go one step farther and also just steal the battery (at this point i wondered if i should actually just make the ESP32 board itself be the button for both as it could support Matter and Zigbee. project for another day), this......worked......but not really. 
` In this image, I wired the postive and negative incorrect`
<p align=“center”>
<img src=assets/CircutBoard.jpeg width=300>
</p>
the 3V the battery was outputting wasn't enough to support everything. the ESP32 would work but couldn't pass enough to actually light the LED like i wanted. 

<p align=“center”>
<img src=assets/pinout.jpeg width=300>
</p>

So i attached the 3v, GND, and D0 to the board of the HA button. verified everything worked, stuck it back together and now i have a functional button that also shows the color of the lamp at her desk. Its not perfect but for spending about 2-3 hours between soldering, programming, and testing, id consider it a success! I will (maybe/hopefully) return to this to make a more professional version with a light diffuser and just have the entire object 
<p align=“center”>
<img src=assets/Button1.jpeg width=300>
  <img src=assets/Button2.jpeg width=300>
  <img src=assets/Button3.jpeg width=300>
</p>

<p align=“center”>
<img src=assets/Blue.jpeg width=300>
  <img src=assets/Red.jpeg width=300>
  <img src=assets/Green.jpeg width=300>
</p>

