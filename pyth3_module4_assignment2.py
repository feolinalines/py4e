# Following Links in Python
# In this assignment you will write a Python program that expands on
# http://www.py4e.com/code3/urllinks.py. The program will use urllib
# to read the HTML from the data files below, extract the href= vaues
# from the anchor tags, scan for a tag that is in a particular position
# relative to the first name in the list, follow that link and repeat
# the process a number of times and report the last name you find.
#
# Imports
#
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
#
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Prompt for the URL, Count, and Position with some
# basic error handling 
#
url = input('Enter URL      : ')

try :
    html = urllib.request.urlopen(url, context=ctx).read()
except :
    print("Unable to open input url: " + url )
    quit()

count = input('Enter Count    : ')

try :
    countInt = int(count)
except :
    print("Unable to convert input value: " + count + " to a numnber!")
    quit()

position = input('Enter Position : ')

try :
    positionInt = int(position)
except :
    print("Unable to convert input value: " + position + " to a numnber!")
    quit()

# First print the initial URL
#
print("Retrieving: " + url)

# Use a while loop to retrieve the URL at the input position
# as many times as the count specifies and print out the result
#
i = 0
while i < countInt :

    # Open the URL
    #
    html = urllib.request.urlopen(url, context=ctx).read()

    # Use BeautifulSoup to parse the incoming html
    #
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all of the anchor tags
    #
    tags = soup('a')

    # Get the tag at the position specified in the list
    #
    tag = tags[positionInt - 1]
    url = tag.get('href', None)
    print("Retrieving: " + url)

    # Increment the count
    #
    i += 1