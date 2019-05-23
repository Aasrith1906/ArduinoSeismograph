import matplotlib.pyplot as plt 
import socket
from random import randint
import serial
from drawnow import *
import numpy as np

data_array_acceleration_x = []
data_array_acceleration_y = []
data_array_acceleration_z = []

data_array_displacement_x = []
data_array_displacement_y = []
data_array_displacement_z = []

time_interval = 50/1000

arduinoData = serial.Serial('COM4', 115200) 
plt.ion() 

def PlotGraph():
                                
    plt.title('Live Streaming Sensor Data')      
    plt.grid(True)                                  
    plt.ylabel('Displacement')                            
    plt.plot(data_array_displacement_x, 'r' )    
    plt.plot(data_array_displacement_y,'g')
    plt.plot(data_array_displacement_z,'b')  
    plt.legend(['displacement x axis','displacement y axis','displacement z axis'],loc='upper left')
                      


def Displacement(acceleration,time_interval):

	displacement = (acceleration*(time_interval*time_interval))/2  #double indefinate integration 

	''' a = dv/dt 
		a.dt = dv
		∫a.dt = ∫dv
		
		at = v

		at = ds/dt 
		at.dt = ds 
		∫at.dt = ∫ds
		at²/2 = s
	'''

	return displacement

def ConvertArray(acceleration_array,time_interval):

    data_array = []

    for i in acceleration_array:

        data_array.append(Displacement(i,time_interval))

    return data_array


while True: 
    while (arduinoData.inWaiting()==0): 
        pass 
    arduinoString = arduinoData.readline() 

    arduinoData.flush()

    arduinoString = arduinoString.decode('utf-8',errors='ignore')

    arduinoString_formatted = arduinoString.split(',')
    
    formatted_string_float_array = []

    for i in arduinoString_formatted:

        formatted_string_float_array.append(float(i))
        print(i)

    ACX = formatted_string_float_array[0] 
    ACY = formatted_string_float_array[1]
    ACZ = formatted_string_float_array[2]

    print(ACX)
    print(ACY)
    print(ACZ)     

    data_array_acceleration_x.append(ACX)                     
    data_array_acceleration_y.append(ACY)
    data_array_acceleration_z.append(ACZ)  

    data_array_displacement_x = ConvertArray(data_array_acceleration_x,time_interval)     
    data_array_displacement_y = ConvertArray(data_array_acceleration_y,time_interval) 
    data_array_displacement_z = ConvertArray(data_array_acceleration_z,time_interval)
    
    drawnow(PlotGraph)    

    plt.pause(0.001) 


















































