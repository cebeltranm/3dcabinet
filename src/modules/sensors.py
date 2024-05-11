import time
import adafruit_dht
import RPi.GPIO as GPIO

class Sensor:
    def load_value():
        pass


class DHT22(Sensor):
    def __init__(self, pin):
        self.sensor = adafruit_dht.DHT22(pin)

    def load_value(self):
        return {
            'temperature': self.sensor.temperature,
            'humidity': self.sensor.humidity
        }
    
class PWMSensor(Sensor):
    def __init__(self, pin, tach):
        # GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.setup(tach, GPIO.IN)

        self.pwm = GPIO.PWM(pin, 25000)  
        self.pwm.start(100)  
        # self.speed = 100

        self.rpm_count = 0
        self.last_time = time.time()
        GPIO.add_event_detect(tach, GPIO.RISING, callback=self.rpm_callback)

    def rpm_callback(self, channel):
        self.rpm_count += 1

    def set_speed(self, speed):
        self.speed = speed
        self.pwm.ChangeDutyCycle(speed)

    def load_value(self):
        current_time = time.time()
        delta = current_time - self.last_time
        self.last_time = current_time
        rpm = (self.rpm_count / delta) * 60 / 2  # Dividing by 2 because there are two pulses per revolution (usually)
        self.rpm_count = 0
        return {
            "rpm": rpm
        }