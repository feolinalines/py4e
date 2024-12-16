# 9.4 Write a program to read through the mbox-short.txt and figure
# out who has sent the greatest number of mail messages. The program
# looks for 'From ' lines and takes the second word of those lines as
# the person who sent the mail. The program creates a Python dictionary
# that maps the sender's mail address to a count of the number of
# times they appear in the file. After the dictionary is produced, the
# program reads through the dictionary using a maximum loop to find the
# most prolific committer.
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
emailAddressCountDict = dict()

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

		# Parse out the second word from our list
		#
		emailAddress  = fromWords[1]

		# debug code
		#
		# print(emailAddress)

		# Populate our dictionary with key value pairs where the email 
		# address is the key and the count of that key appearing in the
		# file is the value
		#
		emailAddressCountDict[emailAddress] = emailAddressCountDict.get(emailAddress, 0) + 1

		# debug code
		#
		# print(emailAddressCountDict)

# Now we need to loop through our dictionary to figure out which email address
# appears the most in the data
#
modeKeyString   = None
modeValueString = None

for key, countValue in emailAddressCountDict.items() :
	if modeValueString is None or countValue > modeValueString :
		modeKeyString   = key
		modeValueString = countValue

# Finally print out the expected output in the format requested
#
print(modeKeyString, modeValueString)