import keyboard
import time
import threading
import adafruit_rgb_display.ili9341 as ili9341
import board
import neopixel
import RPi.GPIO as GPIO
from constants import *
from modules.screens import LoadingScreen, MainScreen, ColorPickerScreen
from modules.sensors import DHT22, PWMSensor
from modules.touch_listener import TouchListener
from modules.render import RenderedComponent
from modules.bus_events import BusEvents, BusEventLlistener

class Main(BusEventLlistener):
    selected_screen = None
    selected_section = None
    procesing = True
    screens = {}

    spi = board.SPI()
    disp = ili9341.ILI9341(spi, rotation=DISPLAY_ROTATION, cs=DISPLAY_CS_PIN, dc=DISPLAY_DC_PIN, rst=DISPLAY_RESET_PIN)

    def __init__(self):
        self.selected_screen = LoadingScreen()
        threading.Thread(target=self._render_thread).start()

        self.selected_screen.step = 1
        self.pixels1 = neopixel.NeoPixel(LEDS1_PIN, LEDS1_SIZE, pixel_order=neopixel.GRB, brightness=0)

        self.selected_screen.step = 2
        self.sensor1 = DHT22(SENSOR1_CS)
        self.sensor2 = DHT22(SENSOR2_CS)
        self.pwmsensor = PWMSensor(PWM_PIN, TACH_SENSOR)

        self.selected_screen.step = 3
        bus_events = BusEvents()
        bus_events.set_listener(self)

        self.selected_screen.step = 4
        self.screens['main'] = MainScreen(self.pixels1, self.pwmsensor)

        self.selected_screen.step = 5
        threading.Thread(target=self._sensors_thread).start()

        self.selected_screen.step = 6
        self.screens['color_picker'] = ColorPickerScreen()

        self.selected_screen.step = 9
        self.touchListener = TouchListener(self.spi, self._touch_event)
        threading.Thread(target=self._touch_thread).start()

        self.selected_screen.step = 10
        self.select_screen('main')

    def select_screen(self, screen, section = None):
        self.screens[screen].clear_state()
        self.selected_screen = self.screens[screen]
        self.selected_section = section

    def select_color(self, color):
        if self.selected_section and hasattr(self.selected_section, 'set_color'):
            self.selected_section.set_color(color)

    def _render_thread(self):
        while self.procesing:
            self.selected_screen.render(self.disp)
            time.sleep(0.05)

    def _sensors_thread(self):
        while self.procesing:
            if self.selected_screen == self.screens['main']:
                try:
                    self.selected_screen.setSensorValues([
                        self.sensor1.load_value(), 
                        self.sensor2.load_value(),
                        self.pwmsensor.load_value(),
                    ])
                except:
                    pass
            time.sleep(1)

    def _touch_thread(self):
        while self.procesing:
            self.touchListener.check_touch()
            time.sleep(0.1)

    def _touch_event(self, event, duration, x = None, y = None):
        if self.selected_screen != None:
            self.selected_screen.touch_event(event, duration, x, y)


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

# loadingScreen = Screen('resources/loading.png', (0,0,0))
# loadingScreen.render(disp)


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
# temp1 = NumberSection( 25, 210, 80, 50, 40)
# hum1 = NumberSection( 85, 210, 80, 50, 40)
# temp2 = NumberSection( 25, 95, 80, 50, 40)
# hum2 = NumberSection( 85, 95, 80, 50, 40)
# light1 = LightSection(160, 230, select_color_screen)

# screens['main'] = MainScreen( [
#     temp1,
    # hum1,
    # temp2,
    # hum2,
    # light1
# ])

# selected_screen = screens['main']
# selected_light = light1
# temp1.value = 10

# # Color screen
# colorSection1 = ColorPickerSection( select_color, 0,0 )
# closeButton = ButtonSection( 'resources/close.jpg', 1, 280, close_screen )

# screens['color'] = Screen(None, (10, 10, 60), [
#     colorSection1,
#     closeButton
# ])





# def render():
#     global selected_screen
#     global procesing
#     while procesing:
#         selected_screen.render(disp)
#         time.sleep(0.05)

# thread_touch = threading.Thread(target=touch)
# thread_render = threading.Thread(target=render)
# thread_sensors = threading.Thread(target=sensors)

# thread_touch.start()
# thread_render.start()
# thread_sensors.start()

main = Main()

try:
    keyboard.wait('enter') 
except KeyboardInterrupt:
    pass

main.procesing = False
GPIO.cleanup()
