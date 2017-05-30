from .base_command_handler import BaseCommandHandler


class LieCommandHandler(BaseCommandHandler):
    def __init__(self):
        super(LieCommandHandler, self).__init__(
            'lie',
            1,
            resulting_state='lying down'
        )

    def range_0(self, source, args):
        return 'You lie down'

    def range_1(self, source, args):
        return '%s lies down' % source.character.name
