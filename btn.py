from machine import Pin
import time

# Configure the button (Red Thread on D12, Green on GND)
btn = Pin(12, Pin.IN, Pin.PULL_UP)

# Configure the blue LED for the ESP32 (GPIO 2)
esp_led = Pin(2, Pin.OUT)

print("Perfect!")

while True:
    # If u press, btn.value() become 0
    if btn.value() == 0:
        esp_led.value(1)  
    else:
        esp_led.value(0)  
        
    time.sleep(0.05)  