import threading
import math
from PIL import Image, ImageDraw, ImageFont

class ColorPickerSection(object):
    #radians value of a specific degree
    A_180 = 3.1416 
    A_60 = 1.047172
    A_55 = 0.9599

    def __init__(self, select_color, x = 0, y = 0, w = 280, h = 240):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.select_color = select_color
        self.mx = w / 2
        self.my = h / 2
        self.background = Image.open(f"resources/pick_color.png")
        self.rendered = False

        # self.image = Image.new('RGB', (w, h))
        # self.imageInit = False

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


    def render(self, disp):
        # if self.imageInit == False:
        #     self.imageInit == True
        #     threading.Thread(target=self.generateImage).start()
        if self.rendered == False:
            self.rendered = True
            disp.image(self.background, None, self.x, self.y)

    def clear_state(self):
        self.rendered = False

    def touch_event(self, event, time, x, y):
        if event == 'touch_down' and self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h:
            color = self.getColorOfPoint(x - self.x, y - self.y)
            print("in box", color)
            self.select_color(color)
