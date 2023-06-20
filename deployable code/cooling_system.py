import time
from PID import PID
import machine
from read_temp import*
#Pins for the stepper motor

class Cooling_System:
    
    def __init__(self,temp_setpoint):
        self.temp_setpoint = temp_setpoint
        self.time = time.time()
        self.dir_pin,self.pwm,self.fan_pin,self.cooler = self.connect_pins()
        self.pid = PID(1.24,-12,0.48, temp_setpoint)
        self.pid.output_limits = (3000,16000)




    def connect_pins(self):
        self.temp_sens = init_temp_sensor()
        self.dir_pin = machine.Pin(26,machine.Pin.OUT)
        self.pwm = machine.PWM(machine.Pin(25),machine.Pin.OUT)   
        self.fan_pin = machine.Pin(15,machine.Pin.OUT)
        self.cooler = machine.Pin(32,machine.Pin.OUT)
        self.dir_pin(1)
        self.pwm.duty(512)
        self.pwm.freq(16000)
        return self.dir_pin,self.pwm,self.fan_pin,self.cooler


    def average_readings(self):
        #t_end = time.time() + 5
        readings = []
       # while time.time() < t_end:  
        for i in range(10):
            current_value = read_temp(self.temp_sens)
            readings.append(current_value)
            time.sleep(0.1)
        self.average = sum(readings)/len(readings)
        return self.average


    def update_setpoint(self,setpoint):
        self.setpoint = setpoint
        self.pid.update(self.setpoint)



    def update_parameter(self,new_readings):
        self.new_readings = new_readings
        self.control_signal = self.pid.__call__(new_readings)
        if self.control_signal >6000:
            self.cooler.value(0)
        else:
            self.cooler.value(1)
        self.pwm.freq(min(16000,int(self.control_signal*1.3)))
        
    
