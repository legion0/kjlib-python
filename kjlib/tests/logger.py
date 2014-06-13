from kjlib.logger import Logger
def main():
	logger = Logger.instance()
	logger.set_print_level(Logger.DEBUG3)
	logger = Logger.instance()
	
	logger.f("fatal msg"  )
	logger.e("error msg"  )
	logger.w("warning msg")
	logger.i("info msg"   )
	logger.v("verbose msg")
	logger.d("debug msg"  )
	logger.d2("debug2 msg")
	logger.d3("debug3 msg")
	
	print "All 8 levels should be printed"

if __name__ == "__main__":
	main()