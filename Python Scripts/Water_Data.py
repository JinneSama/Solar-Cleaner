import RPi.GPIO as GPIO
import time
from flask import Flask, jsonify

# GPIO pin numbers
TRIGGER_PIN = 17
ECHO_PIN = 27

# Initialize the Flask application
app = Flask(__name__)

# Set up GPIO
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)


def measure_distance():
    # Set the trigger pin to HIGH
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, GPIO.LOW)

    # Wait for the echo pin to go HIGH
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()

    # Wait for the echo pin to go LOW
    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()

    # Calculate the pulse duration and convert it to distance
    pulse_duration = pulse_end - pulse_start
    speed_of_sound = 34300  # Speed of sound in cm/s
    distance = pulse_duration * speed_of_sound / 2

    return distance


@app.route('/distance')
def get_distance():
    distance = measure_distance()
    return jsonify({'distance': distance})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)