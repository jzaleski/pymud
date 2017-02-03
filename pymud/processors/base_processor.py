class BaseProcessor(object):
    def __init__(self, client_connection):
        self.__client_connection = client_connection

    @property
    def _client_connection(self):
        return self.__client_connection
