from pymud.entities import CharacterEntity


class ClientConnection(object):
    def __init__(self, remote_address, socket):
        self._id = id(self)
        self._character_entity = CharacterEntity(state='standing')
        self._remote_address = remote_address
        self._socket = socket

    @property
    def id(self):
        return self._id

    @property
    def character(self):
        return self._character_entity

    @property
    def remote_ip(self):
        return self._remote_address[0]

    @property
    def remote_port(self):
        return self._remote_address[1]

    def close(self):
        self._socket.shutdown(2)
        self._socket.close()

    def recv(self, buffer_size):
        return self._socket.recv(buffer_size).strip()

    def send(
        self,
        message='',
        num_leading_new_lines=0,
        num_trailing_new_lines=1
    ):
        self._socket.send(
            '%s%s%s' % (
                '\n' * num_leading_new_lines,
                message,
                '\n' * num_trailing_new_lines,
            )
        )
