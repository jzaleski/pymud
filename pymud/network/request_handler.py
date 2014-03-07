import re, sys

from SocketServer import BaseRequestHandler

from pymud import LOGGER

from pymud.commands import CommandProcessor

from . import (
    ClientConnection,
    ClientConnectionManager,
)

class RequestHandler(BaseRequestHandler):

    def finish(self):
        ClientConnectionManager.instance.remove(self.__client_connection)
        LOGGER.debug(
            '%s:%s - %s disconnected' % (
                self.__client_connection.remote_ip,
                self.__client_connection.remote_port,
                self.__client_connection.character.name,
            )
        )

    def handle(self):
        try:
            while not self.__handle_login():
                continue
            while self.__handle_request():
                continue
        except:
            LOGGER.error(
                sys.exc_info()[1],
                sys.exc_info()[2]
            )

    def setup(self):
        self.__command_processor = CommandProcessor()
        self.__client_connection = ClientConnection(
            self.client_address,
            self.request
        )
        ClientConnectionManager.instance.add(self.__client_connection)

    def __handle_login(self):
        if not self.__client_connection.character.waiting_for_name:
            return True
        self.__client_connection.send('Please enter your name')
        name = self.__client_connection.recv(64)
        if not re.match(r'^[a-zA-Z]{3,12}$', name):
            return False
        self.__client_connection.character.name = name.capitalize()
        LOGGER.debug(
            '%s:%s - %s connected' % (
                self.__client_connection.remote_ip,
                self.__client_connection.remote_port,
                self.__client_connection.character.name,
            )
        )
        self.__client_connection.send('Welcome %s!' % self.__client_connection.character.name)
        matching_client_connections = ClientConnectionManager.instance.get_all_except(
            [self.__client_connection],
            exclude_waiting_for_name=True
        )
        for matching_client_connection in matching_client_connections:
            matching_client_connection.send(
                '%s just arrived' % self.__client_connection.character.name,
                num_leading_new_lines=1
            )
        return not self.__client_connection.character.waiting_for_name

    def __handle_request(self):
        if self.__client_connection.character.waiting_for_name:
            return True
        return self.__command_processor.process(
            self.__client_connection,
            self.__client_connection.recv(256)
        )
