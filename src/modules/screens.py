import adafruit_rgb_display.rgb as rgb
from modules.render import RenderedComponent, TouchEvent
from modules.sections import NumberSection, LightSection, ColorPickerSection, ButtonSection, FanSection, WifiSection
from PIL import Image, ImageDraw, ImageFont
from modules.bus_events import BusEvents
from constants import *

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
        self.steps_image = Image.new('RGB', (DISPLAY_WIDTH, 80))

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step):
        self._step = step
        draw = ImageDraw.Draw(self.steps_image)
        draw.rectangle([(0, 0), (DISPLAY_WIDTH, 80)], fill="black")
        for i in range(0, step):
            draw.rectangle( [(10 + i*23, 0), (23 + i*23, 80)], fill=(100, 100, 200))
        self.rendered_steps = False

    def render(self, disp):
        if super().render(disp):
            w = 80
            h = 30
            image = Image.new('RGB', (w, h))
            font = ImageFont.load_default(16)
            draw = ImageDraw.Draw(image)
            draw.rectangle([(0, 0), (w, h)], fill="black")
            draw.text((0, 0),"Loading...", font=font, fill=(100, 100, 100))
            disp.image(image, None, DISPLAY_WIDTH - w, DISPLAY_HEIGHT - h)
            # disp.image(image, None, 20 - h, 10)
        if self.rendered_steps == False:
            disp.image(self.steps_image, None, 0, 100)
            self.rendered_steps = True
            


class MainScreen(Screen):
    def __init__(self, pixels1, pixels2, pwm_sensor):
        self.section1 = {
            'temperature': NumberSection( 161, 79, 53, 44, FONT_SIZE_MEDIUM, COLOR_TEXT, COLOR_BACKGROUND, ALIGN_RIGHT),
            'humidity': NumberSection( 14, 47, 95, 74, FONT_SIZE_BIG, COLOR_TEXT, COLOR_BACKGROUND, ALIGN_RIGHT),
            'light': LightSection(181, 4, pixels1, 'sec1'),
        }
        self.section2 = {
            'temperature': NumberSection( 161, 214, 53, 44, FONT_SIZE_MEDIUM, COLOR_TEXT, COLOR_BACKGROUND, ALIGN_RIGHT),
            'humidity': NumberSection( 14, 178, 95, 74, FONT_SIZE_BIG, COLOR_TEXT, COLOR_BACKGROUND, ALIGN_RIGHT),
            'light': LightSection(181, 136, pixels2, 'sec2'),
        }
        self.pwm = NumberSection(128, 55, 48, 12, FONT_SIZE_SMALL, COLOR_ACCENT, COLOR_BACKGROUND, ALIGN_CENTER)
        self.pwm_section = FanSection(127, 4, pwm_sensor)
        self.wifi = WifiSection(190, 270);

        super().__init__('resources/main.jpg', None, [
            self.section1["temperature"],
            self.section1["humidity"],
            self.section1["light"],
            self.pwm,
            self.pwm_section,
            self.section2["temperature"],
            self.section2["humidity"],
            self.section2["light"],
            self.wifi,
        ])

    def setSensorValues(self, values):
        try:
            self.section1["temperature"].value = int(values[0]["temperature"])
        except Exception as e:
            print(f"An error occurred seting the temperature of sensor1: {e}")
        try:
            self.section1["humidity"].value = int(values[0]["humidity"])
        except Exception as e:
            print(f"An error occurred seting the humidity of sensor1: {e}")

        try:
            self.section2["temperature"].value = int(values[1]["temperature"])
        except Exception as e:
            print(f"An error occurred seting the temperature of sensor2: {e}")

        try:
            self.section2["humidity"].value = int(values[1]["humidity"])
        except Exception as e:
            print(f"An error occurred seting the humidity of sensor2: {e}")

        try:
            self.pwm.value = values[2]["rpm"]
        except Exception as e:
            print(f"An error occurred seting the rpm of the fan: {e}")

#    def render(self, disp):
#        if super().render(disp):
#            for i in range(1, 5):
#                disp.hline(0, i * 64, DISPLAY_WIDTH, rgb.color565(40, 40, 40))
#            for i in range(1, 2):
#                disp.vline(i * 120, 0, DISPLAY_HEIGHT, rgb.color565(40, 40, 40))

class ColorPickerScreen(Screen):
    def __init__(self):
        self.color_picker = ColorPickerSection(0, 0, 240, 280)
        closeButton = ButtonSection( None, 79, 280, 68, 40, self.close_screen )

        super().__init__("resources/color_picker.jpg", COLOR_BACKGROUND, [
            self.color_picker,
            closeButton
        ])

    def close_screen(self):
        bus_events = BusEvents()
        bus_events.select_screen('main')
