from kjlib.designpatterns import factory
import re

class A:
    def __init__(self, arg):
        print "init A with %s" % arg
    @staticmethod
    def accept(arg):
        return isinstance(arg, basestring) and re.match(r"^A", arg)
factory.register(A)

class B:
    def __init__(self, arg):
        print "init B with %s" % arg
    @staticmethod
    def accept(arg):
        return isinstance(arg, basestring) and re.match(r"^B", arg)
factory.register(B)

if __name__ == "__main__":
    obj1 = factory.new("Alice")
    obj2 = factory.new("Bob")
    print obj1
    print obj2
