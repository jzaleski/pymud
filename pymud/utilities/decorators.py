def classproperty(receiver):
    class WrappedProperty(object):
        def __init__(self):
            self.method_name = receiver.__name__

        def __delete__(self, obj):
            raise AttributeError('Cannot delete "%s"' % self.method_name)

        def __get__(self, obj, cls=None):
            return receiver(cls or type(obj))

        def __set__(self, obj, val):
            raise AttributeError('Cannot set "%s"' % self.method_name)
    return WrappedProperty()
