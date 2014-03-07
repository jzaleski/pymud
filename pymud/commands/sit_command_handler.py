from .base_command_handler import BaseCommandHandler

class SitCommandHandler(BaseCommandHandler):

    def __init__(self):
        BaseCommandHandler.__init__(
            self,
            'sit',
            1
        )

    def range_0(self, source, args):
        return 'You sit down'

    def range_1(self, source, args):
        return '%s sits down' % source.character.name
