# Function takes two arguments, hours and rate
# in string format and converts them to floats.
# Then calculates pay, paying an overtime rate
# for anything over 40 hours.
#
def computepay(hoursStr, rateStr) :

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
		return totalPayFloat

	else :
		payFloat = hoursFloat * rateFloat

		# print expected output
		#
		return payFloat

# Input value into hours variable
#
hoursInput = input("Please enter hours here: ")

# Input value into rate variable
#
rateInput = input("Please enter rate here: ")

# Call our function and then print the returned value
#
computedPay = computepay(hoursInput, rateInput)
print("Pay", computedPay)