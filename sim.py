#Author : Ibrahim Deiaa
##----- This is a simple simulation intended to fine-tune and identify the optimal parameters for a PID control system. 
import time
import math 
import matplotlib.pyplot as plt 
from simple_pid import PID
from cmath import inf

########Function to calculate two different water temperater of different volumes after combining/mixing according to the 
########Unites are degrees celcius and weight in grams, water has a density of 1L/kg thus we can simply add milliliters

def calculate_mixed_temperature(w1, t1, w2, t2):
    mixed_temperature = (w1 * t1 + w2 * t2) / (w1 + w2)
    return mixed_temperature


# TODO: calculate rate of cooling over time
# Using Newtons law of cooling, constant K borrowed from this article https://knowledge.carolina.com/discipline/physical-science/physics/newtons-law-of-cooling/#:~:text=Newton%27s%20law%20of%20cooling%20states,than%20in%20a%20hot%20room.
# A mini-experiment might be neccesary to obatin a more accurate K 

def rate_of_cooling(bucket_temp,time):
    room_temperature = 23.0+273.5
    bucket_temp += 273.5
    K = 0.056/60

    bucket_temp = room_temperature +(bucket_temp-room_temperature)*math.exp(-K*time)
    feedback_temperature = bucket_temp - 273.5
    return feedback_temperature

###### Simulate the cooling system. The amount of water pumped from the cooler is assumed to be dependent of a constant over time, the constant is determined experimentaly. 
###### The temperature of cooled water is also assumed constant and experimentaly determined. 

def simulate_water_pump(pumping_time, pumped_water_temp, bucket_volume, initial_bucket_temp,pumping_rate):
    pumped_water_volume = pumping_time*pumping_rate
    bucket_temp = initial_bucket_temp
    bucket_volume = bucket_volume - pumped_water_volume
    return calculate_mixed_temperature(bucket_volume,bucket_temp,pumped_water_volume,pumped_water_temp)


class PID:

    def __init__ (self,p,i,d,target,max_signal = 300):
        self.p = p
        self.i = i
        self.d = d

        self.signal = 0
        self.target = 0

        self.accumulator  = 0
        self.last_reading = 0

        self.sample_rate = 60
        self.max_signal = max_signal

       


    def set_new_target():
        self_accumulator = 0
        self.target = 0
    
    def adjust_signal(self, feedback_value):
        # Calculate the error - difference between target and feedback_value (measurement)
        error = self.target - feedback_value

        # Add error to accumulator
        self.accumulator += error

        # Calculate signal based on PID coefficients
        self.signal = self.kp * error + self.ki * self.accumulator + self.kd * (feedback_value - self.last_reading)/self.sample_rate
        
        # If caluclated signal exceeds max_signal, then set signal to max_signal value. Do this in both positive
        # and negative directions
        if self.signal > self.max_signal:
            self.signal = self.max_signal
        elif self.signal < -self.max_signal:
            self.signal = -self.max_signal

        # Save current feedback_value as last_reading attribute for use in calulating next signal.
        self.last_reading = feedback_value


simulate_water_pump()