from .base_entity import BaseEntity


class CharacterEntity(BaseEntity):
    def __init__(
        self,
        name=None,
        location=None,
        state=None,
        on_name_change_callbacks=None,
        on_location_change_callbacks=None
    ):
        self._name = name
        self._location = location
        self._state = state
        self._on_name_change_callbacks = on_name_change_callbacks or []
        self._on_location_change_callbacks = on_location_change_callbacks or []
        self._waiting_for_name = name is None

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        old_location = self._location
        self._location = location
        for callback in self._on_location_change_callbacks:
            callback(
                self,
                old_location,
                location
            )

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        old_name = self._name
        self._name = name
        self._waiting_for_name = False
        for callback in self._on_name_change_callbacks:
            callback(
                self,
                old_name,
                name
            )

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def waiting_for_name(self):
        return self._waiting_for_name

    def register_on_name_change_callback(self, callback):
        if callback:
            self._on_name_change_callbacks.append(callback)

    def register_on_location_change_callback(self, callback):
        if callback:
            self._on_location_change_callbacks.append(callback)
