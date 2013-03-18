'''
Created on Feb 17, 2013

@author: jonathanki
'''

import sys

from datetime import datetime
from datetime import timedelta
import time

class TimeTools:
	
	@staticmethod
	def getDateTimeTuple(dateTimeObj):
		return dateTimeObj.timetuple()[0:6] + (dateTimeObj.microsecond/1000,)
	
	@staticmethod
	def getNowTuple():
		return TimeTools.getDateTimeTuple(datetime.now())
	
	@staticmethod
	def formatDate(year, month, day):
		return "%04u/%02u/%02u" % (year, month, day)

	@staticmethod
	def formatTime(hours, minutes, seconds, miliseconds):
		return "%02u:%02u:%02u.%03u" % (hours, minutes, seconds, miliseconds)

	@staticmethod
	def formatDateTime(year, month, day, hours, minutes, seconds, miliseconds):
		return TimeTools.formatDate(year, month, day) + " " + TimeTools.formatTime(hours, minutes, seconds, miliseconds)
	
	@staticmethod
	def formatNow():
		return TimeTools.formatDateTime(*TimeTools.getNowTuple())
	
	@staticmethod
	def formatDelta(delta):
		neg = delta.days < 0
		days = delta.days if not neg else -delta.days
		print days
		hours, t = divmod(delta.seconds, 60*60)
		hours = hours + days * 24
		minutes, t = divmod(t, 60)
		seconds = t
		miliseconds = delta.microseconds / 1000
		string = TimeTools.formatTime(hours, minutes, seconds, miliseconds)
		if neg:
			return "-" + string
		return string

class Timer():
	def __init__(self):
		self.reset()
	
	def start(self):
		self.startTime = datetime.now()
	
	def end(self):
		end = datetime.now()
		self.total = self.total + (end - self.startTime)
		return self.total
	
	def reset(self):
		self.total = timedelta()
		

def main(args):
	print TimeTools.formatNow()
	timer = Timer()
	timer.start()
	time.sleep(1.1009)
	print 0-(timer.end()*-1)
	print -timer.end()
	print TimeTools.formatDelta(timer.end())
	print TimeTools.formatNow()
	timer.reset()
	print repr(timer)
	timer.start()
	time.sleep(2.1009)
	print TimeTools.formatDelta(timer.end())
	print TimeTools.formatNow()

if __name__ == '__main__':
	main(sys.argv[1:])