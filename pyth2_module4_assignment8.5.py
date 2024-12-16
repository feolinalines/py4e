# 8.5 Open the file mbox-short.txt and read it line by line. When you
# find a line that starts with 'From ' like the following line:
# From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
# You will parse the From line using split() and print out the second
# word in the line (i.e. the entire address of the person who sent the
# message). Then print out a count at the end.
# Hint: make sure not to include the lines that start with 'From:'.
# Also look at the last line of the sample output to see how to print
# the count.
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
emailAddressCount = 0

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
		emailAddress      = fromWords[1]
		emailAddressCount = emailAddressCount + 1

		print(emailAddress)

# Finally print out the count in the format requested
#
emailAddressCountString = str(emailAddressCount)

print("There were " + emailAddressCountString + " lines in the file with From as the first word")