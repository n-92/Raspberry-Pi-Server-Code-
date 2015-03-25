import socket
import sys
from signalling import *

__author__ = "Aung Naing Oo"

class PcAPI(object):

	def __init__(self):
		self.ip_address = "192.168.17.18" # Connecting to IP address of MDPGrp17
		self.port = 8089
		self.conn = None
		self.client = None
		self.addr = None
		self.pc_is_connect = False
		self.signalObject = SignallingApi()

	def close_pc_socket(self):
		"""
		Close socket connections
		"""
		if self.conn:
			self.conn.close()
			print "Closing server socket"
		if self.client:
			self.client.close()
			print "Closing client socket"
		self.pc_is_connect = False

	def pc_is_connected(self):
		"""
		Check status of connection to PC
		"""
		return self.pc_is_connect

	def init_pc_comm(self):
		"""
		Initiate PC connection over TCP
		"""
		# Create a TCP/IP socket
		try:
			self.signalObject.signalling()
			self.signalObject.signalTime(15)	#wait for 5 seconds before timeout
			
			self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.conn.bind((self.ip_address, self.port))
			self.conn.listen(1)		#Listen for incoming connections
			print "Listening for incoming connections from PC..."
			self.client, self.addr = self.conn.accept()
			print "Connected! Connection address: ", self.addr
			self.pc_is_connect = True
			self.signalObject.signalTime(0)	#disarm the signal

		except Exception, e: 	#socket.error:
			print "Error: %s" % str(e)
			print "Try again in a few seconds"


	def write_to_PC(self, message):
		"""
		Write message to PC
		"""
		try:
			self.client.sendto(message, self.addr)
			# print "Sent [%s] to PC" % message
		except TypeError:
			print "Error: Null value cannot be sent"
		#	pass #let it go through

	def read_from_PC(self):
		"""
		Read incoming message from PC
		"""
		try:
			pc_data = self.client.recv(2048)
			# print "Read [%s] from PC" %pc_data
			return pc_data
		except Exception, e:
			print "Error: %s " % str(e)
			print "Value not read from PC"
			pass #let it go through	
