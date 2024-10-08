import keyboard
import time
import threading
from modules.display import CacheImage, Display
import board
import RPi.GPIO as GPIO
from constants import *
from modules.screens import LoadingScreen, MainScreen, ColorPickerScreen
from modules.sensors import DHT22, PWMSensor
from modules.touch_listener import TouchListener
from modules.render import RenderedComponent
from modules.bus_events import BusEvents, BusEventLlistener
from modules.network import NetworkInfo
from modules.ledstrip import LedStrip
import time

class Main(BusEventLlistener):
    selected_screen = None
    selected_section = None
    procesing = True
    screens = {}

    spi = board.SPI()
    disp = Display(spi)

    def __init__(self):
        self.selected_screen = LoadingScreen()
        threading.Thread(target=self._render_thread).start()
        self.selected_screen.step = 1
        self.network_info = NetworkInfo()
        self.strip = LedStrip()
        time.sleep(0.1)
        self.selected_screen.step = 2
        self.sensor1 = DHT22(SENSOR1_CS)
        self.sensor2 = DHT22(SENSOR2_CS)
        self.pwmsensor = PWMSensor(PWM_PIN, TACH_SENSOR)
        time.sleep(0.1)

        self.selected_screen.step = 3
        bus_events = BusEvents()
        bus_events.set_listener(self)
        time.sleep(0.1)
        self.selected_screen.step = 4
        self.screens['main'] = MainScreen(self.strip, self.pwmsensor)
        time.sleep(0.1)
        self.selected_screen.step = 5
        threading.Thread(target=self._sensors_thread).start()
        time.sleep(0.1)
        self.selected_screen.step = 6
        self.screens['color_picker'] = ColorPickerScreen()
        time.sleep(0.1)
        self.selected_screen.step = 9
        self.touchListener = TouchListener(self.spi, self._touch_event)
        threading.Thread(target=self._touch_thread).start()
        time.sleep(0.1)
        self.selected_screen.step = 10
        self.select_screen('main')
        threading.Thread(target=self._network_thread).start()        

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

    def _network_thread(self):
        while self.procesing:
            self.network_info.check_network_info()
            if self.network_info.private_ip != None:
                time.sleep(10)
            else:
                time.sleep(1)

    def _sensors_thread(self):
        while self.procesing:
            if self.selected_screen == self.screens['main']:
                try:
                    self.selected_screen.setSensorValues([
                        self.sensor1.load_value(), 
                        self.sensor2.load_value(),
                        self.pwmsensor.load_value(),
                    ])
                except Exception as e:
                    print(f"An error occurred: {e}")
                    pass
            time.sleep(1)

    def _touch_thread(self):
        while self.procesing:
            self.touchListener.check_touch()
            time.sleep(0.1)

    def _touch_event(self, event, duration, x = None, y = None):
        if self.selected_screen != None:
            self.selected_screen.touch_event(event, duration, x, y)

main = Main()

try:
    keyboard.wait('enter') 
except KeyboardInterrupt:
    pass

main.procesing = False
GPIO.cleanup()
