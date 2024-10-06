import pickle
import os
import adafruit_rgb_display.ili9341 as ili9341
from constants import DISPLAY_ROTATION, DISPLAY_CS_PIN, DISPLAY_DC_PIN, DISPLAY_RESET_PIN
from PIL import Image
import adafruit_rgb_display.rgb as rgb

def process_image(img):
    imwidth, imheight = img.size
    pixels = bytearray(imwidth * imheight * 2)
    for i in range(imwidth):
        for j in range(imheight):
            pix = rgb.color565(img.getpixel((i, j)))
            pixels[2 * (j * imwidth + i)] = pix >> 8
            pixels[2 * (j * imwidth + i) + 1] = pix & 0xFF
    data = {
        "width": imwidth,
        "height": imheight,
        "pixels": pixels
    }
    return data

class CacheImage():
    _images = {}

    def __new__(cls, *args, **kwargs):
        if args[0] not in cls._images:
            cls._images[args[0]] = super(CacheImage, cls).__new__(cls)
        return cls._images[args[0]]

    def __init__(self, img_path):
        if img_path.endswith((".png", ".jpg", ".jpeg")):
            img = Image.open(img_path)
            imwidth, imheight = img.size
            pixels = bytearray(imwidth * imheight * 2)
            for i in range(imwidth):
                for j in range(imheight):
                    pix = rgb.color565(img.getpixel((i, j)))
                    pixels[2 * (j * imwidth + i)] = pix >> 8
                    pixels[2 * (j * imwidth + i) + 1] = pix & 0xFF

            self.width = imwidth
            self.height = imheight
            self.pixels = pixels
        elif img_path.endswith((".pkl")):
            with open(img_path, "rb") as binary_file:
                loaded_data = pickle.load(binary_file)
                self.width = loaded_data["width"]
                self.height = loaded_data["height"]
                self.pixels = loaded_data["pixels"]

    def save(self, img_path):
        data = {
            "width": self.width,
            "height": self.height,
            "pixels": self.pixels
        }
        if img_path.endswith((".pkl")):
            with open(img_path, "wb") as file:
                pickle.dump(data, file)

    @staticmethod
    def process_images():
        folder_path = "resources/"
        for filename in os.listdir(folder_path):
            if filename.endswith((".png", ".jpg", ".jpeg")):
                img_path = os.path.join(folder_path, filename)
                print(img_path)
                img = CacheImage(img_path)
                root, _ = os.path.splitext(img_path)
                img.save(root + ".pkl")

class Display(ili9341.ILI9341):
    def __init__(self, spi):
        super().__init__(
            spi, 
            rotation=DISPLAY_ROTATION, 
            cs=DISPLAY_CS_PIN, 
            dc=DISPLAY_DC_PIN, 
            rst=DISPLAY_RESET_PIN
        )
    
    def drawImage(self, x, y, img):
        if img.width > 0:
            self._block(x, y, x + img.width - 1, y + img.height - 1, img.pixels)