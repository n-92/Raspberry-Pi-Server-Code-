from bluetooth import *
from signalling import *

__author__ = 'Aung Naing Oo'

class BluetoothAPI(object):

	def __init__(self):
		"""
		Connect to Galaxy s5 bluetooth
		RFCOMM port: 7
		MAC address: no need 
		"""
		self.server_socket = None
		self.client_socket = None
		self.bt_is_connected = False
		self.signalObject = SignallingApi()

	def close_bt_socket(self):
		"""
		Close socket connections
		"""
		if self.client_socket:
			self.client_socket.close()
			print "Closing client socket"
		if self.server_socket:
			self.server_socket.close()
			print "Closing server socket"
		self.bt_is_connected = False


	def bt_is_connect(self):
		"""
		Check status of Bluetooth connection
		"""
		return self.bt_is_connected


	def connect_bluetooth(self):
		"""
		Connect to the s5
		"""
		# Creating the server socket and bind to port		
		btport = 4
		try:
			self.signalObject.signalling()
			self.signalObject.signalTime(15)	#wait for 5 seconds before timeout
			#print "--signall---..---"
			self.server_socket = BluetoothSocket( RFCOMM )
			self.server_socket.bind(("", btport))
			self.server_socket.listen(1)	# Listen for requests
			self.port = self.server_socket.getsockname()[1]
			uuid = "00001101-0000-1000-8000-00805F9B34FB"

			advertise_service( self.server_socket, "BluetoothServer",
			                   service_id = uuid,
			                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
			                   profiles = [ SERIAL_PORT_PROFILE ],
								)
			print "Waiting for connection on RFCOMM channel %d" % self.port
			# Accept requests
			self.client_socket, client_address = self.server_socket.accept()
			print "Accepted connection from ", client_address
			self.bt_is_connected = True
			self.signalObject.signalTime(0)	#disarm the signal
			
		except Exception, e:
			#print "Error: %s" %str(e)
			print "Bluetooth Connection can't be established"
			# self.close_bt_socket()
			pass  #let it go through


	def write_to_bt(self,message):
		"""
		Write message to s5
		"""
		#print "Enter message to send: "
		#message = raw_input()
		try:
			self.client_socket.send(str(message))
			#print "sending: ", message
		except BluetoothError:
			print "Bluetooth Error. Connection reset by peer"
			self.connect_bluetooth()	# Reestablish connection
			
		#print "quit write()"
		
	def read_from_bt(self):
		"""
		Read incoming message from Nexus
		"""
		try:
			msg = self.client_socket.recv(2048)
			#print "Received: %s " % msg
			return msg
		except BluetoothError:
			print "Bluetooth Error. Connection reset by peer. Trying to connect..."
			self.connect_bluetooth()	# Reestablish connection
