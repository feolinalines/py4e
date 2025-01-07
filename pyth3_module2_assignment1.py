# In this assignment you will read through and parse a file with
# text and numbers. You will extract all the numbers in the file
# and compute the sum of the numbers.
#

# Import regex module
#
import re

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

# Variables
#
numbersList  = list()
numbersTotal = 0

# Clean up the file by stripping trailing characters
#
for line in file :
	line = line.rstrip()

	# Look for integer values in each line
	#
	lineResults = re.findall('[0-9]+', line)

	# If we find any integers on the line then add them to 
	# our list of numbers
	#
	if any(lineResults) :
		numbersList = numbersList + lineResults

# Next we want to interate through our list of numbers
# in string format, convert them to actual integers and
# add them up
#
for numberString in numbersList : 

	# First convert to integer with some error handing
	#
	try:
		number = int(numberString)
	except :
		"Unable to convert " + numberString + " to an integer!"
		continue

	# Next add the converted integer to our running total
	#
	numbersTotal = numbersTotal + number

# Print out our final total which is the assignment answer
#
print(numbersTotal)