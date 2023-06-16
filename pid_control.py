# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 09:00:50 2023

@author: Test
"""

import machine
from time import sleep
from machine import PWM
from machine import ADC
from machine import DAC
from read_temp import*
from mmqt_connection import*
from PID import PID



#connect_wifi

connect_wifi("OnePlus 9 Pro","flaeskesteg")

username = "ibsen95"
io_key = "aio_RwUJ54dSmcttwF0T5q6nUAaEHIXJ"
feedname = "Pid-Final"

client = MQTTConnect(username,io_key,feedname)



def algae_pump():
    algae_pump_dir =  machine.Pin(27,machine.Pin.OUT)
    algae_pump_pwm = machine.PWM(machine.Pin(33),machine.Pin.OUT)
    return algae_pump_dir,algae_pump_pwm


#Pins for the stepper motor

def connect_pins():
    dir_pin = machine.Pin(26,machine.Pin.OUT)
    pwm = machine.PWM(machine.Pin(25),machine.Pin.OUT)   
    return dir_pin,pwm

def fan_pin():
    fan_pin = machine.Pin(15,machine.Pin.OUT)
    cooler = machine.Pin(32,machine.Pin.OUT)
    return fan_pin,cooler


def inital_values():
    dir_pin.value(1)
    fan_pin.value(1)
    cooler.value(0)
    
    
def pid_init(p,i,d):
    pid = PID(p,i,d,setpoint = 17.5)
    #values
    pid.output_limits = (750,16000)
    return pid





dir_pin,pwm = connect_pins()
fan_pin,cooler = fan_pin()
inital_values()
temp_sens = init_temp_sensor(TENP_SENS_ADC_PIN_NO = 39)





algae_pump_dir,algae_pump_pwm = algae_pump()
algae_pump_pwm.duty(512)
algae_pump_pwm.freq(10000)

#Initialize a stepper_motor values object
pwm.duty(512)
pwm.freq(16000)




#%%

# Pid 



pid = pid_init(1.09,-3.9,0.8)
file = []
seconds = time.time()



def apply_signal(signal,cooler,pwm):
    #Apply the control signal 
    if signal > 3500:
        cooler.value(False) # 12v
        pwm.freq(int(signal)) 

    else:
        cooler.value(True) # 5v
        pwm.freq(int(signal)) 

        
while True :
    current_value = read_temp(temp_sens)
    readings = []
    t_end = time.time() + 10
    control_signal = 0
    
    while time.time() < t_end:  
        current_value = read_temp(temp_sens)
        readings.append(current_value)
        time.sleep(0.25)
        
        
    average = sum(readings)/len(readings)
    control_signal = pid.__call__(average) *1.30 + 400
    
    apply_signal(control_signal, cooler, pwm)
        
    p, i, d = pid.components
    publish(average,feedname,username,client)
    print("\n -----------------------------")
    print("avg Temperature: {}".format(average))
    print("\n Error: {}".format(average - 17.5))
    print("\n P:{} \n I: {} \n D:{}".format(p,i,d))
    print("\n Control signal:{}".format(control_signal))
