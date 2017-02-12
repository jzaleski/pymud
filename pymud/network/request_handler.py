import sys

from SocketServer import BaseRequestHandler

from pymud import LOGGER

from pymud.processors import (
    CommandProcessor,
    LoginProcessor,
)

from . import (
    ClientConnection,
    ClientConnectionManager,
)


class RequestHandler(BaseRequestHandler):
    def finish(self):
        ClientConnectionManager.instance.remove(self.__client_connection)

    def handle(self):
        try:
            while not self.__login_processor.process():
                continue
            while self.__command_processor.process():
                continue
        except Exception as e:
            if isinstance(e, NotImplementedError):
                return
            if isinstance(e, IOError) and e.errno == 32:
                return
            LOGGER.error(
                sys.exc_info()[1],
                sys.exc_info()[2]
            )

    def setup(self):
        self.__client_connection = ClientConnection(
            self.client_address,
            self.request
        )
        ClientConnectionManager.instance.add(self.__client_connection)
        self.__command_processor = CommandProcessor(self.__client_connection)
        self.__login_processor = LoginProcessor(self.__client_connection)
