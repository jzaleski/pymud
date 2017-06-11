from .base_command_handler import BaseCommandHandler


class SitCommandHandler(BaseCommandHandler):
    def __init__(self):
        super(SitCommandHandler, self).__init__(
            'sit',
            1,
            resulting_state='sitting'
        )

    def range_0(
        self,
        source,
        args
    ):
        return 'You sit down'

    def range_1(
        self,
        source,
        args
    ):
        return '%s sits down' % source.character.name
