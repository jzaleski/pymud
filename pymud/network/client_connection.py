from pymud.engines import GameEngine

from pymud.entities import CharacterEntity


class ClientConnection(object):
    def __init__(
        self,
        remote_address,
        socket
    ):
        self._id = id(self)
        game_engine = GameEngine.instance
        self._character = CharacterEntity(location=game_engine.starting_location,
            state=game_engine.starting_state)
        self._remote_address = remote_address
        self._socket = socket

    @property
    def id(self):
        return self._id

    @property
    def character(self):
        return self._character

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
        return self._decode(self._socket.recv(buffer_size)).strip()

    def send(
        self,
        message='',
        num_leading_new_lines=0,
        num_trailing_new_lines=1
    ):
        if message:
            self._socket.send(
                self._encode(
                    "%s%s%s\n" % (
                        "\n" * num_leading_new_lines,
                        message,
                        "\n" * num_trailing_new_lines,
                    )
                )
            )

    def _decode(self, value):
        if isinstance(value, bytes):
            value = value.decode()
        return value

    def _encode(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        return value
