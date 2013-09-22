'''
Created on Feb 17, 2013

@author: jonathanki
'''

import sys

from datetime import datetime
from datetime import timedelta
import time

def format_datetime(datetime_instance = None, format_string = "%Y/%m/%d %H:%M:%S"):
	if datetime_instance is None:
		datetime_instance = datetime.now()
	return datetime_instance.strftime(format_string)

def format_timestamp(datetime_instance = None, format_string = "%Y%m%d_%H%M%S"):
	return format_datetime(datetime_instance, format_string)
	
def format_delta(delta):
	abs_delta = abs(delta)
	neg = abs_delta > delta
	delta = abs_delta
	days = delta.days
	hours, t = divmod(delta.seconds, 60*60)
	hours += days*24
	minutes, seconds = divmod(t, 60)
	miliseconds = delta.microseconds / 1000
	res_str = "%02u:%02u:%02u.%03u" %(hours, minutes, seconds, miliseconds)
	if neg:
		res_str = "-" + res_str
	return res_str

class Timer():
	def __init__(self):
		self.reset()
	
	def start(self):
		self.start_time = datetime.now()
	
	def end(self):
		end = datetime.now()
		self.total = self.total + (end - self.start_time)
		return self.total
	
	def reset(self):
		self.total = timedelta()
		

def main(args):
	print format_datetime()
	timer = Timer()
	timer.start()
	time.sleep(1.1009)
	print 0-(timer.end()*-1)
	print -timer.end()
	print format_delta(timer.end())
	print format_datetime()
	timer.reset()
	print repr(timer)
	timer.start()
	time.sleep(2.1009)
	print format_delta(timer.end())
	print format_datetime()

if __name__ == '__main__':
	main(sys.argv[1:])
