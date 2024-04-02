from PIL import Image, ImageDraw

class LoadingScreen(object):

    loadingImg = Image.open('resources/loading.png')

    def __init__(self):
        pass

    def render(self, disp):
        disp.image(self.loadingImg)