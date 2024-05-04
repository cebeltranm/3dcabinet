import adafruit_rgb_display.rgb as rgb
from modules.render import RenderedComponent
from modules.render import TouchEvent

class Screen(RenderedComponent, TouchEvent):
    def __init__(self, background = None, backgroundColor = None, sections = []):
        super().__init__(background, backgroundColor)
        self.sections = sections
    
    def render(self, disp):
        res = super().render(disp)
        for section in self.sections:
            section.render(disp)
        return res

    def clear_state(self):
        for section in self.sections:
            section.clear_state()

    def touch_event(self, event, time, x, y):
        for section in self.sections:
            section.touch_event(event, time, x, y)


class MainScreen(Screen):
    def __init__(self, sections):
        super().__init__(None, (10, 10, 10), sections)

    def render(self, disp):
        if super().render(disp):
            print("render main screen")
            disp.hline(0, 106, 240, rgb.color565(50, 50, 50))
            disp.hline(0, 212, 240, rgb.color565(50, 50, 50))
            disp.vline(80, 0, 320, rgb.color565(50, 50, 50))
            disp.vline(160, 0, 320, rgb.color565(50, 50, 50))
