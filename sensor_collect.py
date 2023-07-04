from atm90e32_spi import atm90e32_spi
from atm90e32_ctl import atm90e32_ctl
import ujson
from common import get_machine_id


def collect():
    spiConn = atm90e32_spi()
    config_file = open("config.json")
    config = ujson.load(config_file)
    sensors_config = config["nodeConfig"]["sensors"]

    linefreq = sensors_config["linefreq"]
    pgagain = sensors_config["pgagain"]
    ugain = sensors_config["ugain"]

    def amps_calc(watts, volts):
        try:
            amps = int(watts) / int(volts)
            return amps
        except:
            return 0

    def get_sensor_status(sensornumber):
        sensornumber = str(sensornumber)
        sensor_config = sensors_config[sensornumber]
        gain = sensor_config["gain"]
        pin = sensor_config["pin"]
        collected_data = atm90e32_ctl(linefreq, pgagain, ugain, gain, gain, gain, pin, spiConn)
        # print(collected_data)
        wattsA = collected_data.apparent_powerA
        wattsB = collected_data.apparent_powerB
        wattsC = collected_data.apparent_powerC
        voltsA = collected_data.line_voltageA
        voltsB = collected_data.line_voltageB
        voltsC = collected_data.line_voltageC
        ampsA = amps_calc(wattsA,voltsA)
        ampsB = amps_calc(wattsB,voltsB)
        ampsC = amps_calc(wattsC,voltsC)
        status = {
            "wattsA": wattsA,
            "wattsB": wattsB,
            "wattsC": wattsC,
            "voltsA": voltsA,
            "voltsB": voltsB,
            "voltsC": voltsC,
            "ampsA": ampsA,
            "ampsB": ampsB,
            "ampsC": ampsC,
            }
        return status

    sensor_output = []

    for key, value in sensors_config.items():
        if "sensor" in key:
            
            if value["name"] == "NA":
                continue
            
            sensor_id = str(key)
            output_dict = get_sensor_status(sensor_id)
            output_dict["name"] = value["name"]
            sensor_output.append(output_dict)
    return(sensor_output)
print(collect())