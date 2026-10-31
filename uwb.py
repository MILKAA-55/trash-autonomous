from machine import UART, Pin
import config

class UWBModule:
    def __init__(self, uart_id=1, tx_pin=4, rx_pin=5, baudrate=921600, value_target=1, value_anchor=2):
        # 1. The UART (communication interface) is initialized to 9211600 bauds (reference retrieved from the datasheet of the EWM550).
        self.uart = UART(uart_id, baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin))
        self.value_target = value_target # Value of the Robot
        self.value_anchor = value_anchor # Value of the Station
        print(f"Perfect! All was initalized (Tag: {self.value_target} => Anchor: {self.value_anchor})")


    def read_data(self): 
        print("Gonna read data")
        if self.uart.any():
            raw_data = self.uart.readline() # If we get a response, we read the raw data (in bytes/octets) and saved it 

            if raw_data:
                try: 
                    return raw_data.decode('utf-8').strip() # Try to transform these raw bytes into readable text (utf-8) while cleaning up unnecessary spaces.
                except UnicodeError:
                    print("Ooh, an error about the raw data")
                    return raw_data
        return None


    def get_distance(self, target_id):
        # 2. We send the request to the target ID (2) and we retrieve the distance
        message = self.read_data()
        if message:
            return message
        return None


