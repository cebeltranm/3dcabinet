import time
import board
import digitalio
from modules.cpy_xpt2046 import Touch
from constants import TOUCH_CS, TOUCH_EVENT

class TouchListener(object):
    touch_x_min = 100
    touch_x_max = 1930
    touch_y_min = 160
    touch_y_max = 1905
    last_state = True

    def __init__(self, event_callback):
        self.touch = Touch(board.SPI(), cs=TOUCH_CS,
                x_min=self.touch_x_min, x_max=self.touch_x_max,
                y_min=self.touch_y_min, y_max=self.touch_y_max)
        self.event_callback = event_callback
        self.pin = digitalio.DigitalInOut(TOUCH_EVENT)
        self.pin.direction = digitalio.Direction.INPUT
        self.pin.pull = digitalio.Pull.DOWN

    def check_touch(self):
        current_state = self.pin.value
        if current_state != self.last_state:
            self.last_state = current_state
            if current_state == False:
                self.start_time = time.time()
                self.event_callback('touch_down', 0)
            else:
                end_time = time.time()
                self.event_callback('touch_up', (end_time - self.start_time))
