import board
import digitalio

DISPLAY_CS_PIN = digitalio.DigitalInOut(board.CE0)
DISPLAY_DC_PIN = digitalio.DigitalInOut(board.D13)
DISPLAY_RESET_PIN = digitalio.DigitalInOut(board.D23)
DISPLAY_ROTATION = 90
