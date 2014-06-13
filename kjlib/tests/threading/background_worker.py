from time import sleep

from kjlib.threading.background_worker import BackgroundWorker

class MyBGWorker(BackgroundWorker):
	def _inner_action(self):
		print "1"
		sleep(0.3)

background_worker = MyBGWorker("some bg workzer")
print "starting"
background_worker.start()
print "started"
sleep(1)
print "pausing"
background_worker.pause()
print "paused"
sleep(1)
print "resuming"
background_worker.resume()
print "resumed"
sleep(1)
print "shutting down"
background_worker.shutdown()
print "shut down"
