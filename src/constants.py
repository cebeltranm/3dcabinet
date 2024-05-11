import board
import digitalio

DISPLAY_CS_PIN = digitalio.DigitalInOut(board.CE0)
DISPLAY_DC_PIN = digitalio.DigitalInOut(board.D6)
DISPLAY_RESET_PIN = digitalio.DigitalInOut(board.D23)
DISPLAY_ROTATION = 90

SENSOR1_CS = board.D5
SENSOR2_CS = board.D16

TOUCH_CS = digitalio.DigitalInOut(board.CE1)
TOUCH_EVENT = board.D26

LEDS1_PIN = board.D18
LEDS1_SIZE = 20

TACH_SENSOR = 4
PWM_PIN = 13
