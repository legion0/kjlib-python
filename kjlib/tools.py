import sys
import string, random

class Tools:
	ALPHA_NUMERIC_CHARS = string.ascii_letters + string.digits
	@staticmethod
	def rand_alpha_numeric(length = 1):
		seq = [random.choice(Tools.ALPHA_NUMERIC_CHARS) for _ in xrange(length)]
		return ''.join(seq)
	
def _test(args):
	for _ in xrange(20):
		print Tools.rand_alpha_numeric(20)

if __name__ == '__main__':
	_test(sys.argv[1:])
