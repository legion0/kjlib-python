#!/usr/bin/env python2
'''
Created on Jul 5, 2014

@author: legion
'''

import os
import sys
# import time
import argparse

_BLOCK_SIZE = 64 * 1024
# _BLOCK_SIZE = 85

def _parse_args():
	parser = argparse.ArgumentParser(description='Smart copy, read and copy if different')
	parser.add_argument("src_path", metavar="<src-path>")
	parser.add_argument("dst_path", metavar="<dst-path>")

	args = parser.parse_args()

	return args

def main():
# 	sys.argv = [sys.argv[0], "/home/legion/README.md", "/home/legion/README.md.2"]
	args = _parse_args()
# 	print args
# 	exit()
	copy(args.src_path, args.dst_path)

def copy(src_path, dst_path):
	src_size = os.path.getsize(src_path)
# 	print "src_size=%r" % src_size
	dst_file = open(dst_path, "ab+")

	if src_size > 0:
		src_file = open(src_path, "rb")
		started_copy = False
		size_in_blocks = src_size / _BLOCK_SIZE
		if size_in_blocks * _BLOCK_SIZE != src_size:
			size_in_blocks += 1
		for block_offset in xrange(size_in_blocks):
			offset = block_offset * _BLOCK_SIZE
# 			print "reading %r bytes from offset %r" % (_BLOCK_SIZE, src_file.tell())
			src_data = src_file.read(_BLOCK_SIZE)
# 			print repr(src_data)
			if started_copy:
# 				print "writing %r bytes to offset %r" % (len(src_data), dst_file.tell())
				dst_file.write(src_data)
			else:
				dst_data = dst_file.read(_BLOCK_SIZE)
# 				print repr(dst_data)
				if src_data != dst_data:
					started_copy = True
					matching_size = max(src_file.tell() - len(src_data), 0)
					print "matching_size=%r" % matching_size
					dst_file.seek(matching_size)
					dst_file.truncate(matching_size)
# 					print "writing %r bytes to offset %r" % (len(src_data), dst_file.tell())
					dst_file.write(src_data)
			_print_progress(offset, src_size, offset > 0)

	dst_file.seek(0, os.SEEK_END)
	if dst_file.tell() > src_size:
		dst_file.truncate(src_size)

	src_file.close()
	dst_file.close()

	_print_progress(src_size, src_size, True)
	print ""

def _print_progress(offset, size, not_first_round):
	percent = 100.0 * offset / size
	msg = "%06.2f%%" % percent
	if not_first_round:
		msg = '\r' + msg
	sys.stdout.write(msg)
	sys.stdout.flush()
# 	time.sleep(1)

if __name__ == "__main__":
	main()
