from .base_entity import BaseEntity

class CharacterEntity(BaseEntity):

    def __init__(self):
        BaseEntity.__init__(self)
        self.__location = None
        self.__name = None
        self.__on_location_change_callbacks = []
        self.__on_name_change_callbacks = []
        self.__waiting_for_name = True

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, location):
        old_location = self.__location
        self.__location = location
        for callback in self.__on_location_change_callbacks:
            callback(
                self,
                old_location,
                location
            )

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        old_name = self.__name
        self.__name = name
        self.__waiting_for_name = False
        for callback in self.__on_name_change_callbacks:
            callback(
                self,
                old_name,
                name
            )

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    @property
    def waiting_for_name(self):
        return self.__waiting_for_name

    def register_on_name_change_callback(self, callback):
        if callback:
            self.__on_name_change_callbacks.append(callback)

    def register_on_location_change_callback(self, callback):
        if callback:
            self.__on_location_change_callbacks.append(callback)
