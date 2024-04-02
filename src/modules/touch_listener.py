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
    last_point_x = None
    last_point_y = None

    def __init__(self, spi, event_callback):
        self.touch = Touch(spi, cs=TOUCH_CS,
                x_min=self.touch_x_min, x_max=self.touch_x_max,
                y_min=self.touch_y_min, y_max=self.touch_y_max)
        self.event_callback = event_callback
        self.pin = digitalio.DigitalInOut(TOUCH_EVENT)
        self.pin.direction = digitalio.Direction.INPUT
        self.pin.pull = digitalio.Pull.DOWN
    
    def transform_points(self, x, y):
        return x, 320 -y

    def check_touch(self):
        current_state = self.pin.value
        if current_state != self.last_state:
            self.last_state = current_state
            if current_state == False:
                self.start_time = time.time()
                xy = self.touch.raw_touch()
                if xy == None:
                    self.last_state = True
                    print ('touch none')
                else:
                    self.last_point_x, self.last_point_y  = self.transform_points(*self.touch.normalize(*xy))
                    self.event_callback('touch_down', 0, self.last_point_x, self.last_point_y)
            else:
                end_time = time.time()
                self.event_callback('touch_up', (end_time - self.start_time), self.last_point_x, self.last_point_y)
        
        return self.last_state == False
