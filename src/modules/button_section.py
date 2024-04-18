from PIL import Image

class ButtonSection(object):
    rendered = False

    def __init__(self, image, x, y, action):
        self.x = x
        self.y = y
        self.action = action
        self.image = Image.open(image)

    def render(self, disp):
        if self.rendered == False:
            disp.image(self.image, None, self.x, self.y)
            self.rendered = True

    def clear_state(self):
        self.rendered = False

    def touch_event(self, event, time, x, y):
        if event == 'touch_down' and self.x <= x <= self.x + self.image.width and self.y <= y <= self.y + self.image.height:
            print("Touch button")
            self.action()
