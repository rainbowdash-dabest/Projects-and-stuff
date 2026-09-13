### Macrokeyboard for iPad [Pi Pico H] (works smh)

# made this project because I needed to precisely scroll a Blender tutorial on YouTube on my ipad, 
# and getting a whole keyboard felt like too much. Compatible with most USB-C devices.

# execution-heirarchy__ to reboot ground pin_0 to enter safe_mode. If key press registered, LED will flash.
# You can modify hold_down repeat rate to spam faster / autoclick with repeat_rate_ms.
# Feel free to change to WSAD or numeric layouts, just need to modify the key_pins dict and match GPIOs.

# specifications and libs__ no need for wifi compatibility, all neccesary files appended already.

import time
import sys
from machine import Pin
from keyboard import Keyboard, Keycode

safe_switch = Pin(0, Pin.IN, Pin.PULL_UP)
if safe_switch.value() == 0:
    print("!!! SAFE_MODE DETECTED: Exiting.")
    sys.exit() # Terminate if pin 0 is grounded.

print("5-second safety buffer...")
time.sleep(5)

# init
kbd = Keyboard()

led = Pin(25, Pin.OUT)
led.value(1)

# macro-key layout
key_pins = {
    14: Keycode.SPACE,
    15: Keycode.UP_ARROW,
    16: Keycode.DOWN_ARROW,
    17: Keycode.LEFT_ARROW,
    18: Keycode.RIGHT_ARROW
}

hold_down_trigger = 2000  # 2.0 seconds before spamming the key when held down
repeat_rate_ms = 100      # 0.1 seconds (10Hz) aka. spam rate

# Configured to pull up. GND-ed when pressed.
# Structure: { btn_object: [keycode, is_pressed, press_time, last_repeat_time] }
buttons = {}
for pin_num, keycode in key_pins.items():
    btn = Pin(pin_num, Pin.IN, Pin.PULL_UP)
    buttons[btn] = [keycode, False, 0.0, 0.0]

print("Ready!")

while True:
    current_time = time.ticks_ms()
    any_button_pressed = False
    for btn, data in buttons.items():
        keycode, is_pressed, press_time, last_repeat_time = data
        
        if btn.value() == 0:  
            if not is_pressed:
                # Click_start: single trigger
                led.value(0) 
                kbd.press(keycode)
                # Save state and timestamp
                buttons[btn] = [keycode, True, current_time, current_time]
            else:
                # but i want to spam
                time_held = time.ticks_diff(current_time, press_time)
                if time_held >= hold_down_trigger:
                    time_since_repeat = time.ticks_diff(current_time, last_repeat_time)
                    # hold_down_trigger seconds passed
                    if time_since_repeat >= repeat_rate_ms:
                        kbd.release()
                        kbd.press(keycode)
                        buttons[btn][3] = current_time # Update last repeat timestamp
                
        # if released.
        else: 
            if is_pressed:
                kbd.release()
                led.value(1)  # Turn light back on when idle
                buttons[btn] = [keycode, False, 0.0, 0.0] # Reset dict
    
    time.sleep(0.01) # Short sleep to avoid button connection contact bounce

'''  
## gpio pin diagnostic
 
import time
from machine import Pin

led = Pin(25, Pin.OUT)
led.value(1) 

test_pin_0 = Pin(14, Pin.IN, Pin.PULL_UP)
test_pin_1 = Pin(15, Pin.IN, Pin.PULL_UP)

print("--- DIAGNOSTIC MODE ---")

while True:
    # Check if either pin drops down to ground level
    if test_pin_0.value() == 0:
        led.value(0)       
        print("-> GP14 Triggered (y)")       
        time.sleep(0.5)    
        led.value(1)       
        
    if test_pin_1.value() == 0:
        led.value(0)       
        print("-> GP15 Triggered (y)")       
        time.sleep(0.5)    
        led.value(1)       
        
    time.sleep(0.01) 
'''