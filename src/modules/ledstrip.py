import time
from rpi_ws281x import PixelStrip, Color
from constants import LED_PIN, LED_SEC1_SIZE, LED_SEC2_SIZE, LED_FILL_TIME

LED_COUNT = LED_SEC1_SIZE + LED_SEC2_SIZE
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800kHz).
LED_DMA = 10           # DMA channel to use for generating signal (try 10).
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest.
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift).
LED_CHANNEL = 0        # Set to 1 for GPIOs 13, 19, 41, 45, or 53.

class LedStrip:
    _instance = None 

    class Section:
        def __init__(self, strip, init, width):
            self._strip = strip
            self._init = init
            self._width = width
            self._color = None
            self._brightness = 0


        def _getColorBrightness(self, color, brightness):
            """Set pixel color with adjustable brightness for individual pixels."""
            r = int(color[0] * brightness / 255)  # Scale red by brightness
            g = int(color[1] * brightness / 255)  # Scale green by brightness
            b = int(color[2] * brightness / 255)  # Scale blue by brightness
            return Color(r, g, b)

        
        def setBrightness(self, brightness):
            if brightness < 0:
                brightness = 0
            if brightness > 255:
                brightness = 255
            if self._color and self._brightness != brightness:
                self._brightness = brightness
                self.fill(self._color, True if brightness < 100 else False)
            else:
                self._brightness = brightness
        
        def fill(self, color, wait = True):
            self._color = color
            colorToUse = self._getColorBrightness(color, self._brightness) if self._brightness < 255 else Color(color[0], color[1], color[2])
            wait_ms = (LED_FILL_TIME / self._width) / 1000
            for i in range(self._width):
                self._strip.setPixelColor(i + self._init, colorToUse)
                if wait == True:
                    self._strip.show()
                    time.sleep(wait_ms)
            if wait == False:
                self._strip.show()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LedStrip, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self._strip.begin()
        self._sections = [
            LedStrip.Section(self._strip, 0, LED_SEC1_SIZE),
            LedStrip.Section(self._strip, LED_SEC1_SIZE + 1, LED_SEC2_SIZE),
        ]

    def getSection(self, id):
        return self._sections[id]
