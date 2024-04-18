from PIL import Image, ImageDraw, ImageFont
import neopixel
from constants import LEDS1_PIN, LEDS1_SIZE

class LightSection(object):
    light_images = None

    rendered = False
    level = 3

    def __init__(self, x, y, select_function):
        if LightSection.light_images == None:
            LightSection.light_images = [Image.open(f"resources/light{i}.jpg") for i in range(1, 6)]
        self.x = x
        self.y = y
        self.pixels = neopixel.NeoPixel(LEDS1_PIN, LEDS1_SIZE, pixel_order=neopixel.GRB, brightness=0)
        self.pixels.fill((0, 255, 0))
        self.increase_level()
        self.select_function = select_function

    def increase_level(self):
        self.level = self.level + 1
        if self.level >= 5:
            self.level = 0
        self.rendered = False
        self.pixels.brightness = self.level / 4

    def set_color(self, color):
        print("set color", color)
        self.pixels.fill(color)
        self.pixels.fill(color)

    def render(self, disp):
        if self.rendered == False:
            self.rendered = True
            disp.image(LightSection.light_images[self.level], None, self.x, self.y)

    def clear_state(self):
        self.rendered = False

    def touch_event(self, event, time, x, y):
        if event == 'touch_up' and self.x <= x <= self.x + LightSection.light_images[0].width and self.y <= y <= self.y + LightSection.light_images[0].height:
            if (time > 0.5):
                self.select_function(self)
            else:
                self.increase_level()
        else:
            if event == 'touch_up':
                print("no light", x, y)

