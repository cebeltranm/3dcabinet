from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import color565

class Screen(object):
    rendered = False

    def __init__(self, background, sections = []):
        self.backgroundImg = Image.open(background)
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