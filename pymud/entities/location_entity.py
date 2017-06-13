from .base_entity import BaseEntity


class LocationEntity(BaseEntity):
    def __init__(
        self,
        name,
        description,
        characters=None,
        exits=None
    ):
        self._id = id(self)
        self._name = name
        self._description = description
        self._characters = characters or []
        self._exits = exits or []

    @property
    def characters(self):
        return self._characters

    @property
    def description(self):
        return self._description

    @property
    def exits(self):
        return self._exits

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
