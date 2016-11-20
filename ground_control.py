#ground_control.py
#########################
#        Imports        #
#########################


import serial 
import matplotlib.pyplot as plt 
from drawnow import *
from time import time, sleep


#########################
#     Prerequisites     #
#########################

tempC= []
pressure=[]
altM=[]
raw = serial.Serial('/dev/tty.usbmodem1412', 9600) 
#plt.ion() #Tell matplotlib you want interactive mode to plot live data
#plt3.ion()
cnt=0


#########################
#      Sub Programs     #
#########################
 

def makeFig1(): 
    plt.ylim(0,40)
    plt.xlabel('Altitude1 (m)')
    plt.grid(True)
    plt.ylabel('Temp1 C')
    plt.plot(tempC, 'ro-', label='Degrees C')
    plt.legend(loc='upper left')
    plt2=plt.twinx()
    plt.ylim(80000,110000)
    plt2.plot(pressure, 'b^-', label='Pressure (Pa)')
    plt2.set_ylabel('Pressure1 (Pa)')
    plt2.ticklabel_format(useOffset=False)
    plt2.legend(loc='upper right')

def makeFig2():
    plt3.ylim(0,40)
    plt3.xlabel('Altitude (m)')
    plt3.grid(True)
    plt3.ylabel('Temp C')
    plt3.plot(tempC, 'ro-', label='Degrees C')
    plt3.legend(loc='upper left')
    plt4=plt.twinx()
    plt4.ylim(80000,110000)
    plt4.plot(pressure, 'b^-', label='Pressure (Pa)')
    plt4.set_ylabel('Pressrue (Pa)')
    plt4.ticklabel_format(useOffset=False)
    plt4.legend(loc='upper right')


#########################
#       Main Loop       #
#########################

start = time()
while True:
    while (raw.inWaiting()==0):
        pass
    data = raw.readline() 
    dataArray = data.split('//')

    temp = float( dataArray[0])
    P =    float( dataArray[1])
    alt = float( dataArray[2])
    lati = str(dataArray[3])
    loni = str(dataArray[4])
    alt2 = float(dataArray[5])

    temp_2 = float( dataArray[6])
    P_2 =    float( dataArray[7])
    alt_2 = float( dataArray[8])
    lati_2 = str(dataArray[9])
    loni_2 = str(dataArray[10])
    alt2_2 = float(dataArray[11])
    #write data to lumos1 file
    lumos1 = open('lumos1.csv', 'a')
    lumos1.write('{},{},{},{},{},{}\n'.format(str(dataArray[0]),str(dataArray[1]),str(dataArray[2]),str(dataArray[3]),str(dataArray[4]),str(dataArray[5])))
    lumos1.close()

    #write data to lumos2 file
    lumos2 = open('lumos2.csv', 'a')
    lumos2.write('{},{},{},{},{},{}\n'.format(str(dataArray[6]),str(dataArray[7]),str(dataArray[8]),str(dataArray[9]),str(dataArray[10]),str(dataArray[11])))
    lumos2.close()
    
    tempC.append(temp)
    pressure.append(P)
    altM.append(alt)

    drawnow(makeFig1)
    plt.pause(.000001)
    cnt=cnt+1

    end = time()
    if (end - start) >= 90:
        plt.ioff()
        plt.show()
        break
    elif(cnt>=100):
        plt.ioff()
        plt.show()
        break
    sleep(0.5)