import signal,os

__author__ = 'Aung Naing Oo'

class SignallingApi(object):
	#Class written to signal and timeout
	def handler(self,signum, frame):
		print "Signal handler called with signal", signum
		raise IOError("Couldn't open device!")

	def signalling(self):
		signal.signal(signal.SIGALRM,self.handler)

	def signalTime(self, time):
		signal.alarm(time)