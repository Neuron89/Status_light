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