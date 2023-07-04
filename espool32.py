from machine import Pin, ADC, reset
from time import sleep_ms
from phmeter import phmeter
import onewire
import ds18x20
import tm1637
import ujson


def load_config(config_name):
    config_file = open("config.json")
    config = ujson.load(config_file)    
    config_return = config[config_name]
    return config_return    
    

def config_ph_pin(PinNumber):
    phPin = ADC(Pin(PinNumber))
    phPin.atten(ADC.ATTN_11DB)
    return(phPin)


def config_orp_pin(PinNumber):
    orpPin = ADC(Pin(PinNumber))
    orpPin.atten(ADC.ATTN_11DB)
    return(orpPin)


def config_tds_pin(PinNumber):
    tdsPin = ADC(Pin(PinNumber))
    tdsPin.atten(ADC.ATTN_6DB)
    return(tdsPin)
    
    
def get_adc_voltage(ADCConnection):
    adcVoltage = ADCConnection.read()
    return(adcVoltage)


def get_ph_reading(voltage, neutral, acid):
    phReading = phmeter()
    print("-------")
    print("PH Voltage = " + str(voltage))
    print("Neutral Voltage = " + str(neutral))
    print("Acid Voltage = " + str(acid))
    print("-------")
    returnValue = phReading.read_PH(voltage, neutral, acid)
    return(returnValue)


def config_temp_pin(PinNumber):
    tempPin = Pin(PinNumber)
    ow_object = ds18x20.DS18X20(onewire.OneWire(tempPin))
    return(ow_object)


def onewire_devicescan(onewire_object):
    roms = onewire_object.scan()
    return(roms) #List Object


def get_average_temperature(ow_temp_object,roms):
    try:
        temperature_list = []
        sleep_time = round(1000/len(roms))
        for rom in roms:
            ow_temp_object.convert_temp()
            sleep_ms(sleep_time)
            temperature_reading = ow_temp_object.read_temp(rom)
            temperature_list.append(temperature_reading)
        average_temp = sum(temperature_list) / len(temperature_list)
        return(average_temp)
    except Exception as e:
        print(e)
        print("Temperature Reading Error - Setting to 25 to continue")
        return(25)


def temp_to_american(c):
    return((c*9/5)+32)


def get_temp(pin):
    probe_list = onewire_devicescan(pin)
    average_temperature = get_average_temperature(pin,probe_list)
    return(average_temperature)


def get_ph(pin, neutral, acid):
    voltage = get_adc_voltage(pin)
#     print("PH Voltage = " + str(voltage))
    ph_reading = get_ph_reading(voltage, neutral, acid)
    return(ph_reading)


def get_orp(pin, offset):
    voltage = (get_adc_voltage(pin)) + offset
    return(voltage)


def get_tds(pin):
    tds_reading = get_adc_voltage(pin)
    return(tds_reading)


def pin_setup():
    temp_config = load_config("temperature")    
    ph_config = load_config("ph")
    orp_config = load_config("orp")
    tds_config = load_config("tds")
    
    
    temp_pin = config_temp_pin(int(temp_config["pin"]))
    temp_pin = {
        "pin": temp_pin,
        "display": temp_config["display"]
        }
    
    ph_pin = config_ph_pin(int(ph_config["pin"]))
    ph_params = ph_setup()
    ph_display = False
    ph_pin = {
        "pin": ph_pin,
        "neutral": ph_params["neutral"],
        "acid": ph_params["acid"],
        "display": ph_config["display"]
        }
    
    orp_pin = config_orp_pin(int(orp_config["pin"]))
    orp_offset = int(orp_config["offset"])
    orp_pin = {
        "pin": orp_pin,
        "offset": orp_offset
        }
    
    tds_pin = config_tds_pin(int(tds_config["pin"]))
    
    return_dict = {
        "temp":temp_pin,
        "ph":ph_pin,
        "orp":orp_pin,
        "tds":tds_pin
        }
    return(return_dict)


def ph_voltage(ph_measure):
    ph_config = load_config("ph")
    voltage = ph_config[ph_measure]
    return(voltage)


def ph_setup():   
    neutral_voltage = float(ph_voltage("neutral"))
    acid_voltage = float(ph_voltage("acid"))
    return_dict = {
        "neutral":neutral_voltage,
        "acid": acid_voltage
        }
    return(return_dict)

   
def get_data_json(temp_pin, ph_pin, orp_pin, tds_pin):
    temperature = get_temp(temp_pin["pin"])
    ph = get_ph(ph_pin["pin"], ph_pin["neutral"], ph_pin["acid"])
    orp = get_orp(orp_pin["pin"], orp_pin["offset"])
    tds = get_tds(tds_pin)
    json_return = {
        "ph": ph,
        "temperature": temperature,
        "orp": orp,
        "tds": tds
        }
    return(json_return)


def espool32_main(temperature, ph, orp, tds):
    collected_data = get_data_json(temperature, ph, orp, tds)
    return(collected_data)