# Name:		Abdullah Alfouzan
# Date:		03/30/2013
# Class:	CPSC 471-03
# Quiz 3
# Socket Programming. 
# This is a Client side of a network application that will send file to the server. please include your file name and path on your
# argument.


# Client

import sys, socket
import os

# The fixed size of the size message
SIZE_MSG_SIZE = 100

# ----------------------------------------
# Sends the data over the specified socket
# @param sock - the socket to use
# @param data - the data to send
# ----------------------------------------
def sendData(sock, data):
	
	# The number of bytes successfully sent in one shot
	numSent = 0
	
	# The total number of bytes transmitted thus far
	totalNumSent = 0

	# Keep sending until all data is sent
	while totalNumSent != len(data):
		
		# Send as much as you can
		numSent = sock.send(data[totalNumSent:])
		
		# Update the total number of bytes sent	
		totalNumSent += numSent
	

# -----------------------------------------------------
# Sends the size message to the server
# @param sock - the socket to send the message over
# @param size - the size to send
# ----------------------------------------------------
def sendSize(sock, size):

	# Convert the size to string
	sizeStr = str(size)
	
	# Keep adding leading 0's until our message
	# size is SIZE_MSG_SIZE
	while len(sizeStr) < SIZE_MSG_SIZE:
		sizeStr = "0" + sizeStr
	
	# Send the message	
	sendData(sock, sizeStr)

# The command line IP
IP = sys.argv[1]

# The server port
PORT = sys.argv[2]

# The file name to send
FILE = sys.argv[3]

# Sending file name.
cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Using TCP
cs.connect((IP, int(PORT)))

# Send the length of the file name
sendSize(cs, len(FILE))

# Send the file name
sendData(cs, FILE)

# Get the file size 
fileSize = os.path.getsize(FILE)

# Send the file size
sendSize(cs, fileSize)

# Open the file for reading
fp = open(FILE, "rb")

# The total number of bytes sent
totalNumSent = 0

# How many chars to transmit at the same time
chunkSize = 100

# Keep sending file contents until all is sent
while totalNumSent < fileSize:

	# Read as much as you can
	data = fp.read(chunkSize)

	# Send the data
	sendData(cs, data)
	
	# Update the data count
	totalNumSent += len(data)	

	

# Close the file and tear down the TCP connection
fp.close()
cs.close()
