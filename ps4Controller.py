import sys
import os
import asyncio
from evdev import InputDevice, categorize, ecodes, AbsInfo
import RPi.GPIO as GPIO

libdir = '/home/pi/Desktop/e-Paper/RaspberryPi_JetsonNano/python/lib'
if os.path.exists(libdir):
    sys.path.append(libdir)
    
from waveshare_epd import epd2in13_V3
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

os.system("echo 'connect DC:AF:68:0D:91:DA' | bluetoothctl")


steering_pin = 12
throttle_pin = 16
extra_pin_1 = 20
extra_pin_2 = 21

GPIO.setup(steering_pin, GPIO.OUT)
GPIO.setup(throttle_pin, GPIO.OUT)
GPIO.setup(extra_pin_1, GPIO.OUT)
GPIO.setup(extra_pin_2, GPIO.OUT)

pwm_steering = GPIO.PWM(steering_pin, 100)
pwm_throttle = GPIO.PWM(throttle_pin, 100)

pwm_steering.start(0)
pwm_throttle.start(0)

epd = epd2in13_V3.EPD()
epd.init()
epd.Clear(0xFF)

font15 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
font24 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
    
image = Image.new('1', (epd.height, epd.width), 255)  
draw = ImageDraw.Draw(image)
    
epd.displayPartBaseImage(epd.getbuffer(image))
last_time = 0
text_to_display = "Starting... "

def map_value(x, in_min, in_max, out_min, out_max):
    return ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


async def update_display(text_to_display):
    draw.rectangle((120,80,220,105), fill=255)
    draw.text((5,5), text_to_display, font=font15, fill=0)
    epd.displayPartial(epd.getbuffer(image))
    time.sleep(1)
    
loop = asyncio.get_event_loop()

try:
    device = InputDevice('/dev/input/event3')

    def get_axis_value(i):
        try:
            return (device.absinfo(i).value - 128) / 128
        except Exception as e:
            print(f"Error getting axis value: {e}")
            return 0

    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            #print(key_event)
            if key_event.keystate == key_event.key_down:
                if key_event.keycode == ['BTN_A', 'BTN_GAMEPAD', 'BTN_SOUTH']:
                    print("X button")
                    text_to_display = text_to_display + "\nX button"
                    GPIO.output(extra_pin_1, GPIO.HIGH)
                elif key_event.keycode == ['BTN_B', 'BTN_EAST']:
                    GPIO.output(extra_pin_2, GPIO.HIGH)
                    print("O button")

        elif event.type == ecodes.EV_ABS:
            abs_event = categorize(event)
            #print(abs_event)
            L_Stick_X = get_axis_value(0) * 100
            R_Trigger = get_axis_value(5) * 100
            L_Trigger = get_axis_value(2) * 100
            
            throttle_value = ((R_Trigger - L_Trigger) / 2)
            
            mapped_steering = map_value(L_Stick_X, -100, 100, 0, 100)
            mapped_throttle = map_value(throttle_value, -100, 100, 0, 100)
            pwm_steering.ChangeDutyCycle(mapped_steering)
            pwm_throttle.ChangeDutyCycle(mapped_throttle)
            #print("joystick moved to: ", mapped_throttle)
            
    loop.run_until_complete(update_display(text_to_display))

except KeyboardInterrupt:
    pwm_steering.stop()
    pwm_throttle.stop()
    GPIO.cleanup()
    device.close()
except Exception as e:
    print(f"An error occurred: {e}")
