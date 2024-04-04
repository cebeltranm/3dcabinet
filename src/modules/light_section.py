from PIL import Image, ImageDraw, ImageFont

class LightSection(object):
    light_images = None

    rendered = False
    level = 0

    def __init__(self):
        if LightSection.light_images == None:
            LightSection.light_images = [Image.open(f"resources/light{i}.jpg") for i in range(1, 6)]

    def increase_level(self):
        self.level = self.level + 1
        if self.level >= 5:
            self.level = 0
        print(self.level)
        self.rendered = False

    def render(self, disp):
        self.increase_level()
        if self.rendered == False:
            self.rendered = True
            disp.image(LightSection.light_images[self.level])

    def clear_state(self):
        self.rendered = False