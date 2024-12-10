# input value into hours variable
#
hoursStr = input("Please enter hours here: ")

# input value into rate variable
#
rateStr = input("Please enter rate here: ")

# convert strings to floats
#
hoursFloat = float(hoursStr)
rateFloat  = float(rateStr)

# figure out how many hours (if any) are to be paid at the higher rate
#
if hoursFloat > 40 :
	standardHoursFloat = float(40)
	overtimeHoursFloat = hoursFloat % standardHoursFloat
	overtimeRateFloat  = rateFloat * 1.5

	# debug code
	#
	# print(overtimeHoursFloat)
	# print(overtimeRateFloat)

	standardPayFloat = standardHoursFloat * rateFloat
	overtimePayFloat = overtimeHoursFloat * overtimeRateFloat

	# debug code
	#
	# print(standardPayFloat)
	# print(overtimePayFloat)

	totalPayFloat = standardPayFloat + overtimePayFloat

	# print expected output
	#
	print(totalPayFloat)

else :
	payFloat = hoursFloat * rateFloat

	# print expected output
	#
	print(payFloat)