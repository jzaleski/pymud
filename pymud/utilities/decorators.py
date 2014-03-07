def class_property(method):

    class descriptor(object):

        def __init__(self):
            self.attribute_error = \
                AttributeError('Property "%s" is read-only' % method.__name__)

        def __get__(self, obj, cls=None):
            return method(cls or type(obj))

        def __set__(self, obj, val):
            raise self.attribute_error

        def __delete__(self, obj):
            raise self.attribute_error

    return descriptor()

def compose(*decorators):

    def decorate(method):
        for decorator in reversed(decorators):
            method = decorator(method)
        return method

    return decorate
