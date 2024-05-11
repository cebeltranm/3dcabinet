import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

# # Setup PWM process
pwm = GPIO.PWM(13, 25000)  # Set frequency to 25 kHz
pwm.start(100)  # Start PWM with 50% duty cycle
time.sleep(1)
pwm.ChangeDutyCycle(100)
time.sleep(100)

# try:
#     while True:
#         # You can vary the duty cycle here to control the fan speed
#         for dc in range(0, 101, 5):
#             time.sleep(10)
#             print(dc)
#             pwm.ChangeDutyCycle(dc)
# except KeyboardInterrupt:
#     pass



# import RPi.GPIO as GPIO
# import time

# Setup GPIO
# GPIO.setmode(GPIO.BCM)
# tach_pin = 4  # Change as per your connection
# GPIO.setup(tach_pin, GPIO.IN)

# # Initialize variables
# rpm_count = 0
# last_time = time.time()

# # Callback function on rising edge
# def rpm_callback(channel):
#     global rpm_count
#     rpm_count += 1

# # Add event detect on rising edge
# GPIO.add_event_detect(tach_pin, GPIO.RISING, callback=rpm_callback)

try:
    while False:
        for dc in range(0, 101, 5):
            print(dc)
            pwm.ChangeDutyCycle(dc)
            time.sleep(1)
        # current_time = time.time()
        # delta = current_time - last_time
        # last_time = current_time
        # rpm = (rpm_count / delta) * 60 / 2  # Dividing by 2 because there are two pulses per revolution (usually)
        # print(f"RPM: {rpm}")
        # rpm_count = 0
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()

