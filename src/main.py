import adafruit_dht
import board
from constants import *
import adafruit_rgb_display.ili9341 as ili9341
import time
from modules.screen import Screen
from modules.number_section import NumberSection
from modules.light_section import LightSection
from modules.touch_listener import TouchListener

spi = board.SPI()
disp = ili9341.ILI9341(spi, rotation=DISPLAY_ROTATION, cs=DISPLAY_CS_PIN, dc=DISPLAY_DC_PIN, rst=DISPLAY_RESET_PIN)
loadingScreen = Screen('resources/loading.png')
loadingScreen.render(disp)

def touch_event(event, duration):
    print(event, duration)

touchListener = TouchListener(touch_event)

sensor1 = adafruit_dht.DHT22(SENSOR1_CS)
sensor2 = adafruit_dht.DHT22(SENSOR2_CS)

def get_sensor_value(sensor, value):
    def get_value():
        try:
            if value == 'temperature':
                return sensor.temperature
            elif value == 'humidity':
                return sensor.humidity
        except RuntimeError as error:
            print(error.args[0])
    return get_value

mainScreen = Screen('resources/main.jpg', [
    NumberSection(get_sensor_value(sensor1, 'temperature'), 25, 210, 80, 50, 40),
    NumberSection(get_sensor_value(sensor1, 'humidity'), 85, 210, 80, 50, 40),
    NumberSection(get_sensor_value(sensor2, 'temperature'), 25, 95, 80, 50, 40),
    NumberSection(get_sensor_value(sensor2, 'humidity'), 85, 95, 80, 50, 40),
    LightSection()
])

while True:
    touchListener.check_touch()
    mainScreen.render(disp)
    time.sleep(0.2)