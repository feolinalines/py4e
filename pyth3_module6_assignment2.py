# Calling a JSON API
#
# In this assignment you will write a Python program somewhat similar
# to http://www.py4e.com/code3/opengeo.py. The program will prompt
# for a location, contact a web service and retrieve JSON for the web
# service and parse that data, and retrieve the first plus_code from
# the JSON. An Open Location Code is a textual identifier that is
# another form of address based on the location of the address.
#
# Imports
#
import urllib.request, urllib.parse
import json, ssl

# Heavily rate limited proxy of https://www.geoapify.com/ api
#
serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?'

# Ignore SSL certificate errors
#
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:

    # Prompt for the location to lookup
    #
    address = input('Enter location: ')
    if len(address) < 1: break

    address = address.strip()
    parms = dict()
    parms['q'] = address

    url = serviceurl + urllib.parse.urlencode(parms)

    # Get the url handle, decode it, and print the character count
    #
    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    # Try to parse the JSON 
    #
    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'features' not in js:
        print('==== Download error ===')
        print(data)
        break

    if len(js['features']) == 0:
        print('==== Object not found ====')
        print(data)
        break

    # Debug code
    #
    # print(json.dumps(js, indent=4))

    # Get the plus_code from the incoming JSON and print it out
    #
    plusCode = js['features'][0]['properties']['plus_code']
    print('Plus Code ', plusCode)