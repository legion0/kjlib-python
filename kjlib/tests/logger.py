from kjlib.logger import Logger


logger = Logger.instance()
logger.set_print_level(Logger.DEBUG3)
logger = Logger.instance()

logger.f("FATAL")
logger.e("ERROR")
logger.w("WARNING")
logger.i("INFO")
logger.v("VERBOSE")
logger.d("DEBUG")
logger.d2("DEBUG2")
logger.d3("DEBUG3")

print "All 8 levels should be printed"