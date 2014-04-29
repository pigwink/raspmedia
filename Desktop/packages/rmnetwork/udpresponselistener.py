import socket, select
import interpreter

from constants import *

def stopListening():
	global observers
	print "Stopping UDP Broadcast Listening routine..."
	global sock, wait
	wait = False
	# notify observers that listening is stopped
	for observer in observers:
		if observer[0] == OBS_STOP:
			observer[1]()

	# clear observer list
	observers = []
	print "Done!"

def startListening():
	global observers
	print "UDP Broadcast Listener starting listening routine..."
	global sock, wait
	if not sock:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(('', 60007))
		
	wait = True

	print "INSIDE BROADCASTLISTENER:"
	print "Waiting for incoming data..."
	while wait:	
		#result = select.select([sock],[],[])
		#print "Result from select - processing..."
		#rec, address = result[0][0].recvfrom(1024)
		rec, address = sock.recvfrom(1024)
		result, response = interpreter.interpret(rec)
		if result == INTERPRETER_SERVER_REQUEST:
			print "Server request response - length: ", len(rec)
			print ":".join("{:02x}".format(ord(c)) for c in rec)
			print "Server address: ", str(address)
			print ""
			for observer in observers:
				if observer[0] == OBS_HOST_SEARCH:
					observer[1](address)
		elif result == INTERPRETER_FILELIST_REQUEST:
			print "File list received!"
			print response
			for observer in observers:
				if observer[0] == OBS_FILE_LIST:
					observer[1](address, response)

def registerObserver(observer):
	global observers
	if not observer in observers:
		observers.append(observer)


def removeObserver(observer):
	global observers
	if observer in observers:
		observers.remove(observer)


sock = None
wait = True
# observers for receiving file list
observers = []
# observers to be notified when listener stops
stopObservers = []