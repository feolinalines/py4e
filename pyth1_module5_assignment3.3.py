# Input value into score variable
#
scoreStr = input("Please enter score here: ")

# Basic error checking
#
try :
	scoreFloat = float(scoreStr)
except :
	print("Input score was not numeric format!")
	quit()

# Calculate the grade if the input score is in
# range, otherwise print an error message and quit
#
if scoreFloat >= 0.0 and scoreFloat <= 1.0 :

	# grade the score
	#
	if scoreFloat >= 0.9 :
		print("A")
	elif scoreFloat >= 0.8 :
		print("B")
	elif scoreFloat >= 0.7 :
		print("C")
	elif scoreFloat >= 0.6 :
		print("D")
	if scoreFloat < 0.6 :
		print("F")

else :
	print("Input score was out of range!")
	quit()