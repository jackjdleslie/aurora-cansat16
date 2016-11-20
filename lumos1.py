# main.py -- put your code here!
#lumos1
#########################
#        Imports        #
#########################


from bmp180 import BMP180
from pyb import UART, LED, Pin, Timer, I2C, Servo
from time import sleep
from micropyGPS import MicropyGPS


#########################
#     Prerequisites     #
#########################

bmp = True

#create BMP180 object
i2c = I2C(2)
i2c.init(I2C.MASTER)
scan = i2c.scan()

if len(scan) > 0:
	bmp180 = BMP180('Y')
	bmp180.oversample_sett = 3 #0=low accuracy, 3=high accuracy
	bmp180.baseline = 102800 #pressure at main sea level
else:
	bmp = False

#create GPS object
my_gps = MicropyGPS()

#servo setup
servo = Servo(1)

#set up transceiver to send data to ground station
y4_pin = Pin('Y4', Pin.OUT_PP)
y4_pin.high()

#create buzzer pin
y6_pin = Pin('Y6') #Y6 had TIM12, CH1
tim = Timer(1, freq=1000)
buzzer = tim.channel(1, Timer.PWM, pin=y6_pin)

#create transceiver object on UART6
hc12 = UART(6, 9600)

#create gps object on UART1
uart = UART(1, 9600)

#feedback-pyboard on and working
green = LED(2)
green.on()

#feedback-received start command
blue = LED(4)

#feedback-waiting for user to press button
orange = LED(3)
orange.on()

#boolean variable to manage main loop
finished = False

#########################
#       Main Loop       #
#########################

servo.angle(40, 5000)

while finished == False:
	#if start command is received
	#if hc12.any():
		#do servo motor stuff

	for i in range(0,3):
		buzzer.pulse_width_percent(10)
		sleep(0.3)
		buzzer.pulse_width_percent(20)
		sleep(0.3)
		orange.off()
	buzzer.pulse_width_percent(0)

	sleep(45)

	#X second loop, get data every half second and write to backup.csv, and also transmit to ground station
	for tag in range(1,2000):

		buzzer.pulse_width_percent(20)
		
		#if data available from bmp180
		if bmp == True:
			temp = bmp180.temperature
			pres = bmp180.pressure
			alt = bmp180.altitude
		else:
			temp = 0
			pres = 0
			alt = 0

		#if there is gps data to be read then get sentence
		if uart.any():
			my_sentence = uart.readline()
			my_sentence = my_sentence.decode('utf-8')
			my_sentence = my_sentence[:-2]

		for x in my_sentence:
			my_gps.update(x)

		latitude = my_gps.latitude_string()
		longitude = my_gps.longitude_string()
		timestamp = my_gps.timestamp
		alt2 = my_gps.altitude

		#open backup.csv to write data to, write to it, then close it
		backup = open('/sd/backup.csv', 'a')
		backup.write('{},{},{},{},{},{},{},{}\n'.format(tag,timestamp,temp,pres,alt,latitude,longitude,alt2))
		backup.close()

		data = str(tag) + '/' + str(temp) + '/' + str(pres) + '/' + str(alt) + '/' + str(latitude) + '/' + str(longitude) + '/' + str(alt2) #concatenate data with slashes

		hc12.write(data) #write data over UART4 to transmit to ground station

		buzzer.pulse_width_percent(0)
		sleep(1) #sleep for a second to buffer

	finished = True
	sleep(2)
	hc12.write('end')


#########################
#      End Program      #
#########################

for i in range(0,3):
	buzzer.pulse_width_percent(50)
	sleep(0.3)
	buzzer.pulse_width_percent(60)
	sleep(0.3)
	orange.off()
buzzer.pulse_width_percent(0)
	
green.off()
blue.off()