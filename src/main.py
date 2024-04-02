import adafruit_dht
import board
from constants import *
import adafruit_rgb_display.ili9341 as ili9341
from modules.loading_screan import LoadingScreen
from modules.main_screan import MainScreen
import time

spi = board.SPI()
disp = ili9341.ILI9341(spi, rotation=DISPLAY_ROTATION, cs=DISPLAY_CS_PIN, dc=DISPLAY_DC_PIN, rst=DISPLAY_RESET_PIN)
loadingScreen = LoadingScreen()
loadingScreen.render(disp)

sensor1 = adafruit_dht.DHT22(board.D5)

mainScreen = MainScreen(sensor1)

while True:
    mainScreen.render(disp)
    time.sleep(1)