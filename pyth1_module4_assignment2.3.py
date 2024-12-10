# input value into hours variable
#
hoursStr = input("Please enter hours here: ")

# input value into rate variable
#
rateStr = input("Please enter rate here: ")

# convert strings to floats
#
hoursFloat = float(hoursStr)
rateFloat  = float(rateStr)

# debug code
#
# print("hoursFloat: ", hoursFloat)
# print("rateFloat: ", rateFloat)

# calculate pay
#
payFloat = hoursFloat * rateFloat

# print expected output
#
print("Pay:",  payFloat)