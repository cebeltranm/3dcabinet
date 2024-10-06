import adafruit_rgb_display.rgb as rgb
from modules.display import CacheImage

class RenderedComponent: 
    rendered = False

    def __init__(self, background = None, backgroundColor = None, x = 0, y = 0, w = 240, h = 320):
        if background != None:
            self.backgroundCacheImg = CacheImage(background)
        else:
            self.backgroundCacheImg = None
        self.backgroundImg = None
        self.backgroundColor = backgroundColor
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def render(self, disp):
        if self.rendered == False:
            if self.backgroundColor != None:
                disp.fill_rectangle(0,0,240,320, rgb.color565(self.backgroundColor))
            if self.backgroundImg != None:
                disp.image(self.backgroundImg, None, self.x, self.y)
            if self.backgroundCacheImg != None:
                disp.drawImage(self.x, self.y, self.backgroundCacheImg)

            self.rendered = True
            return True

    def clear_state(self):
        self.rendered = False

class TouchEvent:
    def touch_event(self, event, time, x, y):
        return False
