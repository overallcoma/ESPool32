import time
import sys
import ujson


_acidVoltage      = 2032.44
_neutralVoltage   = 1500.0


def load_config(config_name):
    try:
        config_file = open("config.json", r)
    except Exception as e:
       print("config.json not found. Creating file now.")
       temp_open = open("config.json", w)
       temp_open.close()
       config_file = open("config.json", r)
    finally:
        config = ujson.load(config_file)    
        config_return = config[config_name]
        config_file.close()
        return(config_return)


def save_voltage(ph_type, voltage):
    config_file = open("config.json", w)
    config = ujson.load(config_file)
    ph_config = config["ph"]
    ph_config[ph_type] = voltage
    ujson.dump(config_file)
    config_file.close()
    return()
           

class phmeter():    
    def begin(self):
        global _acidVoltage
        global _neutralVoltage
        try:
            ph_config = load_config(ph)
            _neutralVoltage = float(ph_config["neutral"])
            _acidVoltage = float(ph_config["acid"])
        except :
            print("phdata.txt ERROR ! Please run phmeter.reset()")
            sys.exit(1)
            
            
    def read_PH(self, voltage, neutral, acid):
        slope = (7.0-4.0)/((float(neutral)-1500.0)/3.0 - (float(acid)-1500.0)/3.0)
        intercept = 7.0 - slope*(float(neutral)-1500.0)/3
        _phValue = slope*(float(voltage)-1500.0)/3.0+intercept
        round(_phValue,2)
        return _phValue  
 
    
    def calibration(self,voltage):
        if (voltage>1322 and voltage<1678):
            print(">>>Buffer Solution:7.0")
            save_voltage("neutral", voltage)
            print(">>>PH:7.0 Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
            time.sleep(5.0)
        elif (voltage>1854 and voltage<2210):
            print(">>>Buffer Solution:4.0")
            save_voltage("acid", voltage)
            print(">>>PH:4.0 Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
            time.sleep(5.0)
        else:
            print(">>>Buffer Solution Error Try Again<<<")
            
            
    def reset(self):
        _acidVoltage    = 2032.44
        _neutralVoltage = 1500.0
        save_voltage("neutral", _neutralVoltage)
        save_voltage("acid", _acidVoltage)
        print(">>>Reset to default parameters<<<")
