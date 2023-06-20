"""
Scenario: 
    Cooling system continusly pumps, the pumping rate depends on the PID-readings
    Algae is fed to the mussels based on the model
    Every gathered data is transmitted to the API
    All the collected data must be stored to the board as well as a backup

    Error handling: If the connection is cut off/ resume and try again later
"""
import time
from data_storage import*
from cooling_system import*
from mmqt_connection import*

#First we connect to the WIFI
try:
    connect_wifi("DESKTOP-EF6HHDI 2656","v8064,R8")
    print("Connection established")
except Exception as e:
    pass 



#Define Adafruit credentials and initiating the clients
username = "ibsen95"
io_key = "aio_GRPH09dbrJoEVToCPbYen8YgBtlB"

#Feeds 
temperature_feed = MQTTConnect(username,io_key,"Temperature")
OD_feed = MQTTConnect(username,io_key,"OD")

#Subscriptions
temp_control = MQTTConnect(username,io_key,"setpoint")
feeding_control = MQTTConnect(username,io_key,"feeding")


# Callback functions for dashboard control ------------------------------------------------------------------------------------------------------------------------------------------------

def cb_setpoint(msg):
    cooling_sys.update(int(msg))

def cb_feeding(msg):
    print("Feeding")


temp_control.set_callback(cb_setpoint)
feeding_control.set_callback(cb_feeding)


#------------------------------------------------------------------------------------------------------------------------------------------------

#Creating data_storage objects for each measurment
filenames = ["Temperature-readings","OD-readings","Feeding-times"]
temperature_storage = data_storage(filenames[0])
OD_storage = data_storage(filenames[1])
feeding_storage = data_storage(filenames[2])
cooling_sys = Cooling_System(17.45)

#--------------------------------------------------------------------------------------------------------------------------------------------------

i=1

while True:
    print("Cycle {}".format(i))
    #TODO logic
    #Check for commands from dashboard
    temp_control.check_msg() 
    print("Temp_control check")

    current_temperature = cooling_sys.average_readings()
    print("Temperature readings")
    publish(current_temperature,"Temperature",username,temperature_feed)
    temperature_storage.save_to_file(current_temperature)
    cooling_sys.update_parameter(current_temperature)
    print("Control signal: {}".format(cooling_sys.control_signal))
    print(current_temperature)
    i+=1

    #TODO
    #Algae feeding 
    """ if feeding_time:
        feed()
        OD = od.get_reading 
        OD_storage.save_to_file(OD)
        feeding_storage.save_to_file(time.time())
        
        try:
            publsh(OD)b
        except Exception e:
            pass

    if circulation_time:
        flow.circulate()

        try:
            publish(flow)
            export_to_df
        except Exception e:
            pass
"""





