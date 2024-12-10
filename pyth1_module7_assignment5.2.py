# Tracking varables initialized as None 
#
largestInt  = None
smallestInt = None

while True :
	# Input value into inputStr variable
	#
	inputStr = input("Please enter a number here: ")

	# If the user enters done then break out of the loop
	#
	if inputStr == "done" :
		break

	# If we're not done then do some error checking on the input
	# value to make sure it's a number
	#
	try :
		inputInt = int(inputStr)
	except :
		print("Invalid input")
		continue

	# If we're here we have a valid number so we can start keeping
	# track of which is the largest and smallest
	#
	if largestInt is None :
		largestInt = inputInt
	elif inputInt > largestInt :
		largestInt = inputInt

	if smallestInt is None :
		smallestInt = inputInt
	elif inputInt < smallestInt :
		smallestInt = inputInt

	# debug code
	#
	# print(inputInt)
	# print("Maximum is", largestInt)
	# print("Minimum is", smallestInt)
	
# We're done so print the expected output
#
print("Maximum is", largestInt)
print("Minimum is", smallestInt)