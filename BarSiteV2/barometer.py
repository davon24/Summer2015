import serial
import time 
import glob
import sys
import datetime
from numpy import *
from ftplib import FTP

ftp = FTP('phoenix.mdacc.tmc.edu') #Declares variables that are used for FTP transfer
FTPUser = 'omitted'
FTPPass = 'omitted'

value = input("Enter Mercury Barometer Reading: ")
admin = raw_input("Enter your name: ")
calibration = raw_input('Do you want to add calibration?: ').lower()
if calibration not in ('yes','y','no','n'): #Checks to see if a valid answer to the question was given
	print "Did not enter valid calibration response."
	sys.exit()

while True:
	print "Program is starting"
	# We are setting the initial conditions for the serial port
	ser = serial.Serial(3) #the number placed in the parenthesis is the COM number minus 1

				   #####
	ser.baudrate = 9600 #
	ser.bytesize = 8    #
	ser.stopbits = 1    #  #  #  # These are the inital conditions for the serial port
	ser.timeout = 5     #
				   ######

	if ser.isOpen() == False: # Opens the port if it isn't already
	    ser.open
	for i in '*0100P3\r\n': # Gives the command to the barometer with some delay to give time for the command to be read 
	    ser.write(i)
	    time.sleep(0.1)

	# Saves the time and date that the measurement took place
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%m/%d/%Y %H:%M'
		)
	raw_reading = ser.readline()[5:12] # Save the electric barometer's reading as 'x' and then closes the port
	ser.close()
	 


	try:  
		data = genfromtxt("file.txt", skiprows = 2, dtype=None, unpack=True) #assigns the contents of the calibration file to a variable
	except Exception:
		data = ""

	slope = 0
	offset = 0
	i = 0

############################
	try:					####
		if len(data) > 10:		######
			for row in data:	   		####
			    slope += row[1]/row[0] 	    ##
			    i+=1 							#####
			slope /= i 								######
															###
			for row in data:									####
			    offset += row[1] - slope*row[0]						 #
			offset /= i 											  #     This block of code goes through the calibration calculations when there are more than
			cal_reading = round(slope*float(raw_reading) + offset,2)  #  	a certain number of data points.
		else:														  #
			cal_reading = raw_reading								# The try and exception are to filter out the errors when there  are no data points
	except Exception:											  #
		cal_reading = raw_reading								#
##############################################################
	
	if calibration in ("yes","y"):
		display_reading = cal_reading
		cal = 'Calibration was added. The slope and offset are %.4f and %.3e respectively' %(slope,offset)
	else:
		display_reading = raw_reading
		cal = 'Calibration was not added.'
	print "Electric Barometer Reading: %s" %(display_reading)
	 
	 
	# Opens and writes the readings into a file

	if value == 0:		# If a mercury reading was not given 
		with open("lonereadings.txt", 'a') as l:
			l.write('%s    %s    %s\n' %(raw_reading, cal_reading, st))
			l.close
		with open('index.html', 'r') as page: 
	    # read a list of lines into site
			site = page.readlines()
	 									#####
		site[20] = str(display_reading)+'\n' # Writes to the website
		site[23] = str(st)+'\n'              # If the html code is changed you will need to change this part
		site[27] = admin+'.'+'\n'            # The numbers in the brackets are the lines of the html code minus 1
		site[28] = cal+'\n'                  #
										#####
		# and write everything back
		with open('index.html','w') as file:
			file.writelines(site)


	else: 		# If a mercury reading is given
		with open("file.txt", "a") as f:
			f.write('%s     %s     %s      %s\n' %(raw_reading, value, cal_reading, st)) # write the new line before
			f.close()
	 
		with open("lonereadings.txt", 'a') as l:
			l.write('%s    %s    %s\n' %(raw_reading, cal_reading, st))
			l.close		 
		with open('index.html', 'r') as page:
		    # read a list of lines into site
			site = page.readlines()
                                          ####
		site[20] = str(display_reading)+'\n'  #
		site[23] = str(st)+'\n'                #
		site[27] = admin+'.'+'\n'              #  This part will also need to be changed if html is changed
		site[28] = cal+'\n'                    #
		site[37] = str(value)+'\n'             #
		site[43] = str(display_reading)+'\n'   #
		site[49] = str(st)+'\n'                #
		                                  ####
		# and write everything back
		with open('index.html','w') as file:
		    file.writelines(site)

                                   
	ftp = FTP('phoenix.mdacc.tmc.edu') 
	ftp.login(FTPUser, FTPPass)          
	ftp.cwd('data2/adelie/htdocs/barometer')

	index = open('index.html', 'rb')          
	ftp.storbinary('STOR index.html', index)
	index.close()
	ftp.quit()
	print "current cycle finished"
	value = 0 
	time.sleep(300) # Program sleeps for 5 minutes
