from .timetools import format_delta, format_datetime
from datetime import datetime, timedelta
import math
import random
import sys
import time

class JobControl:

	def __init__(self, total_jobs=1):
		self._total_jobs = total_jobs
		self._finished_jobs = 0
		self._average_time = None
		self._last_time = self._now()
# 		self.N = min(10, math.ceil(float(self._total_jobs)/10))
# 		self.N = min(1000, self._total_jobs)
		n = max(1, math.ceil(float(self._total_jobs) / 10))
		self._alpha = float(2) / (n + 1)
		self._alpha_changed = False
		self._last_update_percent = None

	def done(self, amount=1):
		self._finished_jobs = self._finished_jobs + amount
		diff = float(self._now() - self._last_time) / amount

		if self.get_percent() >= 1 and not self._alpha_changed:
			self._alpha_changed = True
			self._alpha = float(2) / (self._total_jobs + 1)
		if self._average_time is None:
			self._average_time = diff
		else:
			self._average_time = self._alpha * diff + (1 - self._alpha) * self._average_time
		self._last_time = self._now()

	def _now(self):
		return int(time.time() * 1000)

	def get_progress(self):
		return float(self._finished_jobs) / self._total_jobs

	def get_progress_formatted(self):
		return "{}/{}".format(self._finished_jobs, self._total_jobs)

	def get_percent(self):
		return int(self.get_progress() * 100)

	def get_percent_formatted(self):
		return "%u%%" % self.get_percent()

	def get_time_remaining(self):
		seconds_remaining = int(self._average_time * (self._total_jobs - self._finished_jobs))
		return timedelta(seconds=seconds_remaining)

	def get_eta(self):
		return datetime.now() + self.get_time_remaining()

	def get_time_remaining_formatted(self):
		return format_delta(self.get_time_remaining())

	def get_eta_formatted(self):
		return format_datetime(self.get_eta())

	def get_formatted(self):
		return "{} ({}) ETA:{}".format(self.get_percent_formatted(), self.get_progress_formatted(), self.get_eta_formatted())

	def get_formatted_if_updated(self):
		percent = self.get_percent()
		if percent != self._last_update_percent:
			self._last_update_percent = percent
			return self.get_formatted()
		else:
			return None

def _test():
	N = 100
	DELAY = 100
	RAND = 99
	jc = JobControl(N)
	for _ in xrange(N):
		milis = DELAY + (random.random() - 0.5) * RAND
		time.sleep(milis / 1000)
		jc.done()
		# print jc.get_percent_formatted()
		print jc.get_time_remaining_formatted()

if __name__ == '__main__':
	_test(sys.argv[1:])
