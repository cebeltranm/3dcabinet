import os
import board
import digitalio

os.chdir('/home/carlos/projects/3dcabinet/')

DISPLAY_CS_PIN = digitalio.DigitalInOut(board.CE0)
DISPLAY_DC_PIN = digitalio.DigitalInOut(board.D24)
DISPLAY_RESET_PIN = digitalio.DigitalInOut(board.D25)
DISPLAY_ROTATION = 0

DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 320

SENSOR1_CS = board.D27
SENSOR2_CS = board.D16

TOUCH_CS = digitalio.DigitalInOut(board.CE1)
TOUCH_EVENT = board.D26
# D12
LED_PIN = 12
LED_SEC1_SIZE = 20
LED_SEC2_SIZE = 15
LED_FILL_TIME = 1000 # ms

# LEDS_2_PIN = board.D12
# LEDS_2_SIZE = 80

TACH_SENSOR = 17
PWM_PIN = 13

# Colors
COLOR_BACKGROUND = (18, 18, 18)
COLOR_TEXT = (255, 255, 255)
COLOR_ACCENT = (0, 188, 212)

# FONT SIZES
FONT_SIZE_BIG = 70
FONT_SIZE_MEDIUM = 36
FONT_SIZE_SMALL = 10

ALIGN_LEFT = "left"
ALIGN_RIGHT = "right"
ALIGN_CENTER = "center"