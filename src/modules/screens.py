import adafruit_rgb_display.rgb as rgb
from modules.render import RenderedComponent, TouchEvent
from modules.sections import NumberSection, LightSection, ColorPickerSection, ButtonSection, FanSection
from PIL import Image, ImageDraw, ImageFont
from modules.bus_events import BusEvents

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
        super().clear_state()
        for section in self.sections:
            section.clear_state()

    def touch_event(self, event, time, x, y):
        for section in self.sections:
            section.touch_event(event, time, x, y)

class LoadingScreen(Screen):

    _step = 5
    rendered_steps = True

    def __init__(self):
        super().__init__(None, (0,0,0))
        self.steps_image = Image.new('RGB', (320, 40))

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step):
        self._step = step
        draw = ImageDraw.Draw(self.steps_image)
        draw.rectangle([(0, 0), (320, 40)], fill="black")
        for i in range(0, step):
            draw.rectangle( [(10 + i*30, 0), (30 + i*30, 40)], fill=(100, 100, 200))
        self.rendered_steps = False

    def render(self, disp):
        if super().render(disp):
            w = 80
            h = 20
            image = Image.new('RGB', (w, h))
            font = ImageFont.load_default(16)
            draw = ImageDraw.Draw(image)
            draw.rectangle([(0, 0), (w, h)], fill="black")
            draw.text((0, 0),"Loading...", font=font, fill=(100, 100, 100))
            disp.image(image, None, 220 - h, 10)
        if self.rendered_steps == False:
            disp.image(self.steps_image, None, 100, 0)
            self.rendered_steps = True
            


class MainScreen(Screen):
    def __init__(self, pixels1, pwm_sensor):
        self.section1 = {
            'temperature': NumberSection( 25, 225, 80, 50, 40),
            'humidity': NumberSection( 95, 225, 80, 50, 40),
            'light': LightSection(180, 240, pixels1, 'sec1'),
        }
        self.section2 = {
            'temperature': NumberSection( 25, 120, 80, 50, 40),
            'humidity': NumberSection( 95, 120, 80, 50, 40)
        }
        self.pwm = NumberSection(55, 10, 80, 20, 20)
        self.pwm_section = FanSection(10, 30, pwm_sensor)

        super().__init__(None, (0, 0, 0), [
            self.section1["temperature"],
            self.section1["humidity"],
            self.section2["temperature"],
            self.section2["humidity"],
            self.pwm,
            self.section1["light"],
            self.pwm_section,
        ])

    def setSensorValues(self, values):
        self.section1["temperature"].value = values[0]["temperature"]
        self.section1["humidity"].value = values[0]["humidity"]
        self.section2["temperature"].value = values[1]["temperature"]
        self.section2["humidity"].value = values[1]["humidity"]
        self.pwm.value = values[2]["rpm"]

    def render(self, disp):
        if super().render(disp):
            disp.hline(0, 106, 240, rgb.color565(40, 40, 40))
            disp.hline(0, 212, 240, rgb.color565(40, 40, 40))
            disp.vline(80, 0, 320, rgb.color565(40, 40, 40))
            disp.vline(160, 0, 320, rgb.color565(40, 40, 40))

class ColorPickerScreen(Screen):
    def __init__(self):
        self.color_picker = ColorPickerSection(0, 0)
        closeButton = ButtonSection( 'resources/close.jpg', 1, 280, self.close_screen )

        super().__init__(None, (0, 0, 0), [
            self.color_picker,
            closeButton
        ])

    def close_screen(self):
        bus_events = BusEvents()
        bus_events.select_screen('main')
