from .base_command_handler import BaseCommandHandler


class FallCommandHandler(BaseCommandHandler):
    def __init__(self):
        super(FallCommandHandler, self).__init__(
            'fall',
            1,
            resulting_state='lying down'
        )

    def range_0(self, source, args):
        return 'You fall over'

    def range_1(self, source, args):
        return '%s falls over' % source.character.name
