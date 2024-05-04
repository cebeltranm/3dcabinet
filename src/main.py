import keyboard
import time
import threading
import adafruit_dht
import board
from constants import *
import adafruit_rgb_display.ili9341 as ili9341
from modules.screens import Screen, MainScreen
from modules.number_section import NumberSection
from modules.light_section import LightSection
from modules.touch_listener import TouchListener
from modules.color_picker_section import ColorPickerSection
from modules.button_section import ButtonSection
from modules.render import RenderedComponent

selected_screen = None
selected_light = None
procesing = True
screens = {}

spi = board.SPI()
disp = ili9341.ILI9341(spi, rotation=DISPLAY_ROTATION, cs=DISPLAY_CS_PIN, dc=DISPLAY_DC_PIN, rst=DISPLAY_RESET_PIN)

# def touch_event(event, duration, x = None, y = None):
#     global selected_screen
#     if selected_screen != None:
#         selected_screen.touch_event(event, duration, x, y)

# def select_color(color):
#     global selected_light
#     if selected_light != None:
#         selected_light.set_color(color)

# def close_screen():
#     global selected_screen
#     global screens
#     selected_screen = screens['main']
#     selected_screen.clear_state()

# def select_color_screen(light):
#     global selected_light
#     global selected_screen
#     global screens

#     selected_light = light
#     selected_screen = screens['color']
#     selected_screen.clear_state()

# touchListener = TouchListener(spi, touch_event)

loadingScreen = Screen('resources/loading.png', (0,0,0))
loadingScreen.render(disp)


# sensor1 = adafruit_dht.DHT22(SENSOR1_CS)
# sensor2 = adafruit_dht.DHT22(SENSOR2_CS)

# def get_sensor_value(sensor, value):
#     try:
#         if value == 'temperature':
#             return sensor.temperature
#         elif value == 'humidity':
#             return sensor.humidity
#     except RuntimeError as error:
#         print(error.args[0])

# # main screeen
temp1 = NumberSection( 25, 210, 80, 50, 40)
# hum1 = NumberSection( 85, 210, 80, 50, 40)
# temp2 = NumberSection( 25, 95, 80, 50, 40)
# hum2 = NumberSection( 85, 95, 80, 50, 40)
# light1 = LightSection(160, 230, select_color_screen)

screens['main'] = MainScreen( [
    temp1,
    # hum1,
    # temp2,
    # hum2,
    # light1
])

selected_screen = screens['main']
# selected_light = light1

# # Color screen
# colorSection1 = ColorPickerSection( select_color, 0,0 )
# closeButton = ButtonSection( 'resources/close.jpg', 1, 280, close_screen )

# screens['color'] = Screen(None, (10, 10, 60), [
#     colorSection1,
#     closeButton
# ])


# def sensors():
#     global procesing
#     while procesing:
#         temp1.value = get_sensor_value(sensor1, 'temperature')
#         temp2.value = get_sensor_value(sensor2, 'temperature')
#         hum1.value = get_sensor_value(sensor1, 'humidity')
#         hum2.value = get_sensor_value(sensor2, 'humidity')
#         time.sleep(0.2)

# def touch():
#     global procesing
#     while procesing:
#         touchListener.check_touch()
#         time.sleep(0.1)

def render():
    global selected_screen
    global procesing
    while procesing:
        selected_screen.render(disp)
        time.sleep(0.05)

# thread_touch = threading.Thread(target=touch)
thread_render = threading.Thread(target=render)
# thread_sensors = threading.Thread(target=sensors)

# thread_touch.start()
thread_render.start()
# thread_sensors.start()

try:
    keyboard.wait('enter') 
except KeyboardInterrupt:
    pass

procesing = False
