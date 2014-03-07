from pymud.entities import CharacterEntity

class ClientConnection():

    def __init__(self, remote_address, socket):
        self.__id = id(self)
        self.__character_entity = CharacterEntity()
        self.__remote_address = remote_address
        self.__socket = socket

    @property
    def id(self):
        return self.__id

    @property
    def character(self):
        return self.__character_entity

    @property
    def remote_ip(self):
        return self.__remote_address[0]

    @property
    def remote_port(self):
        return self.__remote_address[1]

    def close(self):
        self.__socket.shutdown(2)
        self.__socket.close()

    def recv(self, buffer_size):
        return self.__socket.recv(buffer_size).strip()

    def send(
        self,
        message='',
        num_leading_new_lines=0,
        num_trailing_new_lines=1
    ):
        self.__socket.send(
            '%s%s%s' % (
                '\n' * num_leading_new_lines,
                message,
                '\n' * num_trailing_new_lines,
            )
        )
