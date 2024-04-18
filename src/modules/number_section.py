from PIL import Image, ImageDraw, ImageFont

class NumberSection(object):

    rendered = False
    _value = None

    def __init__(self, x = 0, y = 0, w = 100, h = 100, font_size = 20):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font_size = font_size
        self.image = Image.new('RGB', (w, h))
        self.font = ImageFont.load_default(self.font_size)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != None and value != self._value:
            self._value = value
            self.rendered = False

    def render(self, disp):
        if self.value != None and self.rendered == False:
            draw = ImageDraw.Draw(self.image)
            draw.rectangle([(0, 0), (self.w, self.h)], fill="black")
            draw.text((0, 0),f"{self.value:.1f}", font=self.font, fill=(0, 255, 255))
            disp.image(self.image, None, self.x, self.y)
            self.rendered = False

    def clear_state(self):
        self.prevValue = None

    def touch_event(self, event, time, x, y):
        pass
 