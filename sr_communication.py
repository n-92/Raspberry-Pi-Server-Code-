import serial
import time
from signalling import *

__author__ = "Aung Naing Oo"

class SerialAPI(object):
	def __init__(self):
		self.port = '/dev/ttyACM0'
		self.baud_rate = 9600
		self.ser = None
		self.signalObject = SignallingApi()

	def connect_serial(self):
		"""
		Initialize serial socket
		"""
		try:
			self.signalObject.signalling()
			self.signalObject.signalTime(15)	#wait for 5 seconds before timeout

			self.ser = serial.Serial(self.port, self.baud_rate)
			print "Serial link connected"
			self.signalObject.signalTime(0)	#disarm the signal
		except Exception, e:
			# print "Error (Serial): %s " % str(e)
			print "Error: Serial connection not established. Try reconnecting the serial cable and/or restart the pi"
			#pass	#let it go through


	def close_sr_socket(self):
		if (self.ser):
			self.ser.close()
			print "Closing serial socket"


	def write_to_serial(self, msg):
		"""
		Write to arduino
		"""
		try:
			self.ser.write(msg)
			#print "Write to arduino: %s " % msg
		except AttributeError:
			print "Error in serial comm. No value to be written. Check connection!"
			#pass	#let it go through

	def read_from_serial(self):
		"""
		Read from arduino

		Waits until data is received from arduino
		"""
		try:
			received_data = self.ser.readline()
			print "Received from arduino: %s " % received_data
			return received_data
		except AttributeError:
			print "Error in serial comm. No value received. Check connection!"
			#pass #let it go through
