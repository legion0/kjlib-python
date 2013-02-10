import sys
import string, random

class Tools:
	ALPHA_NUMERIC_CHARS = string.ascii_letters + string.digits
	@staticmethod
	def randomAlphaNumeric(length = 1):
		seq = [random.choice(Tools.ALPHA_NUMERIC_CHARS) for _ in xrange(length)]
		return ''.join(seq)
	
def main(args):
	print Tools.randomAlphaNumeric(1000)

if __name__ == '__main__':
	main(sys.argv[1:])