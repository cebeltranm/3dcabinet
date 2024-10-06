from PIL import Image
import pickle
from modules.display import CacheImage, Display

import board


# img = Image.open("resources/color_picker.jpg")
# imwidth, imheight = img.size
# pixels = bytearray(imwidth * imheight * 2)
# for i in range(imwidth):
#     for j in range(imheight):
#         pix = rgb.color565(img.getpixel((i, j)))
#         pixels[2 * (j * imwidth + i)] = pix >> 8
#         pixels[2 * (j * imwidth + i) + 1] = pix & 0xFF

# data = {
#     "width": imwidth,
#     "height": imheight,
#     "pixels": pixels
# }

# with open("data.pkl", "wb") as file:
#     pickle.dump(data, file)

spi = board.SPI()
disp = Display(spi)

# disp.fill_rectangle(0,0,240,320, rgb.color565((18, 18, 18)))


# Images.process_images()
img = CacheImage("resources/main.pkl")
disp.drawImage(0,0,img)
