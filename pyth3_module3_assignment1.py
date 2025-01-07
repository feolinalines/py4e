# You are to retrieve the following document using the HTTP protocol in a way
# that you can examine the HTTP Response headers.
#
# http://data.pr4e.org/intro-short.txt
#
# Modify the socket1.py program to retrieve the above URL and print out the
# headers and data. Make sure to change the code to retrieve the above URL - the
# values are different for each URL.
#

# Import socket module
#
import socket

# Initialize a socket object
#
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Use the socket to connect to the pr4e web server
#
mysocket.connect(('data.pr4e.org', 80))

# Send a GET request to the server for the intro-short.txt document
#
cmd = 'GET http://data.pr4e.org/intro-short.txt HTTP/1.0\r\n\r\n'.encode()
mysocket.send(cmd)

# Print out the RESPONSE
#
while True:
    data = mysocket.recv(512)
    if len(data) < 1:
        break
    print(data.decode(),end='')

# Finally close the socket gracefully
#
mysocket.close()
