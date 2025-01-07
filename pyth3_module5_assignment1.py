# Extracting Data from XML
# In this assignment you will write a Python program somewhat similar
# to http://www.py4e.com/code3/xml3.py. The program will prompt for a
# URL, read the XML data from that URL using urllib and then parse and
# extract the comment counts from the XML data, compute the sum of the
# numbers in the file.
#
# Imports
#
import urllib.request
import xml.etree.ElementTree as ET
import ssl

# Ignore SSL certificate errors
#
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Prompt for the URL with some basic error handling 
#
url = input('Enter URL : ')

try :
    print('Retrieving', url)
    data = urllib.request.urlopen(url, context=ctx).read()
    print('Retrieved',len(data),'characters')
except :
    print("Unable to open input url: " + url )
    quit()

# Convert the data we retrived into an element tree
#
tree = ET.fromstring(data)

# Variables
#
commentsList  = list()
commentsTotal = 0

# Find all the counts in the xml
#
foundCounts = tree.findall('.//count')

for foundCount in foundCounts:

    # Add the count to our list
    #
    commentsList.append(foundCount.text)

# Debug code
#
# print(commentsList)

# Next we want to interate through our list of numbers
# in string format, convert them to actual integers and
# add them up
#
for commentString in commentsList : 

    # First convert to integer with some error handing
    #
    try:
        commentInt = int(commentString)
    except :
        "Unable to convert " + commentString + " to an integer!"
        continue

    # Next add the converted integer to our running total
    #
    commentsTotal = commentsTotal + commentInt

print('Count:', len(commentsList))
print('Sum:', commentsTotal)