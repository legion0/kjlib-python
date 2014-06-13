import threading

from kjlib.debugtools import verify
from kjlib.threading.thread import ThreadState


class BackgroundWorker(object):

	__SHUTDOWN_STATES = (ThreadState.RUNNING, ThreadState.PAUSED)

	def __init__(self, thread_name):
		self._current_thread = None
		self._thread_name = thread_name
		self._thread_state = ThreadState.NOT_STARTED
		self._thread_mutex = threading.Lock()
		self._thread_control_cv = threading.Condition(self._thread_mutex)
		self._thread_worker_cv = threading.Condition(self._thread_mutex)

	def start(self):
		with self._thread_mutex:
			verify(self._current_thread is None, "Thread %r already started" % self._thread_name)
			self._current_thread = threading.Thread(target=self._run, name=self._thread_name)
			self._thread_state = ThreadState.RUNNING
			self._current_thread.start()

	def join(self):
		verify(self._current_thread is not None, "Thread %r cannot be joined because it is not started" % self._thread_name)
		self._current_thread.join()

	def _wait_for_new_state(self, cv):
		current_state = self._thread_state
		while self._thread_state == current_state:
			cv.wait()

	def pause(self):
		with self._thread_mutex:
			verify(self._thread_state == ThreadState.RUNNING, "Thread %r is not RUNNING" % self._thread_name)
			self._thread_state = ThreadState.PAUSING
			self._thread_worker_cv.notify_all()
			self._wait_for_new_state(self._thread_control_cv)
			verify(self._thread_state == ThreadState.PAUSED, "Thread %r is not PAUSED after pause" % self._thread_name)

	def resume(self):
		with self._thread_mutex:
			verify(self._thread_state == ThreadState.PAUSED, "Thread %r is not paused" % self._thread_name)
			self._thread_state = ThreadState.RESUMING
			self._thread_worker_cv.notify_all()
			self._wait_for_new_state(self._thread_control_cv)
			verify(self._thread_state == ThreadState.RUNNING, "Thread %r is not RUNNING after resume" % self._thread_name)

	def shutdown(self):
		with self._thread_mutex:
			verify(self._thread_state in BackgroundWorker.__SHUTDOWN_STATES, "Thread %r is not in a legal shutdown state" % self._thread_name)
			self._thread_state = ThreadState.SHUTTING_DOWN
			self._thread_worker_cv.notify_all()
			self._wait_for_new_state(self._thread_control_cv)
			verify(self._thread_state == ThreadState.SHUT_DOWN, "Thread %r is not SHUT_DOWN after shut down" % self._thread_name)
		self.join()

	# returns RUNNING or SHUTTING_DOWN
	def _checkpoint(self):
		with self._thread_mutex:
			while True:
				if (self._thread_state == ThreadState.PAUSING):
					self._thread_state = ThreadState.PAUSED
					self._thread_control_cv.notify()
					self._wait_for_new_state(self._thread_worker_cv)
					continue
				if (self._thread_state == ThreadState.RESUMING):
					self._thread_state = ThreadState.RUNNING
					self._thread_control_cv.notify()
					break
				if (self._thread_state == ThreadState.SHUTTING_DOWN):
					return ThreadState.SHUTTING_DOWN
				break
			verify(self._thread_state == ThreadState.RUNNING, "Thread %r is not RUNNING after checkpoint" % self._thread_name)
			return self._thread_state

	def _run(self):
		while self._checkpoint() != ThreadState.SHUTTING_DOWN:
			self._inner_action()
		self._set_shutdown()

	def _set_shutdown(self):
		with self._thread_mutex:
			self._thread_state = ThreadState.SHUT_DOWN
			self._thread_control_cv.notify()
