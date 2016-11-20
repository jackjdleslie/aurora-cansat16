# main.py -- put your code here!
#lumos_receiver
#########################
#        Imports        #
#########################


from pyb import UART, LED, Pin, Switch, Timer
from time import sleep
import sys


#########################
#     Prerequisites     #
#########################


#set up transceiver to receive data to from cansat
x3_pin = Pin('X3', Pin.OUT_PP)
x3_pin.low()

y4_pin = Pin('Y4', Pin.OUT_PP)
y4_pin.low()

#create lumos1 transceiver object on UART6
lumos1 = UART(6, 9600)
lumos1.write('AT+C005')
sleep(0.2)
y4_pin.high()

#create lumos2 transceiver object on UART4
lumos2 = UART(4, 9600)
lumos2.write('AT+100')
sleep(0.2)
x3_pin.high()

#feedback-pyboard on and working
green = LED(2)
green.on()

#feedback-waiting for user to press button
orange = LED(3)
orange.on()

#feedback-waiting for lumos2 to send ok command
blue = LED(4)
blue.on()

y9_pin = Pin('Y9') #Y6 had TIM12, CH1
tim = Timer(2, freq=1000)
buzzer = tim.channel(3, Timer.PWM, pin=y9_pin)


#########################
#      Sub Programs     #
#########################


def start():
	lumos1.write('start')
	#lumos2.write('start')
	orange.off()

#create switch object
big_red_button = Switch()
big_red_button.callback(start)

finished = False

for i in range(0,3):
	buzzer.pulse_width_percent(10)
	sleep(0.3)
	buzzer.pulse_width_percent(30)
	sleep(0.3)
	orange.off()
buzzer.pulse_width_percent(0)

#########################
#       Main Loop       #
#########################
 
while finished == False: #While loop that loops forever

	if lumos1.any(): 
		blue.off()
		buzzer.pulse_width_percent(50)

		data1 = lumos1.readline()
		data1 = data1.decode('utf-8')

		dataArray1 = data1.split('/')   #Split it into an array called dataArray

		data2 = lumos2.readline()
		data2 = data2.decode('utf-8')

		dataArray2 = data2.split('/')   #Split it into an array called dataArray

		if dataArray1[0] == 'end':
			green.off()
			sleep(0.5)
			green.on()
			sleep(0.5)
			green.off()
			buzzer.pulse_width_percent(0)
			finished == True
		elif len(dataArray1) >= 6:
			tagx = dataArray1[0]
			temp = dataArray1[1]
			pres = dataArray1[2]
			alti = dataArray1[3]
			lati = dataArray1[4]
			loni = dataArray1[5]
			alt2 = dataArray1[6]
		else:
			tagx = 999
			temp = 999
			pres = 999
			alti = 999
			lati = 999
			loni = 999
			alt2 = 999
		
		if len(dataArray2) >= 6:
			tagx_2 = dataArray2[0]
			temp_2 = dataArray2[1]
			pres_2 = dataArray2[2]
			alti_2 = dataArray2[3]
			lati_2 = dataArray2[4]
			loni_2 = dataArray2[5]
			alt2_2 = dataArray2[6]		
		else:
			tagx_2 = 999
			temp_2 = 999
			pres_2 = 999
			alti_2 = 999
			lati_2 = 999
			loni_2 = 999
			alt2_2 = 999	


		#data to analyse later
		#print('TAGX:{}'.format(tagx))
		data = str(temp) + '//' + str(pres) + '//' + str(alti) + '//' + str(lati) + '//' + str(loni) + '//' + str(alt2) + '//' + str(temp_2) + '//' + str(pres_2) + '//' + str(alti_2) + '//' + str(lati_2) + '//' + str(loni_2) + '//' + str(alt2_2)
		print(data)
		buzzer.pulse_width_percent(0)
		#print('PRES:{}'.format(pres))
		#print('ALTI:{}'.format(alti))
		#print('LATI:{}'.format(lati))
		#print('LONI:{}'.format(loni))

buzzer.pulse_width_percent(0)