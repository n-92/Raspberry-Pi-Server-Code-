import sys
import time
import Queue
import threading
from bt_communication import *
from sr_communication import *
from pc_communication import *


__author__ = 'Aung Naing Oo'

class Main(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

#		self.pc_thread = PcAPI()
		self.bt_thread = BluetoothAPI()
		self.sr_thread = SerialAPI()

		# Initialize the connections
#		self.pc_thread.init_pc_comm()
		self.bt_thread.connect_bluetooth()
		self.sr_thread.connect_serial()
		time.sleep(1)	# wait for 1 secs before starting


	# PC Functions

	def writePC(self, msg_to_pc):
		"""
		Write to PC. Invoke write_to_PC()
		"""
		self.pc_thread.write_to_PC(msg_to_pc)
		#print "WritePC: Sent to PC: %s" % msg_to_pc

	def readPC(self):
		"""
		Read from PC. Invoke read_from_PC() and send 
		data according to header
		"""
		print "Inside readPC"
		while True:
			read_pc_msg = self.pc_thread.read_from_PC()

			# Check header for destination and strip out first char
			
			if(read_pc_msg[0].lower() == 'b'):		# send to bluetooth
				self.writeBT(read_pc_msg[1:])		# strip the header
				print "value received from PC: %s" % read_pc_msg[1:]

			elif(read_pc_msg[0].lower() == 'a'):	# send to arduino
				self.writeSR(read_pc_msg[1:])		# strip the header
				print "value received from PC: %s" % read_pc_msg[1:]

			else:
				print "incorrect header received from PC: [%s]" % read_pc_msg[0]
			#	time.sleep(1)	


	# Android/BT functions

	def writeBT(self, msg_to_bt):
		"""
		Write to BT. Invoke write_to_bt()
		"""
		self.bt_thread.write_to_bt(msg_to_bt)
		#print "Value sent to Android: %s" % msg_to_bt

	def readBT(self):
		"""
		Read from BT. Invoke read_from_bt() and send
		data to PC
		"""
		print "Inside readBT"
		while True:
			read_bt_msg = self.bt_thread.read_from_bt()

			# Check header and send data to PC
			if(read_bt_msg[0].lower() == 'p'):	# send to PC
				self.writePC(read_bt_msg[1:])	# strip the header
				print "Value received from Bluetooth: %s" % read_bt_msg[1:]

	#### this case can be commented out ####
			elif(read_bt_msg[0].lower() == 'a'):	# send to SR
			 	self.writeSR(read_bt_msg[1:])		# strip the header
			 	print "value received from BT: %s" % read_bt_msg[1:]

			else:
				print "incorrect header received from BT: [%s]" % read_bt_msg[0]
			#	time.sleep(1)

	# Serial Comm functions

	def writeSR(self, msg_to_sr):
		"""
		Write to Serial. Invoke write_to_serial()
		"""
		self.sr_thread.write_to_serial(msg_to_sr)
		#print "Value sent to arduino: %s" % msg_to_sr

	def readSR(self):
		"""
		Read from SR. Invoke read_from_serial() and send
		data to PC
		"""
		print "Inside readSR"
		while True:
			#print "Inside readSR"
			read_sr_msg = self.sr_thread.read_from_serial()

			# Write straight to Bluetooth and PC without any checking
			self.writeBT(read_sr_msg)
		#	self.writePC(read_sr_msg)
            #print "Value received from arduino: %s" % read_sr_msg
            #time.sleep(1)

	# Remember to comment this out and use direct communication with PC


	# 		# Check header and send data to PC
	# 		if(read_sr_msg[0].lower() == 'p'):	# send to PC
	# 			self.writePC(read_sr_msg[1:])	# strip the header
	# 			print "value written to PC from SR: %s" % read_sr_msg[1:]

	# 	 	this can be commented out 
	# 		elif(read_bt_msg[0].lower() == 'b'):	# send to BT
	# 			self.writeBT(read_sr_msg[1:])		# strip the header
	# 			print "value written to BT from SR: %s" % read_sr_msg[1:]

	# 		else:
	# 			print "incorrect header received from SR: [%s]" % read_sr_msg[0]
	# 			time.sleep(1)

		
	def initialize_threads(self):

		# PC read and write thread
#		rt_pc = threading.Thread(target = self.readPC, name = "pc_read_thread")
		# print "created rt_pc"
#		wt_pc = threading.Thread(target = self.writePC, args = ("",), name = "pc_write_thread")
		# print "created wt_pc"

		# Bluetooth (BT) read and write thread
		rt_bt = threading.Thread(target = self.readBT, name = "bt_read_thread")
		# print "created rt_bt"
		wt_bt = threading.Thread(target = self.writeBT, args = ("",), name = "bt_write_thread")
		# print "created wt_bt"

		# Serial (SR) read and write thread
		rt_sr = threading.Thread(target = self.readSR, name = "sr_read_thread")
		# print "created rt_sr"
		wt_sr = threading.Thread(target = self.writeSR, args = ("",), name = "sr_write_thread")
		# print "created wt_sr"


		# Set threads as daemons
#		rt_pc.daemon = True
#		wt_pc.daemon = True

		rt_bt.daemon = True
		wt_bt.daemon = True

		rt_sr.daemon = True
		wt_sr.daemon = True

		print "All threads initialized successfully"


		# Start Threads
#		rt_pc.start()
#		wt_pc.start()

		rt_bt.start()
		wt_bt.start()

		rt_sr.start()
		wt_sr.start()
	
		# print "Starting rt and wt threads"


	def close_all_sockets(self):
		"""
		Close all sockets
		"""
		pc_thread.close_all_pc_sockets()
		bt_thread.close_all_bt_sockets()
		sr_thread.close_all_sr_sockets()
		print "end threads"

	def keep_main_alive(self):
		"""
		function = Sleep for 500 ms and wake up.
		Keep Repeating function 
		until Ctrl+C is used to kill
		the main thread.
		"""
		while True:
			#suspend the thread  
			time.sleep(0.5)


if __name__ == "__main__":
	mainThread = Main()
	mainThread.initialize_threads()
	mainThread.keep_main_alive()
	mainThread.close_all_sockets()	
