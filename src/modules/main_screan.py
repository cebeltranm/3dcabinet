from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import color565

class MainScreen(object):

    def __init__(self, sensor1):
        self.backgroundImg = Image.open('resources/main.jpg')
        self.sensor1 = sensor1

    def render(self, disp):
        disp.image(self.backgroundImg)
        try:
            # Read temperature and humidity
            temperature1 = self.sensor1.temperature
            humidity1 = self.sensor1.humidity
            image = Image.new('RGB', (50, 50))
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()
            draw.text((10, 10),f"{temperature1:.1f} C", font=font, fill=(0, 255, 255))

            disp.image(image)
            print(f"Temp: {temperature1:.2f} C    Humidity: {humidity1}%")
        except RuntimeError as error:
            # Errors happen fairly often with DHT sensors, keep going
            print(error.args[0])        