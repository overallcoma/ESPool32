from wifi_manager import WifiManager
from time import sleep_ms
import webrepl


wm = WifiManager()
if not wm.is_connected():
    wm.connect()
    sleep_ms(1000)
if wm.is_connected():
    print("Wifi is connected")
    sleep_ms(1000)

webrepl.start(password="espool32")
