from kjlib.mycollections import OrderedSet

_classes = OrderedSet()

def register(class_):
	_classes.add(class_)

def new(name, *args, **kwargs):
	for class_ in _classes:
		if class_.accept(name):
			return class_(*args, **kwargs)
	return None
