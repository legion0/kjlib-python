import inspect
import __main__
import os

from kjlib.debugtools import verify


def get_calling_module_name(extra_frames_up=0, module=None):
	if module is None:
		frames_up = 2 + extra_frames_up
		stack = inspect.stack()
		verify(frames_up < len(stack), "There are less than 2+%r frames in the stack" % extra_frames_up)
		frame = stack[frames_up]
		module = inspect.getmodule(frame[0])
	module_name = getattr(module, "__name__")
	if module_name == "__main__":
		if hasattr(__main__, "__file__"):
			module_name = os.path.splitext(os.path.basename(getattr(__main__, "__file__")))[0]
		else:
			module_name = "python_interpreter"
	return module_name
