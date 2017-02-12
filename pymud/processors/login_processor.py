import re

from pymud import LOGGER

from pymud.network import ClientConnectionManager

from .base_processor import BaseProcessor


class LoginProcessor(BaseProcessor):
    def __init__(self, client_connection):
        BaseProcessor.__init__(
            self,
            client_connection
        )

    def process(self):
        if not self._client_connection.character.waiting_for_name:
            return True
        self._client_connection.send('Please enter your name')
        request = self._client_connection.recv(64) or ''
        if re.match(r'^GET|HEAD|OPTIONS|POST|PUT', request):
            raise NotImplementedError()
        if not re.match(r'^[a-zA-Z]{3,12}$', request):
            return False
        self._client_connection.character.name = request.capitalize()
        LOGGER.debug(
            '%s:%s - %s connected' % (
                self._client_connection.remote_ip,
                self._client_connection.remote_port,
                self._client_connection.character.name,
            )
        )
        self._client_connection.send('Welcome %s!' % self._client_connection.character.name)
        matching_client_connections = ClientConnectionManager.instance.get_all_except(
            [self._client_connection],
            exclude_waiting_for_name=True
        )
        for matching_client_connection in matching_client_connections:
            matching_client_connection.send(
                '%s just arrived' % self._client_connection.character.name,
                num_leading_new_lines=1
            )
        return not self._client_connection.character.waiting_for_name
