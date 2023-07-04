from time import sleep_ms
from wifi_manager import WifiManager
import espool32
from machine import Pin, ADC
from mqtt import MQTTClient, MQTTMessage
import uasyncio as asyncio
import network
import ujson
import tm1637
 

async def main(client):
    await client.connect()
    while True:
        sensor_data = espool32.espool32_main(pin_config["temp"], pin_config["ph"], pin_config["orp"], pin_config["tds"])
        if pin_config["temp"]["display"]:
            freedom_temp = espool32.temp_to_american(sensor_data["temperature"])
            freedom_temp = str(round(freedom_temp))
            #print(str(freedom_temp))
            temp_display.show("    ")
            temp_display.show("t " + freedom_temp)
        if pin_config["ph"]["display"]:
            ph_display.show("    ")
            ph_display_value = str(round(sensor_data["ph"],1))
            ph_display_value = ph_display_value.replace(".","-")
            ph_display.show("p" + ph_display_value)
            #ph_display.show(ph_display_value)
        sensor_data = ujson.dumps(sensor_data).encode()
        print("MQTT Sent - " + sensor_data.decode())
        await client.publish(mqtt_config["topic"], sensor_data, qos=1)
        await asyncio.sleep(5)

pin_config = espool32.pin_setup()

mqtt_config = espool32.load_config("mqtt")
if pin_config["temp"]["display"]:
    temp_display = tm1637.TM1637(clk=Pin(15), dio=Pin(2))
if pin_config["ph"]["display"]:
    ph_display = tm1637.TM1637(clk=Pin(4), dio=Pin(16))

client = MQTTClient()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(client))


# 7 Segment Screen Testing
# import tm1637
# 
# display = tm1637.TM1637(clk=Pin(2), dio=Pin(15))
# display.show("pool")


# Combined Sensor Testing

# while(True):
#     sensor = espool32.get_orp(pin_config["orp"]["pin"], pin_config["orp"]["offset"])
#     print(sensor)
#     sleep_ms(1000)    
#     sensor_data = espool32.espool32_main(pin_config["temp"], pin_config["ph"], pin_config["orp"], pin_config["tds"])
#     print(sensor_data)



# TDS Sensor Testing

# while(True):
#     tdsADCConnection = espool32.config_tds_pin(32)
#     voltage = espool32.get_adc_voltage(tdsADCConnection)
#     print(voltage)

# Temp Sensor Testing

# while(True):
#     temperature_pin = espool32.config_temp_pin(25)
#     probe_list = espool32.onewire_devicescan(temperature_pin)
#     average_temperature = espool32.get_average_temperature(temperature_pin,probe_list)
#     print("average = " + str(round(average_temperature,2)))
#     print(espool32.temp_to_american(average_temperature))
#     print("-----")
#     sleep_ms(1000)
    

# PH Sensor Testing

# while(True):
#     phADCConnection = espool32.config_ph_pin(33)
#     voltage = espool32.get_adc_voltage(phADCConnection)
#     ph_reading = espool32.get_ph(voltage)
#     print(ph_reading)
#     sleep_ms(1000)



