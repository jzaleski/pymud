from .base_command_handler import BaseCommandHandler


class StandCommandHandler(BaseCommandHandler):
    def __init__(self):
        super(StandCommandHandler, self).__init__(
            'stand',
            1,
            resulting_state='standing'
        )

    def range_0(self, source, args):
        return 'You stand up'

    def range_1(self, source, args):
        return '%s stands up' % source.character.name
