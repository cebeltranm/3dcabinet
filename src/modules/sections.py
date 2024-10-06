import math
from modules.render import RenderedComponent, TouchEvent
from PIL import Image, ImageDraw, ImageFont
from modules.bus_events import BusEvents
from modules.store import Store
from modules.network import NetworkInfo
from constants import COLOR_BACKGROUND, COLOR_TEXT, ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER, DISPLAY_HEIGHT, DISPLAY_WIDTH
from modules.display import CacheImage

class Section (RenderedComponent, TouchEvent):
    def __init__(self, x, y , w, h):
        super().__init__(None, None, x, y, w, h)
    
    def is_point_into(self, x,y):
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h

class NumberSection(Section):
    _value = None

    def __init__(self, x, y, w, h, font_size = 20, font_color = COLOR_TEXT, background = COLOR_BACKGROUND, align = ALIGN_LEFT):
        super().__init__(x, y, w, h)
        self.font_size = font_size
        self.backgroundImg = Image.new('RGB', (w, h))
        self.font = ImageFont.load_default(self.font_size)
        self.font_color = font_color
        self.background = background
        self.align = align

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != None and value != self._value:
            self._value = value
            draw = ImageDraw.Draw(self.backgroundImg)
            draw.rectangle([(0, 0), (self.w, self.h)], fill=self.background)
            x = 0
            if self.align ==ALIGN_RIGHT:
                x = self.w - draw.textlength(str(self.value), font=self.font)
            if self.align == ALIGN_CENTER:
                x = int( (self.w - draw.textlength(str(self.value), font=self.font)) / 2)
            draw.text(( x, 0),str(self.value), font=self.font, fill=self.font_color, align=ALIGN_LEFT)
            self.rendered = False

class LevelSection(Section):
    images = None

    def __init__(self, x, y, images):
         super().__init__(x, y, images[0].width, images[0].height)
         self.images = images

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level
        if level < 1:
            self._level = 1
        if level > len(self.images):
            self._level = len(self.images)
        self.backgroundCacheImg = self.images[self._level - 1]
        self.rendered = False
        self.on_level_changed(self._level)
    
    def increase_level(self):
        if self.level >= len(self.images):
            self.level = 0
        else:
            self.level = self.level + 1

    def touch_event(self, event, time, x, y):
        if event == 'touch_up' and self.is_point_into(x,y):
            if (time > 0.5):
                self.on_selected()
            else:
                self.increase_level()

    def on_level_changed(self):
        pass

    def on_selected(self):
        pass

class LightSection(LevelSection):
    light_images = None
    pixels = None
    
    def __init__(self, x, y, pixels, id):
        if LightSection.light_images == None:
            LightSection.light_images = [CacheImage(f"resources/light{i}.pkl") for i in range(1, 6)]
        super().__init__( x, y, LightSection.light_images)

        self.pixels = pixels
        self._id = id
        store = Store()
        self.level = store.get_value(f"${id}_level") if store.get_value(f"${id}_level") else 0
        self.pixels.fill(store.get_value(f"${id}_color") if store.get_value(f"${id}_color") else (0,0,250))

    def set_color(self, color):
        self.pixels.fill(color)
        store = Store()
        store.set_value(f"${self._id}_color", color)

    def on_level_changed(self, level):
        if self.pixels:
            self.pixels.setBrightness( 0 if level <=1 else 255 * (level - 1) / (len(LightSection.light_images) - 1) )
        store = Store()
        store.set_value(f"${self._id}_level", level)
    
    def on_selected(self):
        bus_events = BusEvents()
        bus_events.select_screen('color_picker', self)

