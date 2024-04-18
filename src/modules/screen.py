from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import color565

class Screen(object):
    rendered = False

    def __init__(self, background = None, backgroundColor = None, sections = []):
        if background == None:
            self.backgroundImg = Image.new('RGB', (320, 240))
            if backgroundColor != None:
                draw = ImageDraw.Draw(self.backgroundImg)
                draw.rectangle([(0, 0), (320, 240)], fill=backgroundColor)
        else:
            self.backgroundImg = Image.open(background)
        self.backgroundColor = backgroundColor
        self.sections = sections

    def render(self, disp):
        if self.rendered == False:
            disp.image(self.backgroundImg)
            self.rendered = True
        for section in self.sections:
            section.render(disp)

    def clear_state(self):
        self.rendered = False
        for section in self.sections:
            section.clear_state()

    def touch_event(self, event, time, x, y):
        for section in self.sections:
            section.touch_event(event, time, x, y)
