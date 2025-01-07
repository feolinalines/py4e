# Extracting Data from JSON
#
# In this assignment you will write a Python program somewhat similar
# to http://www.py4e.com/code3/json2.py. The program will prompt for a
# URL, read the JSON data from that URL using urllib and then parse and
# extract the comment counts from the JSON data, compute the sum of the
# numbers in the file
#
# Imports
#
import urllib.request
import json
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

# Read the JSON from the URL
#
jsonData = json.loads(data)

# Debug code
#
# print(json.dumps(jsonData, indent=4))

# The comments are in their own subdictionary in the incoming
# JSON, so let's look at that
#
comments = jsonData['comments']

# Variables
#
commentsTotal = 0

# Iterate through all of the comments in the incoming JSON
#
for comment in comments :

    # Get the count from each comment
    #
    commentCount = comment['count']

    # Now convert each count to an actual integer with some error handing
    #
    try:
        commentCountInt = int(commentCount)
    except :
        "Unable to convert " + commentCount + " to an integer!"
        continue

    # Next add the converted integer to our running total
    #
    commentsTotal = commentsTotal + commentCountInt

print('Count:', len(comments))
print('Sum:', commentsTotal)