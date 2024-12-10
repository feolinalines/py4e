# 6.5 Write code using find() and string slicing (see section 6.10)
# to extract the number at the end of the line below. Convert the
# extracted value to a floating point number and print it out.

text = "X-DSPAM-Confidence:    0.8475"

# Find the index where the number starts in the string
#
startIndex = text.find("0")

# Calculate the length of the string. We can use that
# as our end index
#
endIndex = len(text)

# Extract the value, convert to float, and print out
# the expected output
#
# extractedString = text[5:10]
extractedString = text[startIndex:endIndex]

try :
	extractedFloat = float(extractedString)
	print(extractedFloat)
except :
	print("Extracted value cannot be converted to a float!")

# Debug code
#
# print(startIndex)
# print(endIndex)
# print(extractedString)
# print(extractedFloat)