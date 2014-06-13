from collections import deque
from threading import Thread

from kjlib.debugtools import verify
from kjlib.threading.background_worker import BackgroundWorker
from kjlib.threading.thread import ThreadState


class WorkersPool(BackgroundWorker):
	def __init__(self, pool_name, num_of_threads, callback):
		BackgroundWorker.__init__(self, pool_name)
		self.__pool_name = pool_name
		self.__num_of_threads = num_of_threads
		self.__callback = callback
		self.__queue = deque()
		self.__worker_threads = None
		self.__alive_threads = 0
		self.__running_threads = 0
		self.__outstanding_ops = 0

	def add(self, element):
		with self._thread_mutex:
			self.__queue.append(element)

	def start(self):
		with self._thread_mutex:
			verify(self.__worker_threads is None, "Pool %r already started" % self.__pool_name)
			self.__worker_threads = []
			self._thread_state = ThreadState.RUNNING
			for thread_index in xrange(self.__num_of_threads):
				thread_name = "%s_%d" % (self.__pool_name, thread_index)
				thread = Thread(target=self._run, name=thread_name, args=(thread_index,))
				thread.start()
				self.__worker_threads.append(thread)
			self.__alive_threads = self.__num_of_threads
			self.__running_threads = self.__num_of_threads

	def _run(self, thread_index):
		while self._checkpoint() != ThreadState.SHUTTING_DOWN:
			element, got_element = self.__try_pop()
			if (got_element):
				self.__callback(element, thread_index)
				self.__cmd_done()
		self._set_shutdown()
		thread_name = "%s_%d" % (self.__pool_name, thread_index)
		print "%r exiting" % thread_name

	def wait_for_idle(self):
		with self._thread_mutex:
			while not (self.__is_idle()):
				self._thread_control_cv.wait()

	def __is_idle(self):
		return len(self.__queue) == 0 and self.__outstanding_ops == 0

	def __wait_for_elements(self):
		while self._thread_state == ThreadState.RUNNING and len(self.__queue) == 0:
			self._thread_worker_cv.wait()

	def _checkpoint(self):
		with self._thread_mutex:
			while True:
				if self._thread_state == ThreadState.RUNNING:
					return ThreadState.RUNNING
				if self._thread_state == ThreadState.SHUTTING_DOWN:
					return ThreadState.SHUTTING_DOWN
				if self._thread_state == ThreadState.PAUSED:
					self._wait_for_new_state(self._thread_worker_cv)
					continue
				if self._thread_state == ThreadState.PAUSING:
					self.__running_threads -= 1
					if (self.__running_threads == 0):
						self._thread_state = ThreadState.PAUSED
						self._thread_control_cv.notify()
					else:
						self._wait_for_new_state(self._thread_worker_cv)
					continue
				if self._thread_state == ThreadState.RESUMING:
					self.__running_threads += 1
					if (self.__running_threads == self.__num_of_threads):
						self._thread_state = ThreadState.RUNNING
						self._thread_control_cv.notify()
					else:
						self._wait_for_new_state(self._thread_worker_cv)
					continue
				break
			verify(False, "Invalid thread state %r in checkpoint for thread from %r" % (self._thread_state, self.__pool_name))
			return self._thread_state

	def join(self):
		verify(self.__worker_threads is not None, "Pool %r not started" % self.__pool_name)
		for thread in self.__worker_threads:
			thread.join()

	def __try_pop(self):
		with self._thread_mutex:
			self.__wait_for_elements()
			if len(self.__queue) == 0:
				return None, False
			self.__outstanding_ops += 1
			return self.__queue.popleft(), True

	def __cmd_done(self):
		with self._thread_mutex:
			self.__outstanding_ops -= 1
			if self.__is_idle():
				self._thread_control_cv.notify()

	def _set_shutdown(self):
		with self._thread_mutex:
			self.__alive_threads -= 1
			if self.__alive_threads == 0:
				self._thread_state = ThreadState.SHUT_DOWN
				self._thread_control_cv.notify()
