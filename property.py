from __future__ import unicode_literals, print_function
import timeit


def create_property(name, creator):

    def fget(obj):
        value = None
        if hasattr(obj, name):
            value = getattr(obj, name)
        
        if value is None:
            value = creator(obj)
            setattr(obj, name, value)
        
        return value
    
    def fset(obj, value):
        setattr(obj, name, value)
        
    return property(fget, fset)


def create_property1(self, name, default_value):

    prop_name = '__{}'.format(name)

    def fget(obj):
        return getattr(obj, prop_name)
    
    def fset(obj, value):
        setattr(obj, prop_name, value)
        
    setattr(self, prop_name, default_value)
    return property(fget, fset)


def create_property2(self, name, creator, default_value):

    prop_name = '__{}'.format(name)

    def fget(obj):
        value = getattr(obj, prop_name)
        if value is None:
            value = creator(obj)
            setattr(obj, prop_name)
        return value
    
    def fset(obj, value):
        setattr(obj, prop_name, value)
        
    setattr(self, prop_name, default_value)
    return property(fget, fset)


class Klass(object):

    @property
    def property1(self): return self.__private
    
    @property1.setter
    def property1(self, value): self.__private = value
    
    def __init__(self):
        self.public = None
        self.__private = None
        self.property4 = create_property1(self, 'property4', 0)
        self.property5 = create_property2(self, 'property5', self.__create_property5, None)
    
    def __get_property2(self):
        return self.__private
    
    def __set_property2(self, value):
        self.__private = value
    
    def __create_property3(self):
        return 1
    
    def __create_property5(self):
        return 1

    property2 = property(__get_property2, __set_property2)
    property3 = create_property('__property3', __create_property3)


if __name__ == '__main__':
    count = 10000

    def test0():
        k = Klass()
        data = [None] * count
        for i in xrange(count):
            k.public = i
            data[i] = k.public

    def test1():
        k = Klass()
        data = [None] * count
        for i in xrange(count):
            k.property1 = i
            data[i] = k.property1
    
    def test2():
        k = Klass()
        data = [None] * count
        for i in xrange(count):
            k.property2 = i
            data[i] = k.property2

    def test3():
        k = Klass()
        data = [None] * count
        for i in xrange(count):
            k.property3 = i
            data[i] = k.property3

    def test4():
        k = Klass()
        data = [None] * count
        for i in xrange(count):
            k.property4 = i
            data[i] = k.property4

    def test5():
        k = Klass()
        data = [None] * count
        for i in xrange(count):
            k.property5 = i
            data[i] = k.property5
    
    # a = Klass()
    # a.property1 = 1
    # a.property4 = 1
    # for key in dir(a):
    #     if hasattr(a, key): print(key, getattr(a, key))
    #     else: print(key)

    iterations = 10000
    print(timeit.timeit(test0, number=iterations))
    print(timeit.timeit(test1, number=iterations))
    print(timeit.timeit(test2, number=iterations))
    print(timeit.timeit(test3, number=iterations))
    print(timeit.timeit(test4, number=iterations))
    print(timeit.timeit(test5, number=iterations))
