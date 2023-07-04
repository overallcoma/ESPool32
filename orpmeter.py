import time
import sys
import ujson


def load_config(config_name):
    try:
        config_file = open("config.json", r)
    except Exception:
        print("config.json not found. Creating file now.")
        temp_open = open("config.json", w)
        temp_open.close()
        config_file = open("config.json", r)
    config = ujson.load(config_file)    
    config_return = config[config_name]
    config_file.close()
    return(config_return)


def save_voltage(ph_type, voltage):
    config_file = open("config.json", w)
    config = ujson.load(config_file)
    ph_config = config["orp"]
    ph_config[ph_type] = voltage
    ujson.dump(config_file)
    config_file.close()
    return()
           

class orp_meter():    
    def begin(self):
        try:
            orp_config = load_config(orp)
        except :
            print("config.json ERROR ! Please run smpl-ph-meter.reset()")
            sys.exit(1)
            
    def read_orp(self, voltage)
        
       
    def read_PH(self, voltage, neutral, acid):
        slope = (7.0-4.0)/((float(neutral)-1500.0)/3.0 - (float(acid)-1500.0)/3.0)
        intercept = 7.0 - slope*(float(neutral)-1500.0)/3
        _phValue = slope*(float(voltage)-1500.0)/3.0+intercept
        round(_phValue,2)
        return _phValue  

