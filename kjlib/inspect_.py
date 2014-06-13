import inspect

from kjlib.debugtools import verify


def get_calling_module_name(extra_frames_up=0):
# 	__import_verify()
	frames_up = 2 + extra_frames_up
	stack = inspect.stack()
	verify(frames_up < len(stack), "There are less than 2+%r frames in the stack" % extra_frames_up)
	frame = stack[frames_up]
	module = inspect.getmodule(frame[0])
	module_name = module.__name__
	return module_name