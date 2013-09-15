from kjlib.mycollections import OrderedSet

_classes = OrderedSet()

def register(_class):
    _classes.add(_class)

def new(arg):
    for _class in _classes:
        if _class.accept(arg):
            return _class(arg)
