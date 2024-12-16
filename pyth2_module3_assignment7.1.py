# 7.1 Write a program that prompts for a file name, then
# opens that file and reads through the file, and print the
# contents of the file in upper case. Use the file words.txt
# to produce the output
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
file = fileHandle.read()

# Clean up the file by stripping trailing characters
#
for line in file :
	line = line.rstrip()

# Convert the contents to uppercase
#
fileUpper = file.upper()

# Print the contents of the file in uppercase
#
print(fileUpper)