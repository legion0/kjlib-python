from time import sleep

from kjlib.threading.workers_pool import WorkersPool
from kjlib.printers import format_cli_title

def main():
	test1()
	test2()
	test3()

def test3():
	print format_cli_title("test 3")
	
	def printer(element, thread_index):
		sleep(0.5)
		print "%r:%r" % (thread_index, element)
	
	workers_pool = WorkersPool("workerz3", 2, printer)
	
	for i in xrange(100):
		workers_pool.add(i)
	
	print "starting"
	workers_pool.start()
	print "started"
	sleep(2)
	print "pausing"
	workers_pool.pause()
	print "paused"
	sleep(2)
	print "shutting down"
	workers_pool.shutdown()
	print "shut down"

def test2():
	print format_cli_title("test 2")

	def printer(element, thread_index):
		sleep(0.5)
		print "%r:%r" % (thread_index, element)
	
	workers_pool = WorkersPool("workerz2", 2, printer)
	
	for i in xrange(10):
		workers_pool.add(i)
	
	print "starting"
	workers_pool.start()
	print "started"
	print "waiting"
	workers_pool.wait_for_idle()
	print "done"
	print "shutting down"
	workers_pool.shutdown()
	print "shut down"

def test1():
	print format_cli_title("test 1")

	def printer(element, thread_index):
		sleep(0.5)
		print "%r:%r" % (thread_index, element)
	
	workers_pool = WorkersPool("workerz1", 2, printer)
	
	for i in xrange(100):
		workers_pool.add(i)
	
	print "starting"
	workers_pool.start()
	print "started"
	sleep(2)
	print "pausing"
	workers_pool.pause()
	print "paused"
	sleep(2)
	print "resuming"
	workers_pool.resume()
	print "resumed"
	sleep(2)
	print "shutting down"
	workers_pool.shutdown()
	print "shut down"

if __name__ == "__main__":
	main()
