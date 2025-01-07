# Scraping Numbers from HTML using BeautifulSoup In this assignment you will write
# a Python program similar to http://www.py4e.com/code3/urllink2.py. The program will
# use urllib to read the HTML from the data
#
# Imports
#
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
#
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Prompt for the URL
#
url = input('Enter URL: ')

# Open the URL
#
html = urlopen(url, context=ctx).read()

# Use BeautifulSoup to parse the incoming html
#
soup = BeautifulSoup(html, "html.parser")

# Variables
#
commentsTotalList  = list()
commentsTotal      = 0

# Retrieve all of the span tags
#
tags = soup('span')
for tag in tags:

    # Get the numbers (NavigableString format) from the span tag
    #
    commentsNavigableString = tag.contents[0]

    # Convert the BeautifulSoup NavigableStrings to strings
    #
    commentsString = str(commentsNavigableString)

    # Append the strings to a list
    #
    commentsTotalList.append(commentsString)

# Next we want to interate through our list of numbers
# in string format, convert them to actual integers and
# add them up
#
for commentsString in commentsTotalList : 

    # First convert to integer with some error handing
    #
    try:
        commentsInt = int(commentsString)
    except :
        "Unable to convert " + commentsString + " to an integer!"
        continue

    # Next add the converted integer to our running total
    #
    commentsTotal = commentsTotal + commentsInt

# Print out our final total which is the assignment answer
#
print(commentsTotal)
