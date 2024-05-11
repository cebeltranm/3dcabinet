import board
from constants import *
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.rgb as rgb

selected_screen = None
selected_light = None
procesing = True
screens = {}

spi = board.SPI()
disp = ili9341.ILI9341(spi, rotation=DISPLAY_ROTATION, cs=DISPLAY_CS_PIN, dc=DISPLAY_DC_PIN, rst=DISPLAY_RESET_PIN)

disp.fill_rectangle(0,0,240,320, rgb.color565(0,255,0))
# disp.write(0x28)
disp.write(0x29)