class FanSection(LevelSection):
    fan_images = None
    pwm_sensor = None

    def __init__(self, x, y, pwm_sensor):
        if FanSection.fan_images == None:
            FanSection.fan_images = [CacheImage(f"resources/fan{i}.pkl") for i in range(1, 5)]
        super().__init__( x, y, FanSection.fan_images)
        self.pwm_sensor = pwm_sensor
        store = Store()
        self.level = store.get_value("pwm_level") if store.get_value("pwm_level") else 0

    def on_level_changed(self, level):
        if self.pwm_sensor:
            self.pwm_sensor.set_speed( 100 - (0 if level <=1 else 100 * (level - 1) / (len(FanSection.fan_images) - 1)))
        store = Store()
        store.set_value("pwm_level", level)
    
class ColorPickerSection(Section):
    #radians value of a specific degree
    A_180 = 3.1416 
    A_60 = 1.047172
    A_55 = 0.9599

    def __init__(self, x = 0, y = 0, w = DISPLAY_WIDTH, h = DISPLAY_HEIGHT):
        super().__init__(x, y, w, h )
        self.mx = w / 2
        self.my = h / 2
        # self.backgroundImg = Image.open("resources/pick_color.png")

    def getColor(self, a1, a2, angle, distance):
        if a1 <= angle and angle <= a2:
            return 255
        val1 = 0
        a2v = -self.A_180 if a2 == self.A_180 else a2
        if a2v <= angle and angle <= (a2v + self.A_55):
            val1 = 255 - (angle - a2v ) * 255 / self.A_55
        a1v = self.A_180 if a1 == -self.A_180 else a1
        if a1v >= angle and angle >= (a1v - self.A_55):
            val1 = (angle - (a1v - self.A_55)) * 255 / self.A_55

        val2 = 255 - (distance * 255 / ( self.my - 5 if self.my < self.mx else self.mx - 5 ))

        return int(val1 if val1 > val2 else val2)

    def getColorOfPoint(self, x, y):
        angle = math.atan2(y - self.my, x - self.mx)
        distance = math.sqrt(math.pow(x - self.mx, 2) + math.pow(y - self.my, 2))
        return self.getColor(- self.A_180, -self.A_60, angle, distance), self.getColor(- self.A_60, self.A_60, angle, distance), self.getColor(self.A_60, self.A_180, angle, distance)

    def generateImage(self):
        draw = ImageDraw.Draw(self.image)

        for x in range(0, self.w):
            for y in range(0, self.h):
                angle = math.atan2(y - self.my, x - self.mx)
                distance = math.sqrt(math.pow(x - self.mx, 2) + math.pow(y - self.my, 2))

                draw.point((x, y), fill=(
                    self.getColor(- self.A_180, -self.A_60, angle, distance), 
                    self.getColor(- self.A_60, self.A_60, angle, distance), 
                    self.getColor(self.A_60, self.A_180, angle, distance)
                ))
        self.rendered = False

    def touch_event(self, event, time, x, y):
        if event == 'touch_down' and self.is_point_into(x,y):
            color = self.getColorOfPoint(x - self.x, y - self.y)
            bus_events = BusEvents()
            bus_events.select_color(color)


class ButtonSection(Section):
    def __init__(self, image, x, y, w, h, action):
        super().__init__(x, y, w, h)
        self.action = action    
        if image:
            backgroundImg = Image.open(image)
            self.backgroundImg = backgroundImg

    def touch_event(self, event, time, x, y):
        if event == 'touch_down' and self.is_point_into(x,y):
            self.action()

class WifiSection(Section):
    images = None
    IP = None
    
    def __init__(self, x, y):
        if self.images == None:
            self.images = [CacheImage(f"resources/wifi{i}.pkl") for i in range(1, 3)]
        super().__init__(x, y, self.images[0].width, self.images[0].height)
        self.backgroundCacheImg = self.images[0]
        self.network_info = NetworkInfo()

    def render(self, disp):
        if self.IP == None and self.network_info.private_ip != None:
            self.backgroundCacheImg = self.images[1]
            self.rendered = False
        if self.IP != None and self.network_info.private_ip == None:
            self.backgroundCacheImg = self.images[0]
            self.rendered = False
        self.IP = self.network_info.private_ip
        super().render(disp)
