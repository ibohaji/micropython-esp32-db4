import algae
from machine import ADC
import machine 

#
class OdSensor(algae):
    def __init__(self):
        pass

    def readOD_raw(self):
        self.adc = machine.ADC(machine.Pin(14))
        readings = []
        for _ in range(10):
            readings.append(self.adc.read())
        self.avg_adc = sum(readings)/len(readings)



