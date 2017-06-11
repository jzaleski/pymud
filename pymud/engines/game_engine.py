from six.moves import _thread as thread

from pymud.entities import LocationEntity

from pymud.utilities.decorators import classproperty


class GameEngine(object):
    _lock = thread.allocate_lock()

    def __new__(cls, *args, **kwargs):
        return cls.instance

    @classproperty
    def instance(cls):
        cls._lock.acquire()
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        cls._lock.release()
        return cls._instance

    def initialize(self):
        if not hasattr(self, '_initialized'):
            self._starting_location = LocationEntity('Town Square Central',
                "This is the heart of the main square, where townsfolk, travellers, and "
                "adventurers meet.")
            self._starting_state = 'standing'
            self._initialized = True

    @property
    def starting_location(self):
        return self._starting_location

    @property
    def starting_state(self):
        return self._starting_state
