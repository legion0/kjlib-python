import time
import math

import random

class JobControl:

	def __init__(self, totalJobs = 1):
		self.totalJobs = totalJobs
		self.jobs = 0
		self.avgTime = None
		self.lastTime = self.__now()
#		self.N = min(10, math.ceil(float(self.totalJobs)/10))
#		self.N = min(1000, self.totalJobs)
		n = max(1,math.ceil(float(self.totalJobs)/10))
		self.a = float(2)/(n+1)
		self.alphaChanged = False

	def jobDone(self, amount = 1):
		self.jobs = self.jobs + amount
		diff = float(self.__now() - self.lastTime) / amount

		if self.getProgressPercent() >= 1 and not self.alphaChanged:
			self.alphaChanged = True
			self.a = float(2)/(self.totalJobs+1)
		if self.avgTime is None:
			self.avgTime = diff
		else:
			self.avgTime = self.a * diff + (1-self.a) * self.avgTime
		self.lastTime = self.__now()

	def __now(self):
		return int(time.time()*1000)

	def getProgress(self):
		return float(self.jobs) / self.totalJobs

	def getProgressPercent(self):
		return int(self.getProgress()*100)

	def getProgressFormatted(self):
		return str(self.getProgressPercent()) + "%"

	def getETA(self):
		return int(self.avgTime * (self.totalJobs - self.jobs))

	def getETAFormatted(self):
		t = float(self.getETA())
		msecs = math.floor(t%1000)
		t -= msecs
		secs = math.floor(t/1000)
		mins = math.floor(secs / 60)
		secs -= mins*60
		hours = math.floor(mins / 60)
		mins -= hours * 60
		return "%02u:%02u:%02u.%03u" % (hours, mins, secs, msecs)

	def getFormatted(self):
		progressStr = "{}/{}".format(self.jobs, self.totalJobs)
		return "{} ({}) ETA:{}".format(progressStr, self.getProgressFormatted(), self.getETAFormatted())

def test():
	N = 100
	DELAY = 100
	RAND = 99
	jc = JobControl(N)
	for i in xrange(N):
		milis = DELAY + (random.random()-0.5)*RAND
		time.sleep(milis/1000)
		jc.jobDone()
		#print jc.getProgressFormatted()
		print jc.getETAFormatted()

if __name__ == '__main__':
	test()