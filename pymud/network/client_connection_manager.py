from six.moves import _thread as thread

from pymud.utilities.decorators import classproperty


class ClientConnectionManager(object):
    _lock = thread.allocate_lock()

    def __new__(cls, *args, **kwargs):
        return cls.instance

    @classproperty
    def instance(cls):
        cls._lock.acquire()
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
            cls._instance._client_connections = {}
            cls._instance._client_connections_by_name = {}
            cls._instance._client_connections_by_location = {}
        cls._lock.release()
        return cls._instance

    def add(self, client_connection):
        if client_connection:
            character = client_connection.character
            self._client_connections[client_connection.id] = client_connection
            client_connection.character.register_on_name_change_callback(
                self._on_client_connection_name_change)
            client_connection.character.register_on_location_change_callback(
                self._on_client_connection_location_change)

    def close(self, client_connection):
        if client_connection:
            try:
                client_connection.close()
            except:
                pass

    def close_all(self):
        for client_connection in self.get_all():
            self.close(client_connection)

    def close_and_remove(self, client_connection):
        self.close(client_connection)
        self.remove(client_connection)

    def close_and_remove_all(self):
        self.close_all()
        self.remove_all()

    def get_all(self, exclude_waiting_for_name=False):
        for _, client_connection in enumerate(self._client_connections.values()):
            if exclude_waiting_for_name and client_connection.character.waiting_for_name:
                continue
            else:
                yield client_connection

    def get_all_except(
        self,
        client_connections_to_exclude,
        exclude_waiting_for_name=False
    ):
        for _, client_connection in enumerate(self._client_connections.values()):
            if (exclude_waiting_for_name and client_connection.character.waiting_for_name or \
                client_connection in client_connections_to_exclude):
                continue
            else:
                yield client_connection

    def get_by_location(self, location):
        return self.get_by_location_except(location, [])

    def get_by_location_except(
        self,
        location,
        client_connections_to_exclude
    ):
        client_connections = self._client_connections_by_location.get(location, [])
        for _, client_connection in enumerate(client_connections):
            if client_connection in client_connections_to_exclude:
                continue
            else:
                yield client_connection

    def get_by_name(self, name):
        return self._client_connections_by_name.get(name, None)

    def remove(self, client_connection):
        if client_connection:
            client_connection_id = client_connection.id
            if client_connection_id in self._client_connections:
                del self._client_connections[client_connection_id]
            name = client_connection.character.name
            if name in self._client_connections_by_name:
                del self._client_connections_by_name[name]
            location = client_connection.character.location
            if (location in self._client_connections_by_location and \
                client_connection_id in self._client_connections_by_location[location]):
                del self._client_connections_by_location[location][client_connection_id]

    def remove_all(self):
        for client_connection in self.get_all():
            self.remove(client_connection)

    def _on_client_connection_location_change(
        self,
        client_connection,
        old_location,
        new_location
    ):
        client_connection_id = client_connection.id
        old_client_connections_by_client_connection_id = \
            self._client_connections_by_location.get(old_location, {})
        if client_connection_id in old_client_connections_by_client_connection_id:
            del old_client_connections_by_client_connection_id[client_connection_id]
            self._client_connections_by_location[old_location] = \
                old_client_connections_by_client_connection_id
        new_client_connections_by_client_connection_id = \
            self._client_connections_by_location.get(new_location, {})
        if not client_connection_id in new_client_connections_by_client_connection_id:
            new_client_connections_by_client_connection_id[client_connection_id] = client_connection
            self._client_connections_by_location[new_location] = \
                new_client_connections_by_client_connection_id

    def _on_client_connection_name_change(
        self,
        client_connection,
        old_name,
        new_name
    ):
        if old_name in self._client_connections_by_name:
            del self._client_connections_by_name[old_name]
        self._client_connections_by_name[new_name] = client_connection
