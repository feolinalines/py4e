# 8.4 Open the file romeo.txt and read it line by line. For each
# line, split the line into a list of words using the split() method.
# The program should build a list of words. For each word on each
# line check to see if the word is already in the list and if not
# append it to the list. When the program completes, sort and print
# the resulting words in python sort() order as shown in the desired
# output.
#
# Fetch the handle for the romeo.txt and return an error
# if it doesn't exist
#
romeoFileName = 'romeo.txt'

try :
	romeoFileHandle = open(romeoFileName, 'r')
except :
	print("Filename " + romeoFileName + " does not exist!")
	quit()

# Read the contents of the file referenced by the handle
#
romeoFile = romeoFileHandle.readlines()

# Create an empty list to store unique words from the file
#
romeoList = list()

# Clean up the file by stripping trailing characters
#
for romeoLine in romeoFile :
	romeoLine = romeoLine.rstrip()

	# Split each line into a list of words
	#
	romeoWords = romeoLine.split()

	# Debug code
	#
	# print(romeoWords)

	# Check each word to see if it's in our unique
	# word list. If it's not in there, then append it
	#
	for romeoWord in romeoWords :
		if romeoWord not in romeoList :
			romeoList.append(romeoWord)

# Sort the list
#
romeoList.sort()

# Print out the expected output
#
print(romeoList)