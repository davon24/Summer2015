import sys
calibration = raw_input('Do you want to add calibration?: ').lower()
if calibration not in ('yes','y','no','n'):
	print "Did not enter valid calibration response."
	
print calibration