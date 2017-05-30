import sys

from six.moves.socketserver import BaseRequestHandler

from pymud import LOGGER

from pymud.processors import CommandProcessor, LoginProcessor

from . import ClientConnection, ClientConnectionManager


class RequestHandler(BaseRequestHandler):
    def finish(self):
        ClientConnectionManager.instance.remove(self._client_connection)

    def handle(self):
        try:
            while not self._login_processor.process():
                continue
            while self._command_processor.process():
                continue
        except Exception as e:
            if isinstance(e, NotImplementedError):
                return
            if isinstance(e, IOError) and e.errno == 32:
                return
            LOGGER.error(sys.exc_info()[1], sys.exc_info()[2])

    def setup(self):
        client_connection = ClientConnection(self.client_address, self.request)
        self._command_processor = CommandProcessor(client_connection)
        self._login_processor = LoginProcessor(client_connection)
        self._client_connection = client_connection
        ClientConnectionManager.instance.add(client_connection)
