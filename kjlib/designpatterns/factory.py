from kjlib.mycollections import OrderedSet

_classes = OrderedSet()

def register(class_):
    _classes.add(class_)

def new(arg):
    for class_ in _classes:
        if class_.accept(arg):
            return class_(arg)
