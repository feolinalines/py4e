# 7.2 Write a program that prompts for a file name, then
# opens that file and reads through the file, looking for
# lines of the form: X-DSPAM-Confidence: 0.8475
# Count these lines and extract the floating point values
# from each of the lines and compute the average of those
# values and produce an output as shown below. Do not use
# the sum() function or a variable named sum in your solution.
#
# Prompt user for the file name to open
#
fileName = input("Please enter file name: ")

# Fetch the handle for the file name and return an error
# if it doesn't exist
#
try :
	fileHandle = open(fileName, 'r')
except :
	print("Filename " + fileName + " does not exist!")
	quit()

# Read the contents of the file referenced by the handle
#
file = fileHandle.readlines()

# Variables to calculate the spam confidence average
#
spamConfidenceCount = 0
spamConfidenceTotal = 0.0

# Clean up the file by stripping trailing characters
#
for line in file :
	line = line.rstrip()

	# Look for lines starting with X-DSPAM-Confidence:
	#
	if line.startswith("X-DSPAM-Confidence:") :

		# Parse out the floats that are in string format
		#
		spamConfidenceStartIndex = line.find(" ") + 1
		spamConfidenceEndIndex   = len(line)
		spamConfidenceString     = line[spamConfidenceStartIndex:spamConfidenceEndIndex]

		# Hopefully we have a string that we can
		# convert to a float, if so let's add it to 
		# running total
		#
		try :
			spamConfidenceFloat = float(spamConfidenceString)
			spamConfidenceTotal = spamConfidenceTotal + spamConfidenceFloat
			spamConfidenceCount = spamConfidenceCount + 1

			# Debug code
			#
			# print(spamConfidenceFloat)
			# print(spamConfidenceTotal)
			# print(spamConfidenceCount)
		except :
			print("Unable to convert value: " + spamConfidenceString + " to a float!")
			continue

# Now print out the expected output which should be an 
# average of our spamConfidenceTotal
#
spamConfidenceAverage = spamConfidenceTotal / spamConfidenceCount
print("Average spam confidence: " + str(spamConfidenceAverage))