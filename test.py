import RPi.GPIO as GPIO
import time

# BCM Pin Numbers for Solenoids
RELAY_PINS = {
    "sprains": 5,
    "nosebleeds": 6,
    "laceration": 14,
    "allergic": 19,
    "bruise": 26,
    "fainting": 21,
    "burns": 20,
    "choking": 16,
}

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in RELAY_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)  # all OFF initially

def activate_solenoid(key, duration=3):
    pin = RELAY_PINS.get(key)
    if pin is None:
        print(f"[ERROR] Unknown solenoid key: {key}")
        return
    print(f"[INFO] Activating {key} (GPIO {pin})")
    GPIO.output(pin, GPIO.LOW)  # turn ON
    time.sleep(duration)
    GPIO.output(pin, GPIO.HIGH)  # turn OFF

def cleanup():
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup()
        
        activate_solenoid("laceration")  # Example
        
    finally:
        cleanup()