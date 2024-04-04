from PIL import Image, ImageDraw, ImageFont

class NumberSection(object):

    prevValue = None

    def __init__(self, get_value, x = 0, y = 0, w = 100, h = 100, font_size = 20):
        self.get_value = get_value
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font_size = font_size
        self.image = Image.new('RGB', (w, h))
        self.font = ImageFont.load_default(self.font_size)

    def render(self, disp):
        value = self.get_value()
        if value != None and value != self.prevValue:
            self.prevValue = value

            draw = ImageDraw.Draw(self.image)
            draw.rectangle([(0, 0), (self.w, self.h)], fill="black")
            draw.text((0, 0),f"{value:.1f}", font=self.font, fill=(0, 255, 255))
            disp.image(self.image, None, self.x, self.y)

    def clear_state(self):
        self.prevValue = None