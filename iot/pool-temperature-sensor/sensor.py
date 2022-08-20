from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()

def read_temp():
    return sensor.get_temperature()
