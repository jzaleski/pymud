from .base_command_handler import BaseCommandHandler


class KneelCommandHandler(BaseCommandHandler):
    def __init__(self):
        super(KneelCommandHandler, self).__init__(
            'kneel',
            1,
            resulting_state='kneeling'
        )

    def range_0(
        self,
        source,
        args
    ):
        return 'You kneel down'

    def range_1(
        self,
        source,
        args
    ):
        return '%s kneels down' % source.character.name
