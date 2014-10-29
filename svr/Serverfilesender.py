# Name:		Abdullah Alfouzan
# Date:		03/30/2013
# Class:	CPSC 471-03
# Quiz 3
# Socket Programming. 
# This is a Server side of a network application that will receive file from the client.


import sys, socket
import os
#------------------------------------------------------------------------

# The command line port number
PORT = sys.argv[1]


# The fixed size of the size message
SIZE_MSG_SIZE = 100

# ------------------------------------------
# Receives data from the socket
# @param sock - the socket to receive from
# @param size - how much to receive
# @return - the data received
# ------------------------------------------
def recvData(sock, size):
	
	# The total number of bytes recieved
	totalNumRecv = 0
	
	# The data received
	data = ""
	
	# Keep receiving until you get everything
	while totalNumRecv < size:
		
		# Get as much data as you can
		data += sock.recv(size)
		
		# Get the total data length
		totalNumRecv = len(data)	
	
	return data	

# --------------------------------------------------
# Receives the size
# @param sock - the socket to recieve the size from
# @return - the size of the coming data
# --------------------------------------------------
def recvSize(sock):
	
	# Get the size string
	strSize = recvData(sock, SIZE_MSG_SIZE)
	
	print strSize	
	
	# Convert to integer and return
	return int(strSize)


# Create a TCP socket
listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
listenSock.bind(('127.0.0.1', int(PORT)))

# Listen for incoming connections
listenSock.listen(1)


# Keep serving the clients forever
while True:

	# Accept a connection
	clientSock, addr = listenSock.accept()
		
	# Get the length of the forecoming file name
	fileNameLen = recvSize(clientSock)
	
	# Receive the file name
	fileName = recvData(clientSock, fileNameLen)	
	
	# Get the file size
	fileSize = recvSize(clientSock)
	
	print fileName
	
	# Open the file for writing
	fp = open(fileName, "wb")
	
	# The total number of bytes received
	totalNumRecv = 0
	
	# The chunk size to receive
	chunkSize = 100
	
	# Keep receiving the file conent
	while totalNumRecv < fileSize:
		
		# How many bytes to receive
		numToRecv = 0
		
		# If the last chunk (if it's the last chunk) is
		# >= the remaining bytes than go ahead and receive
		# chunkSize bytes	
		if fileSize - totalNumRecv >= chunkSize:
			numToRecv = chunkSize
		# Otherwise, simply receive the remaining bytes
		else:
			numToRecv = fileSize - totalNumRecv
		
		# Receive the data
		data = recvData(clientSock, numToRecv)	
		
		# Write the data to the file
		fp.write(data)
		
		# Update the count
		totalNumRecv += len(data)

	# Close the file	
	fp.close()
	
	# Tear down the connection
	clientSock.close()
