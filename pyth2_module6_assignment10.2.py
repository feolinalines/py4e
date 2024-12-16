# 10.2 Write a program to read through the mbox-short.txt and figure out
# the distribution by hour of the day for each of the messages. You can
# pull the hour out from the 'From ' line by finding the time and then
# splitting the string a second time using a colon.
#
# From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
#
# Once you have accumulated the counts for each hour, print out the counts,
# sorted by hour as shown below.
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

# Count variable
hoursCountDict = dict()

# Clean up the file by stripping trailing characters
#
for fromLine in file :
	fromLine = fromLine.rstrip()

	# Look for lines starting with From
	#
	if fromLine.startswith("From ") :

		# Split each line into a list of words
		#
		fromWords = fromLine.split()

		# Parse out the time from our list of words
		#
		time = fromWords[5]

		# Parse out the hours from the time
		#
		timeList = time.split(':')
		hour     = timeList[0]

		# Populate our dictionary with key value pairs where the hour 
		# is the key and the count of that key is the value
		#
		hoursCountDict[hour] = hoursCountDict.get(hour, 0) + 1

# Now we need to sort our dictionary of tuples in hours (key) order
#
sortedHoursCountDict = dict(sorted(hoursCountDict.items()))

# debug code
#
# rint(sortedHoursCountDict)

# Finally print out the expected output in the format requested
#
# Basically fetching a list of key value tuples in the dictionary
# and just printing them out
#
for key, value in sortedHoursCountDict.items() :
	print(key, value)